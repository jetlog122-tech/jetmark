from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Temporary list to store student data
students_db = []

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Student Grade Management</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; padding: 40px; }
        .container { max-width: 600px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: auto; }
        h2 { color: #333; text-align: center; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background-color: #28a745; color: white; border: none; border-radius: 5px; margin-top: 20px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #218838; }
        table { width: 100%; border-collapse: collapse; margin-top: 30px; }
        th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; }
        .pass { color: #28a745; font-weight: bold; }
        .fail { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>

<div class="container">
    <h2>Student Grade Management</h2>
    
    <form action="/add" method="POST">
        <label>Student Name:</label>
        <input type="text" name="name" placeholder="e.g. Juan Dela Cruz" required>
        
        <label>Section:</label>
        <input type="text" name="section" placeholder="e.g. Zechariah" required>
        
        <label>Final Grade:</label>
        <input type="number" step="0.01" name="grade" placeholder="0-100" required>
        
        <button type="submit">Save Student Record</button>
    </form>

    <hr>

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Section</th>
                <th>Grade</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td>{{ s.name }}</td>
                <td>{{ s.section }}</td>
                <td>{{ s.grade }}</td>
                <td>
                    <span class="{{ 'pass' if s.status == 'PASSED' else 'fail' }}">
                        {{ s.status }}
                    </span>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, students=students_db)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    section = request.form.get('section')
    # Use a default of 0 if grade is missing or invalid
    try:
        grade = float(request.form.get('grade', 0))
    except ValueError:
        grade = 0.0

    # Logic: 75 and above is PASSED
    status = "PASSED" if grade >= 75 else "FAILED"

    # Add to our temporary list
    students_db.append({
        "name": name,
        "section": section,
        "grade": grade,
        "status": status
    })

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
