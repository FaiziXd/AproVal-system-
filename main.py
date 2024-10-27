from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime, timedelta
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
        #approvalPanel, #waitMessage, #adminLogin, #approvalSection {
            display: none;
        }
        #visitPage {
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
        img {
            max-width: 100%;
            height: auto;
            margin: 20px 0;
        }
    </style>
</head>
<body>

    <div id="adminButton">🔑 Admin</div>

    <div id="approvalPanel">
        <h2>Send Approval</h2>
        <button class="button" id="sendApproval">Send Approval</button>
        <p id="keyMessage"></p>
        <p id="waitMessage">Approval already requested. Please wait for 3 months.</p>
        <img src="https://raw.githubusercontent.com/FaiziXd/AproVal-system-/refs/heads/main/28a4c2693dd79f14362193394aea0288.jpg" alt="Approval Page Image">
    </div>

    <div id="visitPage">
        <h2>Welcome! Your Approval is Accepted</h2>
        <p>Visit Your Own APK</p>
        <a href="https://herf-2-faizu-apk.onrender.com/" target="_blank" class="button">Visit</a>
        <img src="https://raw.githubusercontent.com/FaiziXd/AproVal-system-/refs/heads/main/130b4d853ec2cb9ed5f02d4072529908.jpg" alt="Visit Page Image">
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
        const approvalStorageKey = 'approvalTimestamp';
        const adminPassword = 'THE FAIZU';

        function checkApprovalEligibility() {
            const lastApprovalTimestamp = localStorage.getItem(approvalStorageKey);
            if (lastApprovalTimestamp) {
                const elapsedMonths = (Date.now() - lastApprovalTimestamp) / (1000 * 60 * 60 * 24 * 30);
                return elapsedMonths >= 3;
            }
            return true;
        }

        function setApprovalTimestamp() {
            localStorage.setItem(approvalStorageKey, Date.now());
        }

        function showApprovalPanel() {
            if (checkApprovalEligibility()) {
                document.getElementById('approvalPanel').style.display = 'block';
            } else {
                document.getElementById('visitPage').style.display = 'block';
            }
        }

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
                if (data.status === 'wait') {
                    document.getElementById('waitMessage').style.display = 'block';
                    document.getElementById('keyMessage').textContent = 'Your previously generated key: ' + data.key;
                } else {
                    document.getElementById('keyMessage').textContent = 'This is your key: ' + data.key;
                    alert('Please send this key to Faizan at: https://www.facebook.com/The.drugs.ft.chadwick.67');
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
                    setApprovalTimestamp();
                    document.getElementById('resultMessage').textContent = `Approval accepted for key: ${key}`;
                    document.getElementById('visitPage').style.display = 'block';
                    document.getElementById('approvalPanel').style.display = 'none';
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

        showApprovalPanel();
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
        last_request_time = datetime.fromisoformat(approval["timestamp"])

        # Calculate 3-month waiting period
        if approval["status"] == "approved" and current_time < last_request_time + timedelta(days=90):
            return jsonify({"status": "wait", "key": approval["key"]})

    # Generate new key
    unique_key = generate_unique_key()
    approvals[device_id] = {"status": "wait", "key": unique_key, "timestamp": current_time.isoformat()}
    save_approvals()

    return jsonify({"status": "new", "key": unique_key})

@app.route('/get_approvals', methods=['GET'])
def get_approvals():
    return jsonify({"approvals": [{"device_id": device_id, **details} for device_id, details in approvals.items()]})

@app.route('/admin_approve', methods=['POST'])
def admin_approve():
    data = request.json
    key = data.get('key')
    password = data.get('password')

    if password != adminPassword:
        return jsonify({"status": "error", "message": "Incorrect password."})

    # Find the device by key and approve
    for device_id, details in approvals.items():
        if details['key'] == key:
            details['status'] = 'approved'
            save_approvals()
            return jsonify({"status": "approved"})
    return jsonify({"status": "error", "message": "Key not found."})

@app.route('/admin_reject', methods=['POST'])
def admin_reject():
    data = request.json
    key = data.get('key')
    password = data.get('password')

    if password != adminPassword:
        return jsonify({"status": "error", "message": "Incorrect password."})

    # Find the device by key and reject
    for device_id in list(approvals.keys()):
        if approvals[device_id]['key'] == key:
            del approvals[device_id]
            save_approvals()
            return jsonify({"status": "rejected"})
    return jsonify({"status": "error", "message": "Key not found."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
            
