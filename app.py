from flask import Flask, render_template_string, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- DATABASE CONFIGURATION ---
# This creates a 'students.db' file in your project directory
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'students.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- DATABASE MODEL ---
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    section = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradePortal | Database Edition</title>
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
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
        }

        .app-container {
            width: 100%;
            max-width: 480px; 
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .header { text-align: center; padding: 10px 0; }
        .header h1 { font-size: 1.6rem; margin: 0; font-weight: 700; }
        .header span { color: var(--accent); }

        /* Input Form */
        .input-card {
            background: var(--surface);
            padding: 25px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
        }

        .form-group { margin-bottom: 18px; }
        .form-group label { 
            display: block; font-size: 0.75rem; color: var(--text-secondary); 
            margin-bottom: 8px; font-weight: 700; text-transform: uppercase;
        }

        input { 
            width: 100%; padding: 14px; background: #151e2f;
            border: 1px solid #334155; border-radius: 12px; color: white;
            box-sizing: border-box; font-size: 1rem;
        }

        input:focus { outline: none; border-color: var(--accent); }

        .submit-btn {
            width: 100%; padding: 16px; background: var(--accent);
            color: white; border: none; border-radius: 12px;
            font-weight: 700; cursor: pointer; font-size: 1rem;
        }

        /* List Section */
        .list-section { display: flex; flex-direction: column; gap: 12px; }
        .section-header { display: flex; justify-content: space-between; align-items: center; }
        .section-label { font-size: 0.75rem; color: var(--text-secondary); font-weight: 800; }

        .clear-btn {
            background: transparent; border: 1px solid #334155; color: var(--text-secondary);
            padding: 4px 10px; border-radius: 8px; font-size: 0.7rem; cursor: pointer; text-decoration: none;
        }
        .clear-btn:hover { background: var(--fail-color); color: white; border-color: var(--fail-color); }

        .student-card {
            background: var(--surface); padding: 16px; border-radius: 20px;
            display: flex; align-items: center; justify-content: space-between;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .info-box { display: flex; flex-direction: column; }
        .info-box .name { font-weight: 700; font-size: 1.05rem; }
        .info-box .section-name { font-size: 0.8rem; color: var(--text-secondary); }
        
        .status-chip {
            font-size: 0.6rem; font-weight: 800; padding: 2px 8px; border-radius: 6px;
            margin-top: 5px; width: fit-content;
        }

        .is-pass .status-chip { background: var(--pass-color); color: #052e16; }
        .is-fail .status-chip { background: var(--fail-color); color: #450a0a; }

        .grade-box {
            width: 42px; height: 42px; border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-weight: 800; font-size: 0.9rem; margin-right: 12px;
        }

        .is-pass .grade-box { background: rgba(34, 197, 94, 0.1); color: var(--pass-color); }
        .is-fail .grade-box { background: rgba(239, 68, 68, 0.1); color: var(--fail-color); }

        .delete-btn {
            color: #4a5568; text-decoration: none; font-size: 1.4rem; font-weight: bold;
        }
        .delete-btn:hover { color: var(--fail-color); }
    </style>
</head>
<body>

<div class="app-container">
    <div class="header">
        <h1>Grade<span>Portal</span></h1>
    </div>

    <div class="input-card">
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
            <button type="submit" class="submit-btn">Add to Database</button>
        </form>
    </div>

    <div class="list-section">
        <div class="section-header">
            <span class="section-label">Database Records</span>
            {% if students %}
            <a href="/clear" class="clear-btn" onclick="return confirm('Delete ALL records?')">Clear All</a>
            {% endif %}
        </div>
        
        {% for s in students %}
        <div class="student-card {{ 'is-pass' if s.status == 'PASSED' else 'is-fail' }}">
            <div class="info-box">
                <span class="name">{{ s.name }}</span>
                <span class="section-name">{{ s.section }}</span>
                <span class="status-chip">{{ s.status }}</span>
            </div>
            
            <div style="display: flex; align-items: center;">
                <div class="grade-box">{{ s.grade|int }}</div>
                <a href="/delete/{{ s.id }}" class="delete-btn" onclick="return confirm('Delete this record?')">&times;</a>
            </div>
        </div>
        {% endfor %}
    </div>
</div>

</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def index():
    # Fetch students from DB ordered by ID descending (newest first)
    students = Student.query.order_by(Student.id.desc()).all()
    return render_template_string(HTML_TEMPLATE, students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form.get('name')
    section = request.form.get('section')
    try:
        grade = float(request.form.get('grade', 0))
    except:
        grade = 0.0

    status = "PASSED" if grade >= 75 else "FAILED"

    new_student = Student(name=name, section=section, grade=grade, status=status)
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

@app.route('/clear')
def clear_all():
    db.session.query(Student).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
