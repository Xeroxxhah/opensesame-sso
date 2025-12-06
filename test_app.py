from flask import Flask, request, jsonify
import jwt
import json
app = Flask(__name__)

SECRET_KEY = "r4DmvbFj8ZkL9DkYBQ8J2kkFXlOHOtPDP2BSHzfGDiI4qRTllPGIClZj5mO3jaf1XxTjgMrPTFTJ_VHEN3BGtr7Xj3cAtrCwJUB6A-o1M23CzGasvs6t9O08"  # Same as used by SSO server
last_token = None  # Just for demo storage

@app.route("/sso/callback", methods=["POST", "GET"])
def sso_callback():
    global last_token

    if request.method == "POST":
        tokens = request.form.get("tokens")

        json_tokens = json.loads(tokens) 
        access_token = json_tokens.get('access')
        print(f"[POST] Received tokens: {tokens}")

        # Verify JWT
        try:
            payload = jwt.decode(access_token, SECRET_KEY, algorithms=["HS256"])
            print("Decoded JWT payload:", payload)
        except jwt.PyJWTError as e:
            return jsonify({"status": "error", "message": str(e)}), 400

        return jsonify({"status": "ok", "message": "Token received"})

    else:  # GET request (browser redirect after server POST)
        if not last_token:
            return "No token received yet", 400

        return f"""
        <html>
          <body>
            <h2>SSO Complete</h2>
            <p>Token: {last_token}</p>
          </body>
        </html>
        """


if __name__ == "__main__":
    app.run(port=5000, debug=True)
