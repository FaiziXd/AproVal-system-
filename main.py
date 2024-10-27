from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime
import random
import string

app = Flask(__name__)

# File to store approval requests
APPROVALS_FILE = 'approvals.json'

# Load existing approvals
if os.path.exists(APPROVALS_FILE):
    with open(APPROVALS_FILE, 'r') as f:
        approvals = json.load(f)
else:
    approvals = {}

# Function to generate a unique 7-digit key
def generate_unique_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=7))

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Approval System</title>
    <style>
        body {
            background-color: black;
            color: white;
            text-align: center;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .button {
            background-color: red;
            color: white;
            border: none;
            padding: 10px 20px;
            cursor: pointer;
            font-size: 16px;
            text-decoration: none;
            margin: 10px;
        }
        #approvalPanel, #visitPage, #adminLogin, #approvalSection {
            display: none;
        }
        #adminButton {
            position: fixed;
            top: 10px;
            right: 10px;
            font-size: 20px;
            color: white;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <div id="adminButton">🔑 Admin</div>

    <div id="approvalPanel">
        <h2>Send Approval</h2>
        <img src="https://github.com/FaiziXd/AproVal-system-/blob/main/28a4c2693dd79f14362193394aea0288.jpg" alt="Approval Page" style="max-width: 100%; height: auto;">
        <button class="button" id="sendApproval">Send Approval</button>
        <p id="keyMessage"></p>
        <p id="waitMessage">Approval already requested. Please wait for 3 months.</p>
    </div>

    <div id="visitPage">
        <h2>Welcome! Your Approval is Accepted. Now Visit</h2>
        <img src="https://github.com/FaiziXd/AproVal-system-/blob/main/130b4d853ec2cb9ed5f02d4072529908.jpg" alt="Visit Page" style="max-width: 100%; height: auto;">
        <a href="https://herf-2-faizu-apk.onrender.com/" target="_blank" class="button">Visit</a>
    </div>

    <div id="adminLogin">
        <h2>Admin Panel - Login</h2>
        <input type="password" id="adminPassword" placeholder="Enter Admin Password">
        <button class="button" id="loginButton">Login</button>
    </div>

    <div id="approvalSection">
        <h2>Approval Requests</h2>
        <ul id="requestList"></ul>
        <input type="text" id="approvalKey" placeholder="Enter Key to Approve">
        <button class="button" id="approveButton">Approve</button>
        <button class="button" id="rejectButton">Reject</button>
        <p id="resultMessage"></p>
    </div>

    <script>
        const adminPassword = 'THE FAIZU';

        document.getElementById('sendApproval').addEventListener('click', function() {
            const deviceId = navigator.userAgent;  // Simple device identification
            fetch('/send_approval', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ device_id: deviceId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'new') {
                    document.getElementById('keyMessage').textContent = 'This is your key: ' + data.key;
                    alert('Please send this key to Faizan at: https://www.facebook.com/The.drugs.ft.chadwick.67');
                } else {
                    document.getElementById('waitMessage').style.display = 'block';
                    document.getElementById('keyMessage').textContent = 'Your previously generated key: ' + data.key;
                }
            });
        });

        document.getElementById('adminButton').addEventListener('click', function() {
            document.getElementById('adminLogin').style.display = 'block';
        });

        document.getElementById('loginButton').addEventListener('click', function() {
            const enteredPassword = document.getElementById('adminPassword').value;
            if (enteredPassword === adminPassword) {
                document.getElementById('approvalSection').style.display = 'block';
                document.getElementById('adminLogin').style.display = 'none';
                displayPendingApprovals();
            } else {
                alert('Incorrect Password');
            }
        });

        function displayPendingApprovals() {
            const requestList = document.getElementById('requestList');
            requestList.innerHTML = '';
            fetch('/get_approvals')
            .then(response => response.json())
            .then(data => {
                data.approvals.forEach(approval => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `Device ID: ${approval.device_id} - Key: ${approval.key}`;
                    requestList.appendChild(listItem);
                });
            });
        }

        document.getElementById('approveButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            fetch('/admin_approve', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ key, password: adminPassword }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'approved') {
                    document.getElementById('visitPage').style.display = 'block';
                    document.getElementById('approvalPanel').style.display = 'none';
                    document.getElementById('keyMessage').textContent = '';
                    document.getElementById('resultMessage').textContent = `Approval accepted for key: ${key}`;
                    displayPendingApprovals();
                } else {
                    alert(data.message);
                }
            });
        });

        document.getElementById('rejectButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            fetch('/admin_reject', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ key, password: adminPassword }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'rejected') {
                    document.getElementById('resultMessage').textContent = `Approval rejected for key: ${key}`;
                    displayPendingApprovals();
                } else {
                    alert(data.message);
                }
            });
        });

        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('approvalPanel').style.display = 'block';
        });
    </script>
</body>
</html>
'''

def save_approvals():
    with open(APPROVALS_FILE, 'w') as f:
        json.dump(approvals, f)

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    device_id = data.get('device_id')
    current_time = datetime.now()

    # Check if device already requested approval
    if device_id in approvals:
        approval = approvals[device_id]
        return jsonify({"status": "wait", "key": approval["key"]})

    # Generate new unique key
    unique_key = generate_unique_key()
    approvals[device_id] = {"status": "wait", "key": unique_key, "timestamp": current_time.isoformat()}
    save_approvals()

    return jsonify({"status": "new", "key": unique_key})

@app.route('/get_approvals', methods=['GET'])
def get_approvals():
    pending_approvals = [{"device_id": device_id, "key": approval["key"]} for device_id, approval in approvals.items() if approval["status"] == "wait"]
    return jsonify({"approvals": pending_approvals})

@app.route('/admin_approve', methods=['POST'])
def admin_approve():
    data = request.json
    admin_password = data.get("password")
    key_to_approve = data.get("key")

    if admin_password != 'THE FAIZU':
        return jsonify({"status": "error", "message": "Incorrect admin password."})

    # Approve key
    for device_id, approval in approvals.items():
        if approval["key"] == key_to_approve:
            approval["status"] = "approved"
            save_approvals()
            return jsonify({"status": "approved", "message": f"Approval accepted for key: {key_to_approve}"})

    return jsonify({"status": "error", "message": "Key not found or already approved."})

@app.route('/admin_reject', methods=['POST'])
def admin_reject():
    data = request.json
    admin_password = data.get("password")
    key_to_reject = data.get("key")

    if admin_password != 'THE FAIZU':
        return jsonify({"status": "error", "message": "Incorrect admin password."})

    # Reject key
    for device_id, approval in approvals.items():
        if approval["key"] == key_to_reject:
            approval["status"] = "rejected"
            save_approvals()
            return jsonify({"status": "rejected", "message": f"Approval rejected for key: {key_to_reject}"})

    return jsonify({"status": "error", "message": "Key not found."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
    
