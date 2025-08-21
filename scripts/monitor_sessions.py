import json
import os
import time
import psutil
from datetime import datetime

SESSIONS_FILE = os.path.join(os.path.dirname(__file__), '../config/sessions.json')

def load_sessions():
    if not os.path.exists(SESSIONS_FILE):
        return []
    with open(SESSIONS_FILE, 'r') as f:
        return json.load(f)

def save_sessions(sessions):
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(sessions, f, indent=4)

def check_session_status(session):
    pid = session.get('pid')
    if pid:
        if psutil.pid_exists(pid):
            session['status'] = 'active'
            session['last_seen'] = datetime.now().isoformat()
        else:
            session['status'] = 'inactive'
            # Optionally, add logic for recovery here
    else:
        session['status'] = 'unknown' # No PID to check
    return session

def monitor_sessions():
    print(f"[{datetime.now().isoformat()}] Starting session monitoring...")
    sessions = load_sessions()
    updated_sessions = []
    for session in sessions:
        updated_sessions.append(check_session_status(session))
    save_sessions(updated_sessions)
    print(f"[{datetime.now().isoformat()}] Session monitoring completed.")

if __name__ == "__main__":
    monitor_sessions()
