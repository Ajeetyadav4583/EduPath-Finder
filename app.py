from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

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
    {
        "title": "Data Science with Python",
        "category": "Data Science",
        "provider": "Kaggle",
        "level": "Intermediate",
        "language": "English",
        "rating": 4.7,
        "completed": 1800,
        "url": "https://www.kaggle.com/learn"
    },
    {
        "title": "DSA Masterclass",
        "category": "DSA",
        "provider": "LeetCode",
        "level": "Advanced",
        "language": "English",
        "rating": 4.8,
        "completed": 2100,
        "url": "https://leetcode.com/"
    },
    {
        "title": "UPSC Complete Guide",
        "category": "UPSC",
        "provider": "Unacademy",
        "level": "Intermediate",
        "language": "Hindi/English",
        "rating": 4.5,
        "completed": 890,
        "url": "https://unacademy.com/"
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
    {
        "title": "Think Python",
        "author": "Allen B. Downey",
        "category": "Python",
        "rating": 4.7,
        "url": "https://greenteapress.com/wp/think-python/"
    },
    {
        "title": "Deep Learning Book",
        "author": "Goodfellow, Bengio, Courville",
        "category": "AI/ML",
        "rating": 4.8,
        "url": "https://www.deeplearningbook.org/"
    },
    {
        "title": "Eloquent JavaScript",
        "author": "Marijn Haverbeke",
        "category": "Web Dev",
        "rating": 4.8,
        "url": "https://eloquentjavascript.net/"
    },
]

tools = [
    {
        "name": "GitHub",
        "category": "Coding",
        "description": "Code hosting and portfolio building platform used by every developer.",
        "rating": 4.9,
        "url": "https://github.com/"
    },
    {
        "name": "Google Colab",
        "category": "AI/ML",
        "description": "Run Python and ML notebooks online for free with GPU access.",
        "rating": 4.8,
        "url": "https://colab.research.google.com/"
    },
    {
        "name": "VS Code",
        "category": "Coding",
        "description": "The most popular free code editor with thousands of extensions.",
        "rating": 4.9,
        "url": "https://code.visualstudio.com/"
    },
    {
        "name": "ChatGPT",
        "category": "AI",
        "description": "AI assistant to help debug code, explain concepts and generate ideas.",
        "rating": 4.7,
        "url": "https://chat.openai.com/"
    },
]

notes = []

# ========================= MODELS =========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

# ========================= ROUTES =========================

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


@app.route("/roadmap", methods=["GET", "POST"])
def roadmap_page():
    roadmap = None
    if request.method == "POST":
        goal = request.form.get("goal")
        hours = request.form.get("hours")
        roadmap = [
            f"Goal: {goal} | Daily Time: {hours} hours",
            "Step 1: Basics strong karo — fundamentals skip mat karo.",
            "Step 2: Roz practice karo — consistency > intensity.",
            "Step 3: 2 mini projects banao aur GitHub pe daalo.",
            "Step 4: Community join karo — Discord, Reddit, YouTube comments.",
            "Step 5: 1 bada portfolio project complete karo.",
            "Step 6: Resume update karo aur apply karna shuru karo!",
        ]
    return render_template("roadmap.html", roadmap=roadmap)


@app.route("/notes", methods=["GET", "POST"])
def notes_page():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if title and content:
            notes.append({"title": title, "content": content})
        return redirect(url_for("notes_page"))
    return render_template("notes.html", notes=notes)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = User.query.filter_by(email=email).first()
        if existing:
            return render_template("signup.html", error="Email already registered.")

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            return redirect(url_for("home"))
        return render_template("login.html", error="Invalid email or password.")
    return render_template("login.html")


# ========================= INIT =========================

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)