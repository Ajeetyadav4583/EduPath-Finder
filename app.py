from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    }
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
    }
]

tools = [
    {
        "name": "GitHub",
        "category": "Coding",
        "description": "Code hosting and portfolio building platform.",
        "rating": 4.9,
        "url": "https://github.com/"
    },
    {
        "name": "Google Colab",
        "category": "AI/ML",
        "description": "Run Python and ML notebooks online.",
        "rating": 4.8,
        "url": "https://colab.research.google.com/"
    }
]

notes = []

@app.route("/")
def home():
    return render_template("index.html", courses=courses)

@app.route("/courses")
def course_page():
    query = request.args.get("q", "").lower()
    filtered_courses = courses

    if query:
        filtered_courses = [
            course for course in courses
            if query in course["title"].lower() or query in course["category"].lower()
        ]

    return render_template("courses.html", courses=filtered_courses)

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
            f"Goal: {goal}",
            f"Daily Study Time: {hours} hours",
            "Step 1: Basics strong karo.",
            "Step 2: Daily practice karo.",
            "Step 3: 2 mini projects banao.",
            "Step 4: GitHub par upload karo.",
            "Step 5: Portfolio project complete karo."
        ]

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

if __name__ == "__main__":
    app.run(debug=True)