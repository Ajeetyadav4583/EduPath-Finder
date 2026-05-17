from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "edupath_secret_key"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

courses = [
    {"title": "Python for Beginners", "category": "Python", "provider": "FreeCodeCamp", "level": "Beginner", "language": "English", "rating": 4.8, "completed": 1250, "url": "https://www.freecodecamp.org/"},
    {"title": "AI/ML Basics", "category": "AI/ML", "provider": "Google", "level": "Beginner", "language": "English", "rating": 4.7, "completed": 980, "url": "https://developers.google.com/machine-learning"},
    {"title": "JEE Preparation", "category": "JEE", "provider": "YouTube", "level": "Intermediate", "language": "Hindi", "rating": 4.6, "completed": 2300, "url": "https://www.youtube.com/"},
    {"title": "Web Development Bootcamp", "category": "Web Dev", "provider": "The Odin Project", "level": "Beginner", "language": "English", "rating": 4.9, "completed": 3100, "url": "https://www.theodinproject.com/"},
    {"title": "Data Science with Python", "category": "Data Science", "provider": "Kaggle", "level": "Intermediate", "language": "English", "rating": 4.7, "completed": 1800, "url": "https://www.kaggle.com/learn"},
    {"title": "DSA Masterclass", "category": "DSA", "provider": "LeetCode", "level": "Advanced", "language": "English", "rating": 4.8, "completed": 2100, "url": "https://leetcode.com/"},
    {"title": "UPSC Complete Guide", "category": "UPSC", "provider": "Unacademy", "level": "Intermediate", "language": "Hindi/English", "rating": 4.5, "completed": 890, "url": "https://unacademy.com/"},
]

books = [
    {"title": "Automate the Boring Stuff with Python", "author": "Al Sweigart", "category": "Python", "rating": 4.9, "url": "https://automatetheboringstuff.com/"},
    {"title": "Think Python", "author": "Allen B. Downey", "category": "Python", "rating": 4.7, "url": "https://greenteapress.com/wp/think-python/"},
    {"title": "Deep Learning Book", "author": "Goodfellow, Bengio, Courville", "category": "AI/ML", "rating": 4.8, "url": "https://www.deeplearningbook.org/"},
    {"title": "Eloquent JavaScript", "author": "Marijn Haverbeke", "category": "Web Dev", "rating": 4.8, "url": "https://eloquentjavascript.net/"},
]

tools = [
    {"name": "GitHub", "category": "Coding", "description": "Code hosting and portfolio building platform used by every developer.", "rating": 4.9, "url": "https://github.com/"},
    {"name": "Google Colab", "category": "AI/ML", "description": "Run Python and ML notebooks online for free with GPU access.", "rating": 4.8, "url": "https://colab.research.google.com/"},
    {"name": "VS Code", "category": "Coding", "description": "The most popular free code editor with thousands of extensions.", "rating": 4.9, "url": "https://code.visualstudio.com/"},
    {"name": "ChatGPT", "category": "AI", "description": "AI assistant to help debug code, explain concepts and generate ideas.", "rating": 4.7, "url": "https://chat.openai.com/"},
]

notes = []

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

@app.route("/")
def home():
    return render_template("index.html", courses=courses[:3])

@app.route("/courses")
def course_page():
    query = request.args.get("q", "").lower()
    filtered = courses

    if query:
        filtered = [
            c for c in courses
            if query in c["title"].lower() or query in c["category"].lower()
        ]

    return render_template("courses.html", courses=filtered)

@app.route("/books")
def book_page():
    return render_template("books.html", books=books)

@app.route("/tools")
def tool_page():
    return render_template("tools.html", tools=tools)

# ========================= FOCUS MODE =========================

@app.route("/focus")
def focus_page():
    return render_template("focus.html")

# ========================= ROADMAP =========================

@app.route("/roadmap", methods=["GET", "POST"])
def roadmap_page():
    roadmap = None

    if request.method == "POST":
        goal = request.form.get("goal")
        hours = request.form.get("hours")

        roadmap_data = {
            "Learn Python": [
                f"Goal: {goal} | Daily Time: {hours} hours",
                "Step 1: Python basics, variables, loops aur conditions seekho.",
                "Step 2: Functions, lists, dictionaries aur file handling practice karo.",
                "Step 3: Calculator, quiz app aur notes app jaise mini projects banao.",
                "Step 4: GitHub par projects upload karo.",
                "Step 5: Flask basics seekhkar web project banao."
            ],

            "Become AI Engineer": [
                f"Goal: {goal} | Daily Time: {hours} hours",
                "Step 1: Python, NumPy aur Pandas strong karo.",
                "Step 2: Statistics aur basic math revise karo.",
                "Step 3: Machine Learning algorithms seekho.",
                "Step 4: AI/ML mini projects banao.",
                "Step 5: GitHub par AI portfolio create karo."
            ],

            "Crack JEE": [
                f"Goal: {goal} | Daily Time: {hours} hours",
                "Step 1: Physics, Chemistry, Math ka syllabus divide karo.",
                "Step 2: Daily concepts aur formulas revise karo.",
                "Step 3: Previous year questions solve karo.",
                "Step 4: Weekly mock tests do.",
                "Step 5: Weak topics par extra focus karo."
            ],

            "Prepare UPSC": [
                f"Goal: {goal} | Daily Time: {hours} hours",
                "Step 1: NCERT foundation complete karo.",
                "Step 2: Daily current affairs padho.",
                "Step 3: Polity, History, Geography aur Economy cover karo.",
                "Step 4: Answer writing practice karo.",
                "Step 5: Mock tests aur revision cycle follow karo."
            ],

            "Become Web Developer": [
                f"Goal: {goal} | Daily Time: {hours} hours",
                "Step 1: HTML aur CSS strong karo.",
                "Step 2: JavaScript DOM aur events seekho.",
                "Step 3: Flask backend aur routing seekho.",
                "Step 4: Login/signup wala full stack project banao.",
                "Step 5: GitHub aur Render par deploy karo."
            ],
        }

        roadmap = roadmap_data.get(goal)

    return render_template("roadmap.html", roadmap=roadmap)

@app.route("/notes", methods=["GET", "POST"])
def notes_page():

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        if title and content:

            notes.append({
                "title": title,
                "content": content
            })

        return redirect(url_for("notes_page"))

    return render_template("notes.html", notes=notes)

@app.route("/contact", methods=["GET", "POST"])
def contact_page():

    success = False

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        message = request.form.get("message")

        print("Contact Message:", name, email, message)

        success = True

    return render_template(
        "contact.html",
        success=success
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(email=email).first()

        if existing:

            return render_template(
                "signup.html",
                error="Email already registered."
            )

        new_user = User(
            username=username,
            email=email,
            password=password
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user:

            return render_template(
                "login.html",
                error="Please signup first."
            )

        if user.password != password:

            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        session["username"] = user.username

        return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():

    session.pop("username", None)

    return redirect(url_for("home"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )