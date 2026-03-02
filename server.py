from flask import Flask, request, jsonify
import requests, uuid, os

app = Flask(__name__)
pending = {}

CLIENT_ID = os.getenv("CLIENT_ID", "1478005449155674134")
CLIENT_SECRET = os.getenv("CLIENT_SECRET", "ABirG5lgEpO1DC8ncvU6sYUq_RCQr75f")
REDIRECT_URI = "https://zland-oauth.onrender.com/callback"

@app.route("/")
def home():
    return "OAuth2 Server is Online"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    
    print(f"[CALLBACK] code={code}, state={state}")
    
    r = requests.post("https://discord.com/api/oauth2/token", data={
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
    })
    
    data = r.json()
    print(f"[DISCORD RESPONSE] {data}")  # This will show the error!
    
    token = data.get("access_token", "")
    if token:
        pending[state] = token
        print(f"[SUCCESS] Token stored for state={state}")
    else:
        print(f"[ERROR] No token received: {data}")
    
    return "<html><body><h2>Login successful! You can close this tab.</h2></body></html>"

@app.route("/poll")
def poll():
    state = request.args.get("state")
    print(f"[POLL] state={state}, pending keys={list(pending.keys())}")
    token = pending.pop(state, None)
    return jsonify({"token": token})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
