from flask import Flask, request, jsonify, render_template_string
import json
import os
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

# Generate a unique 8-digit key
def generate_unique_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

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
        #approvalPanel, #waitMessage, #adminLogin, #approvalSection, #visitPage {
            display: none;
        }
        img {
            max-width: 100%;
            height: auto;
            margin: 20px 0;
        }
    </style>
</head>
<body>

    <div id="approvalPanel">
        <h2>Send Approval</h2>
        <button class="button" id="sendApproval">Send Approval</button>
        <p id="keyMessage"></p>
        <p id="waitMessage">Approval already requested. Please wait for 3 months.</p>
        <p>Contact for queries: <a href="https://www.facebook.com/The.drugs.ft.chadwick.67" style="color: yellow;">Contact Me</a></p>
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
        <input type="text" id="approvalKey" placeholder="Enter Key to Approve/Reject">
        <button class="button" id="approveButton">Approve</button>
        <button class="button" id="rejectButton">Reject</button>
        <p id="resultMessage"></p>
    </div>

    <script>
        const adminPassword = 'THE FAIZU';

        function showApprovalPanel() {
            document.getElementById('approvalPanel').style.display = 'block';
        }

        document.getElementById('sendApproval').addEventListener('click', function() {
            const deviceId = navigator.userAgent;
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
                if (approvals[key].status === 'wait') {
                    const listItem = document.createElement('li');
                    listItem.textContent = `Device ID: ${key} - Key: ${approvals[key].key}`;
                    requestList.appendChild(listItem);
                }
            }
        }

        document.getElementById('approveButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            for (const deviceId in approvals) {
                if (approvals[deviceId].key === key && approvals[deviceId].status === 'wait') {
                    approvals[deviceId].status = 'approved';
                    document.getElementById('resultMessage').textContent = `Approval accepted for key: ${key}`;
                    alert('Approval accepted');
                    displayPendingApprovals();
                    document.getElementById('visitPage').style.display = 'block';
                    return;
                }
            }
            alert('Enter a valid key');
        });

        document.getElementById('rejectButton').addEventListener('click', function() {
            const key = document.getElementById('approvalKey').value;
            for (const deviceId in approvals) {
                if (approvals[deviceId].key === key) {
                    approvals[deviceId].status = 'rejected';
                    document.getElementById('resultMessage').textContent = `Approval rejected for key: ${key}`;
                    alert('Approval rejected');
                    displayPendingApprovals();
                    return;
                }
            }
            alert('Enter a valid key');
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

    if device_id in approvals:
        if approvals[device_id]['status'] == 'wait':
            return jsonify({"status": "wait", "key": approvals[device_id]['key']})

    unique_key = generate_unique_key()
    approvals[device_id] = {"status": "wait", "key": unique_key}

    with open(APPROVALS_FILE, 'w') as f:
        json.dump(approvals, f)

    return jsonify({"status": "new", "key": unique_key})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
        
