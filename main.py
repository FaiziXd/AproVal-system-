from flask import Flask, render_template_string, request, jsonify
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)

# Load existing approvals if any
if os.path.exists('approvals.json'):
    with open('approvals.json', 'r') as f:
        approvals = json.load(f)
else:
    approvals = {}

# HTML Template
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
        #approvalMessage {
            display: none;
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
    </div>

    <div id="visitPage">
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
                    document.getElementById('keyMessage').textContent = 'This is your key: ' + data.key;
                } else {
                    document.getElementById('keyMessage').textContent = 'This is your key: ' + data.key;
                    alert('Please send this key to Faizan for approval.');
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
            for (const key in approvals) {
                const listItem = document.createElement('li');
                listItem.textContent = `Key: ${key} - Status: ${approvals[key].status}`;
                requestList.appendChild(listItem);
            }
        }

        document.getElementById('approveButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            if (key && approvals[key]) {
                approvals[key].status = 'approved';
                setApprovalTimestamp();
                document.getElementById('resultMessage').textContent = `Approval accepted for key: ${key}`;
                alert('Approval accepted');
                displayPendingApprovals();
            } else {
                alert('Enter a valid key');
            }
        });

        document.getElementById('rejectButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            if (key && approvals[key]) {
                approvals[key].status = 'rejected';
                document.getElementById('resultMessage').textContent = `Approval rejected for key: ${key}`;
                alert('Approval rejected');
                displayPendingApprovals();
            } else {
                alert('Enter a valid key');
            }
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
    device_id = request.json.get('device_id')

    if device_id in approvals:
        existing_approval = approvals[device_id]
        if datetime.now() < existing_approval['expiry']:
            return jsonify({"status": "wait", "key": existing_approval['key']})

    # Generate a new key and set approval
    unique_key = f"KEY-{os.urandom(4).hex().upper()}"
    approvals[device_id] = {
        "key": unique_key,
        "expiry": datetime.now() + timedelta(days=90)  # 3 months
        , "status": "pending"  # Add status to approvals
    }
    with open('approvals.json', 'w') as f:
        json.dump(approvals, f)

    return jsonify({"status": "success", "key": unique_key})

# Run the application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
