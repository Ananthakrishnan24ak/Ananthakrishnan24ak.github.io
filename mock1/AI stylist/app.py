from flask import Flask, request, jsonify, render_template
import json
import os
import datetime

app = Flask(__name__)

# Correctly point to the data directory relative to this file
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

def load_data():
    garments = []
    if not os.path.exists(DATA_DIR):
        print(f"Data directory not found: {DATA_DIR}")
        return garments
    
    for filename in os.listdir(DATA_DIR):
        if filename.endswith('.json'):
            filepath = os.path.join(DATA_DIR, filename)
            try:
                with open(filepath, 'r') as f:
                    site_data = json.load(f)
                    if isinstance(site_data, list):
                        garments.extend(site_data)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    return garments

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/outfits', methods=['POST'])
def get_outfits():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    occasion = data.get('occasion', '').strip().lower()
    climate = data.get('climate', '').strip().lower()
    occasion_date_str = data.get('occasionDate')
    
    if not all([occasion, climate, occasion_date_str]):
        return jsonify({"error": "Missing required fields: occasion, climate, occasionDate"}), 400
        
    try:
        occasion_date = datetime.datetime.strptime(occasion_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

    garments = load_data()
    results = []
    
    for g in garments:
        # Check delivery date
        delivery_date_str = g.get('deliveryDate')
        if not delivery_date_str:
            continue

        try:
            delivery_date = datetime.datetime.strptime(delivery_date_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            continue # Skip invalid dates
            
        if delivery_date > occasion_date:
            continue
            
        # Check tags
        tags = [t.lower() for t in g.get('tags', [])]
        
        if occasion in tags and climate in tags:
            results.append(g)
            
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
