import os
import time
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session
from models import create_tables, get_db
from ai_engine import generate_outfits
import requests
from nlp_engine import parse_prompt

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

API_KEY = "6dcca2e4c2eb786cedc40dfe171f831f"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app = Flask(__name__)
app.secret_key = "super_secret_fashion_ai_key" # Required for sessions
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
create_tables()

@app.route("/")
def home():
    if "user_id" in session:
        return redirect(url_for("wardrobe"))
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        mobile = request.form["mobile"]
        password = request.form["password"]
        
        db = get_db()
        try:
            hashed_pw = generate_password_hash(password)
            db.execute("INSERT INTO users (username, mobile, password) VALUES (?, ?, ?)", 
                       (username, mobile, hashed_pw))
            db.commit()
            return redirect(url_for("login"))
        except:
            return render_template("signup.html", error="Username already exists!")
            
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        
        if user and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["username"] = user[1]
            return redirect(url_for("wardrobe"))
        else:
            return render_template("login.html", error="Invalid credentials")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/wardrobe", methods=["GET", "POST"])
def wardrobe():
    if "user_id" not in session:
        return redirect(url_for("login"))
        
    db = get_db()
    edit_id = request.args.get("edit_id")
    edit_item = None
    
    if request.method == "POST":
        if "wear" in request.form:
             # Increment worn count
            db.execute("UPDATE wardrobe SET worn_count = worn_count + 1 WHERE id=?", (request.form["wear"],))
            db.commit()
            return redirect(url_for("wardrobe"))

        if "delete" in request.form:
            # Delete wardrobe item and its image
            item = db.execute("SELECT image FROM wardrobe WHERE id=?", (request.form["delete"],)).fetchone()
            if item and item[0]:
                image_path = os.path.join(UPLOAD_FOLDER, item[0])
                if os.path.exists(image_path):
                    os.remove(image_path)
            db.execute("DELETE FROM wardrobe WHERE id=?", (request.form["delete"],))
            db.commit()
            return redirect(url_for("wardrobe"))
        
        # Handle file upload
        image_filename = None
        if "image" in request.files:
            file = request.files["image"]
            print(f"DEBUG: File received: {file}")
            print(f"DEBUG: Filename: {file.filename}")

            if file and file.filename != "":
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    timestamp = str(int(time.time()))
                    filename = f"{timestamp}_{filename}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)

                    print(f"DEBUG: Saving to: {filepath}")
                    file.save(filepath)

                    if os.path.exists(filepath):
                        print(f"SUCCESS: File saved - {filename}")
                        image_filename = filename
                    else:
                        print("ERROR: File failed to save")
                else:
                    print(f"ERROR: File type not allowed: {file.filename}")
        else:
            print("DEBUG: No image in request.files")

        
        if "update" in request.form:
            # Update existing item
            item_id = request.form["update"]
            # Get old image to preserve if no new one uploaded
            old_item = db.execute("SELECT image FROM wardrobe WHERE id=?", (item_id,)).fetchone()
            if not image_filename and old_item:
                image_filename = old_item[0]
            
            db.execute("""
            UPDATE wardrobe SET name=?, category=?, formality=?, season=?, color=?, image=?
            WHERE id=?
            """, (
                request.form["name"],
                request.form["category"],
                request.form["formality"],
                request.form["season"],
                request.form["color"],
                image_filename,
                item_id
            ))
        else:
            # Add new item
            db.execute("""
            INSERT INTO wardrobe (name, category, formality, season, color, image)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                request.form["name"],
                request.form["category"],
                request.form["formality"],
                request.form["season"],
                request.form["color"],
                image_filename
            ))
        db.commit()
        return redirect(url_for("wardrobe"))
    
    # Get item to edit if edit_id provided
    if edit_id:
        edit_item = db.execute("SELECT * FROM wardrobe WHERE id=?", (edit_id,)).fetchone()
    
    items = db.execute("SELECT * FROM wardrobe").fetchall()
    return render_template("wardrobe.html", items=items, edit_item=edit_item)

@app.route("/calendar", methods=["GET", "POST"])
def calendar():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    edit_id = request.args.get("edit_id")
    edit_event = None
    
    if request.method == "POST":
        if "update" in request.form:
            # Update existing event
            db.execute("""
            UPDATE events SET title=?, date=?, event_type=?
            WHERE id=?
            """, (
                request.form["title"],
                request.form["date"],
                request.form["event_type"],
                request.form["update"]
            ))
        elif "delete" in request.form:
            # Delete event
            db.execute("DELETE FROM events WHERE id=?", (request.form["delete"],))
        else:
            # Add new event
            db.execute("""
            INSERT INTO events (title, date, event_type)
            VALUES (?, ?, ?)
            """, (
                request.form["title"],
                request.form["date"],
                request.form["event_type"]
            ))
        db.commit()
    
    # Get event to edit if edit_id provided
    if edit_id:
        edit_event = db.execute("SELECT * FROM events WHERE id=?", (edit_id,)).fetchone()
    
    events = db.execute("SELECT * FROM events").fetchall()
    return render_template("calendar.html", events=events, edit_event=edit_event)

@app.route("/outfits", methods=["GET", "POST"])
def outfits():
    if "user_id" not in session:
        return redirect(url_for("login"))
    db = get_db()
    wardrobe_items = db.execute("SELECT * FROM wardrobe").fetchall()

    # build richer wardrobe objects including name, season and image
    wardrobe = [{
        "id": w[0],
        "name": w[1],
        "category": w[2],
        "formality": w[3],
        "season": w[4],
        "color": w[5],
        "image": w[6],
        "worn_count": w[7] if len(w) > 7 else 0
    } for w in wardrobe_items]

    results = []
    searched = False
    weather_info = None
    ai_analysis = None
    
    if request.method == "POST":
        searched = True
        
        # 1. Init variables
        location = request.form.get("location")
        occasion = request.form.get("occasion")
        prompt = request.form.get("prompt")
        
        temperature_str = "20°C" # default
        
        # 2. Check for AI Chat Prompt
        if prompt:
            analysis = parse_prompt(prompt)
            if analysis:
                ai_analysis = {
                    "prompt": prompt,
                    "occasion": analysis.get("occasion", "Casual"), # fallback if not detected
                    "temperature": analysis.get("temperature", "20°C")
                }
                occasion = ai_analysis["occasion"]
                temperature_str = ai_analysis["temperature"]
        
        # 3. If no AI prompt (or AI missed temp), try Weather API
        if not ai_analysis or not ai_analysis.get("temperature"):
            if location:
                try:
                    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
                    response = requests.get(url)
                    data = response.json()
                    
                    if response.status_code == 200:
                        temp = int(data["main"]["temp"])
                        desc = data["weather"][0]["description"].title()
                        weather_info = {
                            "city": data["name"],
                            "temp": temp,
                            "desc": desc
                        }
                        temperature_str = f"{temp}°C"
                except Exception as e:
                    print(f"Weather API Exception: {e}")

        # 4. Generate
        results = generate_outfits(
            wardrobe,
            occasion,
            temperature_str
        )

    return render_template("outfits.html", outfits=results, searched=searched, weather_info=weather_info, ai_analysis=ai_analysis)

@app.route("/outfit_worn", methods=["POST"])
def outfit_worn():
    """Increment the worn count for items in an outfit"""
    db = get_db()
    
    # Get the item IDs from the request
    top_id = request.form.get("top_id")
    bottom_id = request.form.get("bottom_id")
    shoe_id = request.form.get("shoe_id")
    
    # Increment worn count for each item
    if top_id:
        db.execute("UPDATE wardrobe SET worn_count = worn_count + 1 WHERE id = ?", (top_id,))
    if bottom_id:
        db.execute("UPDATE wardrobe SET worn_count = worn_count + 1 WHERE id = ?", (bottom_id,))
    if shoe_id:
        db.execute("UPDATE wardrobe SET worn_count = worn_count + 1 WHERE id = ?", (shoe_id,))
    
    db.commit()
    return redirect(url_for("outfits"))

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
