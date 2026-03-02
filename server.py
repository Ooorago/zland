from flask import Flask, request, jsonify
import os

app = Flask(__name__)
pending = {}

@app.route("/")
def home():
    return "OAuth2 Server is Online"

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    print(f"[CALLBACK] code={code}, state={state}")
    pending[state] = code  # Store CODE not token
    return "<html><body><h2>Login successful! You can close this tab.</h2></body></html>"

@app.route("/poll")
def poll():
    state = request.args.get("state")
    code = pending.pop(state, None)
    print(f"[POLL] state={state}, found={'yes' if code else 'no'}")
    return jsonify({"code": code})

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
