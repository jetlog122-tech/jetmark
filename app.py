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
        body { font-family: 'Segoe UI', sans-serif; background-color: #f4f7f6; padding: 40px; }
        .container { max-width: 800px; background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin: auto; }
        h2 { color: #333; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; font-weight: bold; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button.save-btn { width: 100%; padding: 12px; background-color: #4f46e5; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; transition: 0.3s; }
        button.save-btn:hover { background-color: #4338ca; }
        
        table { width: 100%; border-collapse: collapse; margin-top: 30px; }
        th, td { border-bottom: 1px solid #eee; padding: 12px; text-align: left; }
        th { background-color: #f8f9fa; color: #666; }
        
        .status-badge { padding: 5px 10px; border-radius: 15px; font-size: 0.85rem; font-weight: bold; }
        .pass { background: #dcfce7; color: #166534; }
        .fail { background: #fee2e2; color: #991b1b; }
        
        .delete-btn { color: #dc3545; text-decoration: none; font-weight: bold; font-size: 0.9rem; }
        .delete-btn:hover { text-decoration: underline; }
    </style>
</head>
<body>

<div class="container">
    <h2>Student Grade Management</h2>
    
    <form action="/add" method="POST">
        <div class="form-group">
            <label>Student Name</label>
            <input type="text" name="name" required>
        </div>
        <div class="form-group">
            <label>Section</label>
            <input type="text" name="section" required>
        </div>
        <div class="form-group">
            <label>Final Grade</label>
            <input type="number" step="0.1" name="grade" required>
        </div>
        <button type="submit" class="save-btn">Save Record</button>
    </form>

    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Section</th>
                <th>Grade</th>
                <th>Status</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td>{{ s.name }}</td>
                <td>{{ s.section }}</td>
                <td>{{ s.grade }}</td>
                <td>
                    <span class="status-badge {{ 'pass' if s.status == 'PASSED' else 'fail' }}">
                        {{ s.status }}
                    </span>
                </td>
                <td>
                    <a href="/delete/{{ loop.index0 }}" class="delete-btn" onclick="return confirm('Delete this student?')">Delete</a>
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
    try:
        grade = float(request.form.get('grade', 0))
    except ValueError:
        grade = 0.0

    status = "PASSED" if grade >= 75 else "FAILED"

    students_db.append({
        "name": name,
        "section": section,
        "grade": grade,
        "status": status
    })
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    # Check if the index exists, then remove it
    if 0 <= student_id < len(students_db):
        students_db.pop(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
