from flask import Flask, request, abort
import requests, os

app = Flask(__name__)

@app.route('/run')
def run():
    secret = request.headers.get("X-Secret")
    if secret != os.getenv("SECRET_TOKEN"):
        abort(403)

    api_dev_key = os.getenv("API_DEV_KEY")
    username = os.getenv("PASTEBIN_USERNAME")
    password = os.getenv("PASTEBIN_PASSWORD")
    paste_key = os.getenv("PASTE_KEY")

    user_key = requests.post("https://pastebin.com/api/api_login.php", data={
        "api_dev_key": api_dev_key,
        "api_user_name": username,
        "api_user_password": password
    }).text

    code = requests.post("https://pastebin.com/api/api_raw.php", data={
        "api_dev_key": api_dev_key,
        "api_user_key": user_key,
        "api_option": "show_paste",
        "api_paste_key": paste_key
    }).text

    return code

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
