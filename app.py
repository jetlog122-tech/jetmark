from flask import Flask, request, render_template_string, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(_name_)

# --- DATABASE CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(_file_))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'student_records.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year_level = db.Column(db.String(20), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    final_grade = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

with app.app_context():
    db.create_all()

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduTrack | Management</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary: #4f46e5;
            --bg-body: #f8fafc;
            --text-main: #1e293b;
            --border-color: #e2e8f0;
        }

        body { 
            background-color: var(--bg-body);
            color: var(--text-main);
            font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            padding-top: 50px;
        }

        .container { max-width: 1000px; }

        /* Sidebar-style card for form */
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            background: white;
            margin-bottom: 30px;
        }

        .card-header {
            background: white;
            border-bottom: 1px solid var(--border-color);
            padding: 20px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1px;
            font-size: 0.9rem;
        }

        .form-label { font-weight: 600; font-size: 0.85rem; color: #64748b; }

        .form-control, .form-select {
            border: 1px solid var(--border-color);
            padding: 10px;
            border-radius: 8px;
        }

        .btn-primary {
            background-color: var(--primary);
            border: none;
            padding: 10px 20px;
            font-weight: 600;
            border-radius: 8px;
            transition: all 0.2s;
        }

        .btn-primary:hover { background-color: #4338ca; transform: translateY(-1px); }

        /* Table Styling */
        .table-container { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
        .table { margin-bottom: 0; }
        .table thead { background: #f1f5f9; }
        .table th { border: none; padding: 15px; color: #64748b; font-size: 0.8rem; text-transform: uppercase; }
        .table td { padding: 18px 15px; vertical-align: middle; border-bottom: 1px solid #f1f5f9; }

        .status-badge {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
        }

        .passed { background: #dcfce7; color: #166534; }
        .failed { background: #fee2e2; color: #991b1b; }

        .delete-link { color: #94a3b8; text-decoration: none; transition: 0.2s; }
        .delete-link:hover { color: #ef4444; }

        .address-text { color: #94a3b8; font-size: 0.8rem; }
    </style>
</head>
<body>

<div class="container">
    <div class="row">
        <div class="col-md-4">
            <div class="card">
                <div class="card-header">Add New Student</div>
                <div class="card-body p-4">
                    <form action="/add" method="POST">
                        <div class="mb-3">
                            <label class="form-label">Name</label>
                            <input type="text" name="name" class="form-control" placeholder="Juan Dela Cruz" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Year Level</label>
                            <select name="year_level" class="form-select">
                                <option>1st Year</option>
                                <option>2nd Year</option>
                                <option>3rd Year</option>
                                <option>4th Year</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Section</label>
                            <input type="text" name="section" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Final Grade</label>
                            <input type="number" step="0.01" name="final_grade" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Address</label>
                            <textarea name="address" class="form-control" rows="2" required></textarea>
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Save Record</button>
                    </form>
                </div>
            </div>
        </div>

        <div class="col-md-8">
            <div class="table-container">
                <table class="table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Class</th>
                            <th>Grade</th>
                            <th>Status</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for s in student_list %}
                        <tr>
                            <td>
                                <div class="fw-bold">{{ s.name }}</div>
                                <div class="address-text">{{ s.address }}</div>
                            </td>
                            <td>{{ s.year_level }}<br><small class="text-muted">{{ s.section }}</small></td>
                            <td class="fw-bold">{{ s.final_grade }}</td>
                            <td>
                                <span class="status-badge {% if s.status == 'Passed' %}passed{% else %}failed{% endif %}">
                                    {{ s.status | upper }}
                                </span>
                            </td>
                            <td>
                                <a href="/delete/{{ s.id }}" class="delete-link" onclick="return confirm('Delete this record?')">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                                      <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                      <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                                    </svg>
                                </a>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</div>

</body>
</html>
"""

@app.route('/')
def index():
    all_students = Student.query.order_by(Student.id.desc()).all()
    return render_template_string(HTML_PAGE, student_list=all_students)

@app.route('/add', methods=['POST'])
def add_student():
    try:
        grade_val = float(request.form.get('final_grade'))
    except (ValueError, TypeError):
        grade_val = 0.0

    status = "Passed" if grade_val >= 75 else "Failed"
    
    new_student = Student(
        name=request.form.get('name'),
        year_level=request.form.get('year_level'),
        section=request.form.get('section'),
        address=request.form.get('address'),
        final_grade=grade_val,
        status=status
    )
    
    db.session.add(new_student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    student_to_delete = db.session.get(Student, id)
    if student_to_delete:
        db.session.delete(student_to_delete)
        db.session.commit()
    return redirect(url_for('index'))

if _name_ == '_main_':
    app.run(debug=True)
