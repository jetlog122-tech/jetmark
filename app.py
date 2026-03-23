from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# Temporary list to store student data
students_db = []

# --- UPDATED MODERN HTML & CSS TEMPLATE ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GradePortal | Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #6366f1;
            --primary-hover: #4f46e5;
            --bg: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-dim: #94a3b8;
            --success: #22c55e;
            --danger: #ef4444;
        }

        body { 
            font-family: 'Inter', sans-serif; 
            background-color: var(--bg); 
            color: var(--text-main);
            margin: 0;
            display: flex;
            justify-content: center;
            padding: 40px 20px;
        }

        .container { 
            width: 100%;
            max-width: 900px; 
            animation: fadeIn 0.8s ease;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h2 { font-weight: 600; margin-bottom: 30px; letter-spacing: -0.025em; font-size: 2rem; }
        h2 span { color: var(--primary); }

        /* Form Card */
        .glass-card {
            background: var(--card-bg);
            padding: 30px;
            border-radius: 16px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
            margin-bottom: 40px;
        }

        .form-row {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 15px;
            align-items: flex-end;
        }

        @media (max-width: 768px) {
            .form-row { grid-template-columns: 1fr; }
        }

        .form-group label { 
            display: block; 
            font-size: 0.85rem;
            color: var(--text-dim);
            margin-bottom: 8px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        input { 
            width: 100%; 
            padding: 12px; 
            background: #0f172a;
            border: 1px solid #334155; 
            border-radius: 8px; 
            color: white;
            font-size: 1rem;
            transition: all 0.3s;
        }

        input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2);
        }

        button.save-btn { 
            padding: 12px 25px; 
            background-color: var(--primary); 
            color: white; 
            border: none; 
            border-radius: 8px; 
            cursor: pointer; 
            font-weight: 600;
            transition: 0.3s;
            height: 46px;
        }

        button.save-btn:hover { background-color: var(--primary-hover); transform: translateY(-1px); }

        /* Table Styling */
        table { width: 100%; border-collapse: separate; border-spacing: 0 10px; }
        th { 
            text-align: left; 
            padding: 15px; 
            color: var(--text-dim); 
            font-weight: 400;
            font-size: 0.9rem;
        }
        
        td { 
            background: var(--card-bg);
            padding: 18px 15px;
        }

        td:first-child { border-radius: 12px 0 0 12px; border-left: 1px solid rgba(255,255,255,0.05); }
        td:last-child { border-radius: 0 12px 12px 0; border-right: 1px solid rgba(255,255,255,0.05); }

        /* Badges */
        .status-badge { 
            padding: 6px 12px; 
            border-radius: 6px; 
            font-size: 0.75rem; 
            font-weight: 600; 
        }
        .pass { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.2); }
        .fail { background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.2); }

        .delete-btn { 
            color: var(--text-dim); 
            text-decoration: none; 
            font-size: 1.2rem;
            transition: 0.2s;
        }
        .delete-btn:hover { color: var(--danger); }

        .empty-state { text-align: center; color: var(--text-dim); padding: 40px; }
    </style>
</head>
<body>

<div class="container">
    <h2>Grade<span>Portal</span></h2>
    
    <div class="glass-card">
        <form action="/add" method="POST" class="form-row">
            <div class="form-group">
                <label>Student Name</label>
                <input type="text" name="name" placeholder="John Doe" required>
            </div>
            <div class="form-group">
                <label>Section</label>
                <input type="text" name="section" placeholder="12-A" required>
            </div>
            <div class="form-group">
                <label>Final Grade</label>
                <input type="number" step="0.1" name="grade" placeholder="0-100" required>
            </div>
            <button type="submit" class="save-btn">Add Student</button>
        </form>
    </div>

    <table>
        <thead>
            <tr>
                <th>STUDENT</th>
                <th>SECTION</th>
                <th>GRADE</th>
                <th>STATUS</th>
                <th></th>
            </tr>
        </thead>
        <tbody>
            {% for s in students %}
            <tr>
                <td style="font-weight: 600;">{{ s.name }}</td>
                <td style="color: var(--text-dim);">{{ s.section }}</td>
                <td style="font-weight: 600;">{{ s.grade }}%</td>
                <td>
                    <span class="status-badge {{ 'pass' if s.status == 'PASSED' else 'fail' }}">
                        {{ s.status }}
                    </span>
                </td>
                <td style="text-align: right;">
                    <a href="/delete/{{ loop.index0 }}" class="delete-btn" onclick="return confirm('Remove this record?')">×</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    {% if not students %}
    <div class="empty-state">
        No student records found. Start by adding one above.
    </div>
    {% endif %}
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
