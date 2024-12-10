from flask import Flask, request, render_template_string
import requests
import os
import time

app = Flask(__name__)
app.debug = True

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        # Logic remains unchanged
        pass

    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Faizu's Power Tool</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet">
  <style>
    body {
      background-color: #181818;
      color: #f5f5f5;
      font-family: 'Courier New', Courier, monospace;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
    }
    .header {
      background-image: url('https://raw.githubusercontent.com/FaiziXd/AproVal-System-here/refs/heads/main/7a1e91d3a04a6e4711668741990e9209.jpg');
      background-size: cover;
      background-position: center;
      color: white;
      padding: 70px 20px;
      text-align: center;
      box-shadow: 0 8px 15px rgba(0, 0, 0, 0.5);
    }
    .header h1 {
      font-size: 50px;
      text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.7);
    }
    .container {
      max-width: 500px;
      background: linear-gradient(145deg, #202020, #2a2a2a);
      border: 2px solid black;
      padding: 30px;
      margin: 30px auto;
      border-radius: 15px;
      box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.9);
    }
    label, select, input, .btn-submit {
      color: #f5f5f5;
    }
    label {
      font-size: 1.1rem;
      margin-bottom: 5px;
    }
    .form-control {
      background: #121212;
      border: none;
      padding: 10px;
      border-radius: 8px;
      margin-bottom: 15px;
    }
    .form-control:focus {
      outline: none;
      box-shadow: 0px 0px 5px rgba(255, 0, 0, 0.7);
    }
    .btn-submit {
      background: linear-gradient(to right, #ff0000, #cc0000);
      border: none;
      padding: 10px 15px;
      font-size: 1.2rem;
      font-weight: bold;
      text-transform: uppercase;
      border-radius: 8px;
      transition: all 0.3s ease;
    }
    .btn-submit:hover {
      background: linear-gradient(to right, #cc0000, #ff0000);
      transform: scale(1.05);
    }
    .footer {
      text-align: center;
      color: #aaa;
      margin: 20px 0;
    }
    .footer p {
      margin: 5px 0;
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    .header, .container, .footer {
      animation: fadeIn 1.5s ease-in-out;
    }
  </style>
</head>
<body>
  <header class="header">
    <h1>FAIZU'S TOOL 2.0</h1>
    <h2>🔥 UNSTOPPABLE SYSTEM 🔥</h2>
    <h3>OWNED BY THE FAIZU LEGACY</h3>
  </header>
  <div class="container">
    <form action="/" method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenType">Token Type</label>
        <select class="form-control" id="tokenType" name="tokenType" required>
          <option value="single">Single Token</option>
          <option value="multi">Multi Token</option>
        </select>
      </div>
      <div class="mb-3">
        <label for="accessToken">Your Token</label>
        <input type="text" class="form-control" id="accessToken" name="accessToken">
      </div>
      <div class="mb-3">
        <label for="threadId">Convo/Inbox ID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx">Hater Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3">
        <label for="txtFile">Message File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
      </div>
      <div class="mb-3" id="multiTokenFile" style="display: none;">
        <label for="tokenFile">Token File (Multi-Token)</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" accept=".txt">
      </div>
      <div class="mb-3">
        <label for="time">Speed (Seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <button type="submit" class="btn btn-submit">Start Messaging</button>
    </form>
  </div>
  <footer class="footer">
    <p>&copy; 2024 Faizu's Legacy. All Rights Reserved.</p>
    <p>"Power Beyond Limits"</p>
  </footer>
  <script>
    document.getElementById('tokenType').addEventListener('change', function() {
      var tokenType = this.value;
      document.getElementById('multiTokenFile').style.display = tokenType === 'multi' ? 'block' : 'none';
    });
  </script>
</body>
</html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True, use_reloader=True)
