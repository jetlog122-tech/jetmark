from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Temporary list to store student data
students_db = []

# --- VERTICAL MODERN HTML & CSS ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradePortal | Vertical</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --accent: #8b5cf6;
            --accent-soft: rgba(139, 92, 246, 0.1);
            --bg: #0f172a;
            --surface: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
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
            max-width: 450px; /* Constrained width for a vertical "App" look */
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .header {
            padding: 20px 0;
            text-align: center;
        }

        .header h1 { font-size: 1.5rem; margin: 0; font-weight: 700; }
        .header span { color: var(--accent); }

        /* Stats Row */
        .stats-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .stat-card {
            background: var(--surface);
            padding: 15px;
            border-radius: 16px;
            text-align: center;
            border: 1px solid rgba(255,255,255,0.05);
        }

        .stat-card small { color: var(--text-secondary); font-size: 0.75rem; text-transform: uppercase; }
        .stat-card div { font-size: 1.25rem; font-weight: 700; margin-top: 5px; }

        /* Vertical Form */
        .input-card {
            background: var(--surface);
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }

        .form-group { margin-bottom: 18px; }
        .form-group label { 
            display: block; 
            font-size: 0.8rem; 
            color: var(--text-secondary); 
            margin-bottom: 8px;
            font-weight: 600;
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
        }

        input:focus { outline: none; border-color: var(--accent); background: #1a2438; }

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
            margin-top: 10px;
        }

        .submit-btn:hover { opacity: 0.9; transform: scale(0.98); }

        /* List Section */
        .list-section {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .student-item {
            background: var(--surface);
            padding: 15px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            border: 1px solid rgba(255,255,255,0.05);
            transition: 0.3s;
        }

        .student-info { display: flex; flex-direction: column; }
        .student-info .name { font-weight: 700; font-size: 1rem; }
        .student-info .meta { font-size: 0.8rem; color: var(--text-secondary); }

        .grade-pill {
            padding: 6px 12px;
            border-radius: 10px;
            font-weight: 700;
            font-size: 0.85rem;
            min-width: 45px;
            text-align: center;
        }

        .pass { background: rgba(34, 197, 94, 0.15); color: #4ade80; }
        .fail { background: rgba(239, 68, 68, 0.15); color: #f87171; }

        .delete-icon {
            color: var(--text-secondary);
            text-decoration: none;
            margin-left: 15px;
            font-size: 1.2rem;
        }
    </style>
</head>
<body>

<div class="app-container">
    <div class="header">
        <h1>Grade<span>Portal</span></h1>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <small>Total Students</small>
            <div>{{ students|length }}</div>
        </div>
        <div class="stat-card">
            <small>Class Avg</small>
            <div>
                {% if students %}
                    {{ (students|map(attribute='grade')|sum / students|length)|round(1) }}%
                {% else %}
                    0%
                {% endif %}
            </div>
        </div>
    </div>

    <div class="input-card">
        <form action="/add" method="POST">
            <div class="form-group">
                <label>STUDENT NAME</label>
                <input type="text" name="name" placeholder="Enter full name" required>
            </div>
            <div class="form-group">
                <label>SECTION</label>
                <input type="text" name="section" placeholder="e.g. Grade 12 - Zeus" required>
            </div>
            <div class="form-group">
                <label>FINAL GRADE</label>
                <input type="number" step="0.1" name="grade" placeholder="0.0" required>
            </div>
            <button type="submit" class="submit-btn">Save Student Record</button>
        </form>
    </div>

    <div class="list-section">
        <label style="font-size: 0.75rem; color: var(--text-secondary); font-weight: 700;">RECENT RECORDS</label>
        {% for s in students %}
        <div class="student-item">
            <div class="student-info">
                <span class="name">{{ s.name }}</span>
                <span class="meta">{{ s.section }}</span>
            </div>
            <div style="display: flex; align-items: center;">
                <div class="grade-pill {{ 'pass' if s.status == 'PASSED' else 'fail' }}">
                    {{ s.grade }}
                </div>
                <a href="/delete/{{ loop.index0 }}" class="delete-icon" onclick="return confirm('Delete record?')">×</a>
            </div>
        </div>
        {% endfor %}
        
        {% if not students %}
        <p style="text-align: center; color: var(--text-secondary); font-size: 0.9rem; margin-top: 20px;">
            No records yet.
        </p>
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
    if 0 <= student_id < len(students_db):
        students_db.pop(student_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
