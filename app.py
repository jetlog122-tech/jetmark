from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Temporary storage (clears when you restart the server)
students = []

# Simple HTML template to display the form and the results
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Grade Checker</title>
    <style>
        body { font-family: sans-serif; margin: 40px; line-height: 1.6; }
        .pass { color: green; font-weight: bold; }
        .fail { color: red; font-weight: bold; }
        input { margin-bottom: 10px; display: block; padding: 5px; }
    </style>
</head>
<body>
    <h2>Enter Student Details</h2>
    <form method="POST" action="/add_student">
        <input type="text" name="name" placeholder="Student Name" required>
        <input type="text" name="section" placeholder="Section" required>
        <input type="number" name="grade" placeholder="Grade (0-100)" required>
        <button type="submit">Submit</button>
    </form>

    <hr>

    <h2>Student List</h2>
    <ul>
        {% for s in students %}
            <li>
                <strong>{{ s.name }}</strong> (Section: {{ s.section }}) - 
                Grade: {{ s.grade }} - 
                Status: <span class="{{ s.status.lower() }}">{{ s.status }}</span>
            </li>
        {% endfor %}
    </ul>
</body>
</html>
"""

@app.route('/')
def home():
    # We use render_template_string to keep everything in one file for now
    return render_template_string(HTML_TEMPLATE, students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form.get('name')
    section = request.form.get('section')
    grade = int(request.form.get('grade'))

    # Passing Logic: 75 is the usual passing mark
    status = "Pass" if grade >= 75 else "Fail"

    # Save to our list
    students.append({
        "name": name,
        "section": section,
        "grade": grade,
        "status": status
    })

    # Return to the home page to see the updated list
    return render_template_string(HTML_TEMPLATE, students=students)

if __name__ == "__main__":
    app.run(debug=True)
