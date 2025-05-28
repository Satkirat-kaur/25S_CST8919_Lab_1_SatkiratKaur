# CST8919 – Lab 1: Flask Authentication with Auth0

This lab demonstrates how to build a secure Python web application using Flask and Auth0 for authentication. Users can log in, view a protected dashboard, and log out securely.

---

## 🔧 Lab Setup & Environment

### ✅ Prerequisites

- Python
- Auth0 account (https://auth0.com)

---

## 1. Clone the Lab Repository

```bash
git clone https://github.com/ramymohamed10/25S_CST8919_Lab_1.git
cd 25S_CST8919_Lab_1
```
## 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # For Windows: venv\Scripts\activate
```
## 3. Install Dependencies

```bash
pip install -r requirements.txt
```
#### Make sure your requirements.txt includes:
- flask>=2.0.3
- python-dotenv>=0.19.2
- authlib>=1.0
- requests>=2.27.1

## 4. Set Up Auth0 Application

### a. Create Auth0 App

1. Go to [https://manage.auth0.com](https://manage.auth0.com)
2. Navigate to: **Applications → Create Application**
3. Choose **Regular Web Application**
4. Name your app: `FlaskAuthApp`

---

### b. Configure Auth0 Settings

Set the following values under your application's **Settings**:

#### **Allowed Callback URLs**
```bash
http://127.0.0.1:3000/callback
```
#### **Allowed Logout URLs**
```bash
http://localhost:3000
```
#### **Allowed Web Origins**
```bash
http://localhost:3000
```
#### Save Changes

## 5. Create `.env` File

In the root folder of your project, create a `.env` file and add the following environment variables:

```ini
AUTH0_CLIENT_ID=your_auth0_client_id
AUTH0_CLIENT_SECRET=your_auth0_client_secret
AUTH0_DOMAIN=your-tenant-name.us.auth0.com
APP_SECRET_KEY=your_random_secret_key
PORT=3000
```
#### You can generate a secure random APP_SECRET_KEY using the following command:

```bash
openssl rand -hex 32
```
## 6. Create `server.py` File

In your project root, create a file named `server.py` and add the following code:

```python
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv, find_dotenv
from flask import Flask, redirect, render_template, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)  # ✅ Fix here
app.secret_key = env.get("APP_SECRET_KEY")

oauth = OAuth(app)
oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={"scope": "openid profile email"},
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration'
)

@app.route("/")
def home():
    user = session.get("user")
    return render_template("home.html", user=user, pretty=json.dumps(user, indent=4))


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(redirect_uri=url_for("callback", _external=True))

@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token["userinfo"]  # ✅ Only store user info
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?" + urlencode({
            "returnTo": url_for("home", _external=True),
            "client_id": env.get("AUTH0_CLIENT_ID")
        }, quote_via=quote_plus)
    )
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("dashboard.html", user=session["user"])

@app.route("/protected")
def protected():
    if "user" not in session:
        return redirect("/login")
    return render_template("protected.html", user=session["user"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
```
## 7. Create HTML Templates

Create a `templates/` folder in your project root and add the following two HTML files:

---

### `templates/home.html`

```html
<html>
  <body>
    {% if user %}
        <h1>Welcome {{ user['name'] }}</h1>
        <a href="/protected">Go to Protected Page</a><br>
        <a href="/logout">Logout</a>
        <pre>{{ pretty }}</pre>
    {% else %}
        <h1>Welcome Guest</h1>
        <a href="/login">Login</a>
    {% endif %}
  </body>
</html>
```
### `templates/protected.html`

```html
<html>
  <body>
    <h1>Protected Page</h1>
    <p>Hello {{ user['name'] }}</p>
    <a href="/">Go Home</a><br>
    <a href="/logout">Logout</a>
  </body>
</html>
```
## 8. Run Flask App (if using `if __name__ == "__main__"`)

To start your Flask application, run the following command from your project root:

```bash
python server.py
```


## 9. Youtube video presentation link

(https://youtu.be/x4pFwuO0VnM)



