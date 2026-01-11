# Ananthakrishnan24ak.github.io

# Fashion AI 👗✨

**Your Intelligent AI Stylist**

---

## 1. Project Title
**Fashion AI**

## 2. Basic Details

*   **Team Name**: Fashtechs
*   **Team Members**:
    *   Ananthakrishnan
    *   Kurian R Varghese
    *   Darren Jose
*   **Track / Theme**: The AI Stylist: An AI that suggests outfits based on a user’s wardrobe, calendar schedule, and weather conditions

### Problem Statement
People often struggle with "Wardrobe Paralysis"—having a closet full of clothes but feeling like they have nothing to wear. Keeping track of what you own, matching items for specific occasions (like interviews or parties), and adapting to changing weather conditions is time-consuming and inefficient. Additionally, many people unintentionally over-wear or under-wear specific items.

### Solution Overview
**Fashion AI** is a smart digital wardrobe assistant that solves this by digitizing your closet. It uses an AI-driven recommendation engine to generate perfect outfit combinations (Top + Bottom + Shoes) based on the **Occasion**, **Weather**, and **Style Rules**. It also includes a "Smart Calendar" to plan outfits for upcoming events and a "Wear Counter" to track clothing usage, helping users make sustainable fashion choices.

### Brief Project Description
Fashion AI is a full-stack web application built with Flask. Users can upload photos of their clothes, which are stored in a database with metadata (Category, Color, Season, Formality). The core feature is the **AI Stylist**, which accepts natural language prompts (e.g., "I have a date night and it's chilly") or manual inputs. It integrates with real-time Weather APIs and uses a Color Theory algorithm to suggest aesthetically pleasing outfits. It simulates a personal stylist experience, ensuring you look your best for every event.

---

## 3. Technical Details

### Tech Stack
*   **Frontend**: HTML5, CSS3 (Custom Dark Mode Design), JavaScript.
*   **Backend**: Python, Flask (Web Framework).
*   **Database**: SQLite (Lightweight, serverless relational database).

### Libraries, APIs, & AI Models
*   **OpenWeatherMap API**: Fetches real-time temperature and weather descriptions for outfit context.
*   **NLP Engine (Custom)**: A keyword-extraction Natural Language Processing module that parses user prompts to detect "Occasion" (e.g., 'interview' → Formal) and "Temperature" context.
*   **Rule-Based AI Engine**: A custom recommendation algorithm that filters wardrobe items based on:
    *   *Seasonality Integration* (Winter clothes for cold weather).
    *   *Occasion Matching* (Formal wear for work).
    *   *Color Theory* (Matching complementary colors).

### Implementation
The application follows the **MVC (Model-View-Controller)** architecture:
1.  **Model**: `models.py` defines the schema for Users, Wardrobe Items, and Events using SQLite.
2.  **View**: Jinja2 templates (`.html` files) render the dynamic UI.
3.  **Controller**: `app.py` handles routing, authentication (Sessions/Hashing), and coordinates the AI logic between the database and the frontend.

---

## 4. Installation & Execution

Follow these steps to run the project locally.

### Prerequisites
*   Python 3.x installed on your system.

### Step 1: Install Dependencies
Open your terminal/command prompt and run:
```bash
pip install flask requests werkzeug
```

### Step 2: Setup Database
The application automatically creates the database (`database.db`) and tables on the first run. No manual SQL setup is required.

### Step 3: Run the Application
Navigate to the project directory and execute:
```bash
python app.py
```

### Step 4: Access the App
Open your web browser and go to:
```
http://127.0.0.1:8080
```

### Step 5: Login
*   Click **Sign Up** to create a new account.
*   Login with your credentials (e.g., username `admin`, password `password`).
*   Enjoy your personal AI Stylist!

---
*Created by Team Fashtechs for [Event/Hackathon Name] 2026*
