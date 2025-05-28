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

@app.route("/protected")
def protected():
    if "user" not in session:
        return redirect("/login")
    return render_template("protected.html", user=session["user"])

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=3000)
