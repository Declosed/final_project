import os
import json
from flask import Flask, render_template, request, redirect, url_for

# 1. Establish the current root directory path
base_dir = os.path.abspath(os.path.dirname(__file__))
db_file_path = os.path.join(base_dir, 'students_db.json')

# 2. Automated Search Matrix: Scans all possible folder levels for your template files
possible_paths = [
    base_dir,                                              # Main Root folder
    os.path.join(base_dir, 'portal'),                      # Inside /portal/
    os.path.join(base_dir, 'templates'),                   # Inside /templates/
    os.path.join(base_dir, 'portal', 'templates'),         # Inside /portal/templates/
    os.path.join(base_dir, 'portal', 'templates', 'portal') # Inside /portal/templates/portal/
]

# Loop checks which folder contains portal_core.html and locks Flask to it instantly
template_folder_resolved = base_dir
for folder in possible_paths:
    if os.path.exists(os.path.join(folder, 'portal_core.html')):
        template_folder_resolved = folder
        break

# Initialize Flask tied to the automatically resolved folder path layout
app = Flask(
    __name__, 
    template_folder=template_folder_resolved,  
    static_folder=template_folder_resolved     
)

# --- SECURE DATABASE READ/WRITE UTILITIES ---
def load_db():
    if not os.path.exists(db_file_path):
        default_data = [{"username": "admin_candidate", "password": "SecurePassword123", "track": "Systems Architecture"}]
        with open(db_file_path, 'w') as f:
            json.dump(default_data, f, indent=4)
        return default_data
    with open(db_file_path, 'r') as f:
        return json.load(f)

def save_to_db(data):
    with open(db_file_path, 'w') as f:
        json.dump(data, f, indent=4)

billing_ledger = [
    {"token": "TXN-98231-LP", "desc": "Initial Admission Deposit Payment", "date": "January 12, 2026", "amount": "₦150,000", "status": "COMPLETED"},
    {"token": "TXN-99402-LP", "desc": "Mid-Term Academic Tuition Instalment", "date": "March 05, 2026", "amount": "₦150,000", "status": "COMPLETED"}
]

# --- PLATFORM ROUTES & LOGIC HANDLING ---

@app.route('/')
def index():
    error_flag = request.args.get('error')
    return render_template('index.html', error_message=error_flag)

@app.route('/dashboard')
def dashboard():
    current_user = request.args.get('username', 'Guest Candidate')
    current_track = request.args.get('track', 'Unassigned Track')
    return render_template('portal_core.html', username=current_user, track=current_track, billing=billing_ledger)

@app.route('/auth-login', methods=['POST'])
def auth_login():
    username = request.form.get('username')
    password = request.form.get('password')
    students_database = load_db()
    
    student = next((s for s in students_database if s['username'] == username and s['password'] == password), None)
    
    if student:
        return redirect(url_for('dashboard', username=student['username'], track=student['track']))
    else:
        return redirect(url_for('index', error="Authentication Failed: Invalid Username or Password credentials."))

@app.route('/register-student', methods=['POST'])
def register_student():
    reg_user = request.form.get('regUser')
    reg_email = request.form.get('regEmail')
    reg_pass = request.form.get('regPass')
    track = request.form.get('track')
    students_database = load_db()
    
    if any(s['username'] == reg_user for s in students_database):
        return redirect(url_for('index', error="Provisioning Error: Username is already allocated."))
    
    students_database.append({"username": reg_user, "email": reg_email, "password": reg_pass, "track": track})
    save_to_db(students_database)
    return redirect(url_for('index', error="Profile provisioned successfully! You can now log in."))

if __name__ == '__main__':
    app.run(port=3000, debug=True)
