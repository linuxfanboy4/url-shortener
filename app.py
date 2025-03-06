from flask import Flask, request, redirect, render_template_string, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
import qrcode
from io import BytesIO
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls3.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(500), nullable=False)
    short_url = db.Column(db.String(20), unique=True, nullable=False)
    clicks = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    qr_code = db.Column(db.LargeBinary)

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route("/", methods=["GET", "POST"])
def home():
    error = None
    success = None
    if request.method == "POST":
        original_url = request.form['original_url']
        option = request.form['option']
        custom_alias = request.form.get('custom_alias', '').strip()

        if not re.match(r'^https?://\S+', original_url):
            error = "Please enter a valid URL starting with http:// or https://"
        else:
            if option == 'custom':
                if not custom_alias:
                    error = "Custom alias is required"
                elif not re.match(r'^[a-zA-Z0-9_-]{4,20}$', custom_alias):
                    error = "Use 4-20 characters (letters, numbers, _-)"
                elif URL.query.filter_by(short_url=custom_alias).first():
                    error = "Custom alias already exists"
                else:
                    short_url = custom_alias
            else:
                length = int(request.form['length'])
                short_url = generate_random_string(length)
                while URL.query.filter_by(short_url=short_url).first():
                    short_url = generate_random_string(length)

            if not error:
                new_url = URL(original_url=original_url, short_url=short_url)
                db.session.add(new_url)
                db.session.commit()
                success = short_url

    return render_template_string(TEMPLATE, error=error, success=success)

@app.route("/<short_url>")
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    url.clicks += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route("/stats")
def stats():
    urls = URL.query.order_by(URL.created_at.desc()).all()
    return render_template_string(STATS_TEMPLATE, urls=urls)

@app.route("/qr/<short_url>")
def generate_qr(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    qr = qrcode.make(request.url_root + short_url)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quantum Link</title>
    <style>
        :root {
            --primary: #7c3aed;
            --secondary: #6366f1;
            --glass: rgba(255, 255, 255, 0.05);
            --text: rgba(255, 255, 255, 0.9);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Inter', sans-serif;
        }

        body {
            background: linear-gradient(45deg, #0f172a, #1e293b);
            min-height: 100vh;
            color: var(--text);
            display: grid;
            place-items: center;
            padding: 1rem;
        }

        .container {
            background: var(--glass);
            backdrop-filter: blur(12px);
            border-radius: 1.5rem;
            padding: 2.5rem;
            width: 100%;
            max-width: 600px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        h1 {
            text-align: center;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 2rem;
            font-size: 2.5rem;
        }

        .toggle-group {
            display: flex;
            gap: 1rem;
            margin: 1rem 0;
        }

        .toggle-btn {
            flex: 1;
            padding: 0.75rem;
            border: none;
            border-radius: 0.75rem;
            background: var(--glass);
            color: var(--text);
            cursor: pointer;
            transition: all 0.3s ease;
        }

        .toggle-btn.active {
            background: linear-gradient(to right, var(--primary), var(--secondary));
            box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
        }

        input, select {
            width: 100%;
            padding: 1rem;
            margin: 0.5rem 0;
            border: none;
            border-radius: 0.75rem;
            background: var(--glass);
            color: var(--text);
            font-size: 1rem;
            transition: all 0.3s ease;
        }

        input:focus, select:focus {
            outline: none;
            box-shadow: 0 0 0 2px var(--primary);
        }

        button[type="submit"] {
            width: 100%;
            padding: 1rem;
            margin: 1rem 0;
            border: none;
            border-radius: 0.75rem;
            background: linear-gradient(to right, var(--primary), var(--secondary));
            color: white;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s ease;
        }

        button[type="submit"]:hover {
            transform: translateY(-2px);
        }

        .result {
            margin-top: 2rem;
            text-align: center;
            animation: fadeIn 0.5s ease;
        }

        .qr-code {
            margin: 2rem auto;
            padding: 1rem;
            background: white;
            border-radius: 1rem;
            width: fit-content;
        }

        .stats-link {
            display: block;
            text-align: center;
            margin-top: 2rem;
            color: var(--text);
            text-decoration: none;
            opacity: 0.8;
            transition: opacity 0.3s ease;
        }

        .stats-link:hover {
            opacity: 1;
        }

        .error {
            color: #ef4444;
            margin: 1rem 0;
            text-align: center;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @media (max-width: 600px) {
            .container {
                padding: 1.5rem;
                border-radius: 1rem;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
    <script>
        function toggleOption(selected) {
            document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
            document.getElementById(selected + '-btn').classList.add('active');
            document.getElementById('custom-alias').style.display = selected === 'custom' ? 'block' : 'none';
            document.getElementById('length').style.display = selected === 'random' ? 'block' : 'none';
        }

        function copyToClipboard() {
            const url = `{{ request.url_root }}${'{{ success }}'}`;
            navigator.clipboard.writeText(url);
            alert('URL copied to clipboard!');
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>🔗 Quantum Link</h1>
        
        {% if error %}
            <div class="error">{{ error }}</div>
        {% endif %}

        <form method="POST">
            <input type="url" name="original_url" placeholder="https://example.com" required>
            
            <div class="toggle-group">
                <button type="button" id="random-btn" class="toggle-btn active" onclick="toggleOption('random')">Random</button>
                <button type="button" id="custom-btn" class="toggle-btn" onclick="toggleOption('custom')">Custom</button>
            </div>

            <div id="custom-alias" style="display: none;">
                <input type="text" name="custom_alias" placeholder="my-custom-alias">
            </div>

            <div id="length">
                <select name="length">
                    <option value="6">6 Characters</option>
                    <option value="8">8 Characters</option>
                    <option value="10">10 Characters</option>
                </select>
            </div>

            <button type="submit">Create Short URL</button>
        </form>

        {% if success %}
            <div class="result">
                <p>Short URL created:</p>
                <h3>{{ request.url_root }}{{ success }}</h3>
                <button onclick="copyToClipboard()" style="margin-top: 1rem;">Copy URL</button>
                <div class="qr-code">
                    <img src="{{ url_for('generate_qr', short_url=success) }}" alt="QR Code">
                </div>
            </div>
        {% endif %}

        <a href="{{ url_for('stats') }}" class="stats-link">View Advanced Analytics →</a>
    </div>
</body>
</html>
"""

STATS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Analytics Dashboard</title>
    <style>
        body {
            background: linear-gradient(45deg, #0f172a, #1e293b);
            color: rgba(255, 255, 255, 0.9);
            padding: 2rem;
            font-family: 'Inter', sans-serif;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        h1 {
            text-align: center;
            margin-bottom: 2rem;
            background: linear-gradient(to right, #7c3aed, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border-radius: 1rem;
            overflow: hidden;
        }

        th, td {
            padding: 1rem;
            text-align: left;
        }

        th {
            background: linear-gradient(to right, #7c3aed, #6366f1);
            color: white;
        }

        tr:nth-child(even) {
            background: rgba(255, 255, 255, 0.02);
        }

        tr:hover {
            background: rgba(255, 255, 255, 0.08);
        }

        .back-btn {
            display: inline-block;
            margin: 2rem 0;
            padding: 0.75rem 1.5rem;
            background: linear-gradient(to right, #7c3aed, #6366f1);
            color: white;
            text-decoration: none;
            border-radius: 0.75rem;
            transition: transform 0.2s ease;
        }

        .back-btn:hover {
            transform: translateY(-2px);
        }

        .click-count {
            font-weight: bold;
            color: #7c3aed;
        }

        @media (max-width: 768px) {
            table {
                display: block;
                overflow-x: auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Analytics Dashboard</h1>
        <table>
            <thead>
                <tr>
                    <th>Short URL</th>
                    <th>Original URL</th>
                    <th>Clicks</th>
                    <th>Created At</th>
                </tr>
            </thead>
            <tbody>
                {% for url in urls %}
                <tr>
                    <td><a href="{{ url_for('redirect_to_url', short_url=url.short_url) }}" style="color: #7c3aed;">{{ url.short_url }}</a></td>
                    <td style="max-width: 400px; overflow: hidden; text-overflow: ellipsis;">{{ url.original_url }}</td>
                    <td class="click-count">{{ url.clicks }}</td>
                    <td>{{ url.created_at.strftime('%Y-%m-%d %H:%M') }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        <a href="{{ url_for('home') }}" class="back-btn">← Back to Shortener</a>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
