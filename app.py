from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ========================= DATA =========================

courses = [
    {
        "title": "Python for Beginners",
        "category": "Python",
        "provider": "FreeCodeCamp",
        "level": "Beginner",
        "language": "English",
        "rating": 4.8,
        "completed": 1250,
        "url": "https://www.freecodecamp.org/"
    },
    {
        "title": "AI/ML Basics",
        "category": "AI/ML",
        "provider": "Google",
        "level": "Beginner",
        "language": "English",
        "rating": 4.7,
        "completed": 980,
        "url": "https://developers.google.com/machine-learning"
    },
    {
        "title": "JEE Preparation",
        "category": "JEE",
        "provider": "YouTube",
        "level": "Intermediate",
        "language": "Hindi",
        "rating": 4.6,
        "completed": 2300,
        "url": "https://www.youtube.com/"
    },
    {
        "title": "Web Development Bootcamp",
        "category": "Web Dev",
        "provider": "The Odin Project",
        "level": "Beginner",
        "language": "English",
        "rating": 4.9,
        "completed": 3100,
        "url": "https://www.theodinproject.com/"
    },
]

books = [
    {
        "title": "Automate the Boring Stuff with Python",
        "author": "Al Sweigart",
        "category": "Python",
        "rating": 4.9,
        "url": "https://automatetheboringstuff.com/"
    },
]

tools = [
    {
        "name": "GitHub",
        "category": "Coding",
        "description": "Code hosting platform",
        "rating": 4.9,
        "url": "https://github.com/"
    },
]

notes = []

# ========================= MODELS =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

# ========================= ROUTES =========================

@app.route("/")
def home():
    return render_template(
        "index.html",
        courses=courses
    )

@app.route("/courses")
def course_page():
    query = request.args.get("q", "").lower()

    filtered = courses

    if query:
        filtered = [
            c for c in courses
            if query in c["title"].lower()
            or query in c["category"].lower()
        ]

    return render_template(
        "courses.html",
        courses=filtered
    )

@app.route("/books")
def book_page():
    return render_template(
        "books.html",
        books=books
    )

@app.route("/tools")
def tool_page():
    return render_template(
        "tools.html",
        tools=tools
    )

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

    return render_template(
        "notes.html",
        notes=notes
    )

# ========================= SIGNUP =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:

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

# ========================= LOGIN =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(
            email=email
        ).first()

        # signup nahi kiya
        if not user:

            return render_template(
                "login.html",
                error="Please signup first."
            )

        # password galat
        if user.password != password:

            return render_template(
                "login.html",
                error="Invalid email or password."
            )

        # successful login
        return redirect(url_for("home"))

    return render_template("login.html")

# ========================= DATABASE INIT =========================

with app.app_context():
    db.create_all()

# ========================= RUN APP =========================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )