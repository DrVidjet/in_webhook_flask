from flask import Flask, request, jsonify
import requests
import os
import configparser


CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'API.conf')
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

TARGET_URL = config.get('DEFAULT', 'TARGET_URL').strip('"')


app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook_proxy():
    try:
        data = request.get_json(force=True, silent=True)
        headers = {
            "Content-Type": "application/json"
        }

        r = requests.post(
            TARGET_URL,
            json=data,
            headers=headers,
            timeout=10
        )

        print("FORWARDED:", r.status_code, r.text)

        return jsonify({"status": "forwarded"}), 200

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"status": "error", "msg": str(e)}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
