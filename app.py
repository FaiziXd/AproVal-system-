from flask import Flask, request, jsonify, render_template_string
import json
import os
from datetime import datetime

app = Flask(__name__)

# File to store approval requests
APPROVALS_FILE = 'approvals.json'

# Load existing approvals
if os.path.exists(APPROVALS_FILE):
    with open(APPROVALS_FILE, 'r') as f:
        approvals = json.load(f)
else:
    approvals = {}

# HTML template (same as before)
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
        #approvalPanel, #waitMessage, #adminLogin, #approvalSection, #visitPage {
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
        <img src="https://github.com/FaiziXd/AproVal-system-/blob/main/130b4d853ec2cb9ed5f02d4072529908.jpg?raw=true" alt="Approval Image">
        <button class="button" id="sendApproval">Send Approval</button>
        <p id="keyMessage"></p>
        <p id="waitMessage">Approval already requested. Please wait for 3 months.</p>
    </div>

    <div id="visitPage">
        <img src="https://github.com/FaiziXd/AproVal-system-/blob/main/28a4c2693dd79f14362193394aea0288.jpg?raw=true" alt="Visit Image">
        <h2>Welcome Dear, Now Your Approval Accepted</h2>
        <p>Visit Your Own APK</p>
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

        showApprovalPanel();
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/send_approval', methods=['POST'])
def send_approval():
    data = request.json
    device_id = data.get('device_id')
    print(f"Received approval request from device ID: {device_id}")  # Debug statement

    # Check if this device has already requested approval
    if device_id in approvals:
        print(f"Device {device_id} already has status: {approvals[device_id]['status']}")  # Debug statement
        if approvals[device_id]['status'] == 'wait':
            return jsonify({"status": "wait", "key": approvals[device_id]['key']})

    # Generate a unique key for this device
    unique_key = f"KEY-{len(approvals) + 1}"
    approvals[device_id] = {"status": "wait", "key": unique_key}
    print(f"Generated new key for device {device_id}: {unique_key}")  # Debug statement

    # Save to JSON file
    with open(APPROVALS_FILE, 'w') as f:
        json.dump(approvals, f)  # Fixed JSON save issue here

    return jsonify({"status": "new", "key": unique_key})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)