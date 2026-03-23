from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
basedir = os.path.abspath(os.path.dirname(__file__))
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

# Create Database File
with app.app_context():
    db.create_all()

# --- MODERN VERTICAL UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradePortal | Database Pro</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --accent: #8b5cf6;
            --bg: #0f172a;
            --surface: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --pass-color: #22c55e;
            --fail-color: #ef4444;
        }

        body { 
            font-family: 'Plus Jakarta Sans', sans-serif; 
            background-color: var(--bg); 
            color: var(--text-primary);
            margin: 0; padding: 20px;
            display: flex; justify-content: center;
        }

        .app-container { width: 100%; max-width: 480px; display: flex; flex-direction: column; gap: 20px; }
        .header { text-align: center; padding: 10px 0; }
        .header h1 { font-size: 1.6rem; margin: 0; font-weight: 700; }
        .header span { color: var(--accent); }

        /* Form Styling */
        .input-card {
            background: var(--surface); padding: 25px; border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.05);
        }

        .form-group { margin-bottom: 15px; }
        .form-group label { 
            display: block; font-size: 0.7rem; color: var(--text-secondary); 
            margin-bottom: 6px; font-weight: 700; text-transform: uppercase;
        }

        input { 
            width: 100%; padding: 12px; background: #151e2f;
            border: 1px solid #334155; border-radius: 10px; color: white;
            box-sizing: border-box; font-size: 0.95rem;
        }
        input:focus { outline: none; border-color: var(--accent); }

        .submit-btn {
            width: 100%; padding: 14px; background: var(--accent);
            color: white; border: none; border-radius: 10px;
            font-weight: 700; cursor: pointer; transition: 0.2s; margin-top: 10px;
        }
        .submit-btn:hover { background: #7c3aed; }

        /* Record Cards */
        .list-section { display: flex; flex-direction: column; gap: 12px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; padding: 0 5px; }
        .section-label { font-size: 0.75rem; color: var(--text-secondary); font-weight: 800; text-transform: uppercase; }

        .student-card {
            background: var(--surface); padding: 16px; border-radius: 20px;
            display: flex; align-items: center; justify-content: space-between;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .info-box { display: flex; flex-direction: column; gap: 2px; }
        .info-box .name { font-weight: 700; font-size: 1.05rem; }
        .info-box .meta { font-size: 0.75rem; color: var(--text-secondary); }
        
        .status-chip {
            font-size: 0.6rem; font-weight: 800; padding: 2px 8px; border-radius: 6px;
            text-transform: uppercase; margin-top: 5px; width: fit-content;
        }

        .right-box { display: flex; align-items: center; gap: 12px; }
        .grade-box {
            width: 45px; height: 45px; border-radius: 12px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 1rem;
        }

        /* Pass/Fail Conditional Styles */
        .is-pass .grade-box { background: rgba(34, 197, 94, 0.1); color: var(--pass-color); border: 1px solid rgba(34, 197, 94, 0.2); }
        .is-pass .status-chip { background: var(--pass-color); color: #052e16; }

        .is-fail .grade-box { background: rgba(239, 68, 68, 0.1); color: var(--fail-color); border: 1px solid rgba(239, 68, 68, 0.2); }
        .is-fail .status-chip { background: var(--fail-color); color: #450a0a; }

        .btn-delete {
            background: #2d3748; color: #cbd5e0; border: none;
            width: 32px; height: 32px; border-radius: 8px;
            cursor: pointer; text-decoration: none; display: flex;
            align-items: center; justify-content: center; font-weight: bold;
        }
        .btn-delete:hover { background: var(--fail-color); color: white; }
    </style>
</head>
<body>

<div class="app-container">
    <div class="header">
        <h1>Grade<span>Portal</span> DB</h1>
    </div>

    <div class="input-card">
        <form action="/add" method="POST">
            <div class="form-group">
                <label>Student Name</label>
                <input type="text" name="name" placeholder="Full Name" required>
            </div>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div class="form-group">
                    <label>Year Level</label>
                    <input type="text" name="year_level" placeholder="e.g. Grade 12" required>
                </div>
                <div class="form-group">
                    <label>Section</label>
                    <input type="text" name="section" placeholder="e.g. STEM-A" required>
                </div>
            </div>
            <div class="form-group">
                <label>Address</label>
                <input type="text" name="address" placeholder="City / Province" required>
            </div>
            <div class="form-group">
                <label>Final Grade</label>
                <input type="number" step="0.1" name="grade" placeholder="0 - 100" required>
            </div>
            <button type="submit" class="submit-btn">Save to Database</button>
        </form>
    </div>

    <div class="list-section">
        <div class="section-header">
            <span class="section-label">Recent Submissions</span>
            <span style="font-size: 0.7rem; color: var(--text-secondary);">{{ students|length }} Students</span>
        </div>
        
        {% for s in students %}
        <div class="student-card {{ 'is-pass' if s.status == 'PASSED' else 'is-fail' }}">
            <div class="info-box">
                <span class="name">{{ s.name }}</span>
                <span class="meta">{{ s.year_level }} • {{ s.section }}</span>
                <span class="meta" style="font-size: 0.7rem; opacity: 0.7;">📍 {{ s.address }}</span>
                <span class="status-chip">{{ s.status }}</span>
            </div>
            
            <div class="right-box">
                <div class="grade-box">
                    {{ s.final_grade|int }}
                </div>
                <a href="/delete/{{ s.id }}" class="btn-delete" onclick="return confirm('Delete this record?')">&times;</a>
            </div>
        </div>
        {% endfor %}
        
        {% if not students %}
        <div style="text-align:center; padding: 40px; color: var(--text-secondary); opacity: 0.5;">
            No database records found.
        </div>
        {% endif %}
    </div>
</div>

</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def index():
    # Query database and show newest records first
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    year_level = request.form.get('year_level')
    section = request.form.get('section')
    address = request.form.get('address')
    try:
        grade = float(request.form.get('grade', 0))
    except:
        grade = 0.0

    status = "PASSED" if grade >= 75 else "FAILED"

    # Save to SQLAlchemy Database
    new_student = Student(
        name=name, 
        year_level=year_level, 
        section=section, 
        address=address, 
        final_grade=grade, 
        status=status
    )
    db.session.add(new_student)
    db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
