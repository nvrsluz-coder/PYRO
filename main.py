from flask import Flask
import requests, os

app = Flask(__name__)

@app.route('/run')
def run():
    user_key = requests.post("https://pastebin.com/api/api_login.php", data={
        "api_dev_key": "B1wMYLw7-GZE8rFy_Pkpsjc6l6Pd_mge",
        "api_user_name": "Ilxom1991",
        "api_user_password": "Ilxom19910301"
    }).text
    
    code = requests.post("https://pastebin.com/api/api_raw.php", data={
        "api_dev_key": "B1wMYLw7-GZE8rFy_Pkpsjc6l6Pd_mge",
        "api_user_key": user_key,
        "api_option": "show_paste",
        "api_paste_key": "A9Ms1mU6"
    }).text
    
    return code

if __name__ == '__main__':
    app.run()