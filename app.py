from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Temporary list to store student data
students_db = []

# --- VERTICAL CLEAN HTML & CSS ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradePortal | Pro</title>
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

        .header {
            padding: 10px 0;
            text-align: center;
        }

        .header h1 { font-size: 1.6rem; margin: 0; font-weight: 700; letter-spacing: -1px; }
        .header span { color: var(--accent); }

        /* Form Card */
        .input-card {
            background: var(--surface);
            padding: 25px;
            border-radius: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
        }

        .form-group { margin-bottom: 18px; }
        .form-group label { 
            display: block; 
            font-size: 0.75rem; 
            color: var(--text-secondary); 
            margin-bottom: 8px;
            font-weight: 700;
            letter-spacing: 0.05em;
        }

        input { 
            width: 100%; 
            padding: 14px; 
            background: #151e2f;
            border: 1px solid #334155; 
            border-radius: 12px; 
            color: white;
            box-sizing: border-box;
            font-size: 1rem;
            transition: 0.2s;
        }

        input:focus { 
            outline: none; 
            border-color: var(--accent); 
            box-shadow: 0 0 0 4px rgba(139, 92, 246, 0.15);
        }

        .submit-btn {
            width: 100%;
            padding: 16px;
            background: var(--accent);
            color: white;
            border: none;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            transition: 0.2s;
            font-size: 1rem;
        }

        .submit-btn:hover { background: #7c3aed; transform: translateY(-1px); }

        /* List Section */
        .list-section {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 5px;
        }

        .section-label {
            font-size: 0.75rem; 
            color: var(--text-secondary); 
            font-weight: 800;
            text-transform: uppercase;
        }

        .student-card {
            background: var(--surface);
            padding: 16px;
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }

        .student-card:hover { border-color: rgba(255,255,255,0.15); }

        .info-box { display: flex; flex-direction: column; gap: 2px; }
        .info-box .name { font-weight: 700; font-size: 1.05rem; }
        .info-box .section-name { font-size: 0.8rem; color: var(--text-secondary); }
        
        /* Status Badge */
        .status-chip {
            font-size: 0.65rem;
            font-weight: 800;
            padding: 2px 8px;
            border-radius: 6px;
            text-transform: uppercase;
            width: fit-content;
            margin-top: 4px;
        }

        .right-box { display: flex; align-items: center; gap: 15px; }

        .grade-circle {
            width: 45px;
            height: 45px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 1rem;
        }

        /* Pass/Fail Styles */
        .is-pass .grade-circle { background: rgba(34, 197, 94, 0.1); color: var(--pass-color); border: 1px solid rgba(34, 197, 94, 0.2); }
        .is-pass .status-chip { background: var(--pass-color); color: #052e16; }

        .is-fail .grade-circle { background: rgba(239, 68, 68, 0.1); color: var(--fail-color); border: 1px solid rgba(239, 68, 68, 0.2); }
        .is-fail .status-chip { background: var(--fail-color); color: #450a0a; }

        .remove-action-btn {
            background: #2d3748;
            color: #cbd5e0;
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 10px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            text-decoration: none;
            font-weight: bold;
            transition: 0.2s;
        }

        .remove-action-btn:hover { background: var(--fail-color); color: white; }

        .empty-state {
            text-align: center;
            padding: 40px;
            color: var(--text-secondary);
            border: 2px dashed rgba(255,255,255,0.05);
            border-radius: 20px;
        }
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
                <label>FULL NAME</label>
                <input type="text" name="name" placeholder="Ex. Juan Dela Cruz" required>
            </div>
            <div class="form-group">
                <label>SECTION</label>
                <input type="text" name="section" placeholder="Ex. 12 - STEM A" required>
            </div>
            <div class="form-group">
                <label>FINAL GRADE</label>
                <input type="number" step="0.1" name="grade" placeholder="0 - 100" required>
            </div>
            <button type="submit" class="submit-btn">Save Student</button>
        </form>
    </div>

    <div class="list-section">
        <div class="section-header">
            <span class="section-label">Records</span>
            <span style="font-size: 0.75rem; color: var(--text-secondary);">{{ students|length }} Total</span>
        </div>
        
        {% for s in students %}
        <div class="student-card {{ 'is-pass' if s.status == 'PASSED' else 'is-fail' }}">
            <div class="info-box">
                <span class="name">{{ s.name }}</span>
                <span class="section-name">{{ s.section }}</span>
                <span class="status-chip">{{ s.status }}</span>
            </div>
            
            <div class="right-box">
                <div class="grade-circle">
                    {{ s.grade|round|int }}
                </div>
                <a href="/delete/{{ loop.index0 }}" class="remove-action-btn" onclick="return confirm('Remove this student?')">
                    &times;
                </a>
            </div>
        </div>
        {% endfor %}
        
        {% if not students %}
        <div class="empty-state">
            No records found.
        </div>
        {% endif %}
    </div>
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
    except (ValueError, TypeError):
        grade = 0.0

    status = "PASSED" if grade >= 75 else "FAILED"

    # Insert at the beginning so the newest record is at the top
    students_db.insert(0, {
        "name": name,
        "section": section,
        "grade": grade,
        "status": status
    })
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    if 0 <= student_id < len(students_db):
        students_db.pop(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
