from time import sleep
import json5
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_login import login_required, LoginManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire import webdriver
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, request
import os

absolute_path = os.path.dirname(__file__)
relative_path = "index.html"
full_path = os.path.join(absolute_path, relative_path)
print(full_path)

class BankTest:

    def __init__(self):
        self.browser = None
        self.url = f"file://{full_path}"
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless')

    def wait_until_element_available(self, element):
        try:
            return WebDriverWait(self.browser, 15).until(
                EC.visibility_of_element_located(element))
        except Exception as e:
            return e

    def bank_test_automation(self, ref_id):
        bank_test_load = (By.XPATH, "// h2[contains(text(), 'درگاه تست')]")
        bank_test_code = (By.XPATH, "//code")
        submit_form = (By.XPATH, "//*[@type='submit']")
        self.browser = webdriver.Chrome(options=self.options)
        self.browser.get(self.url)
        self.browser.execute_script(f"document.getElementById('RefId').value = '{ref_id}'")
        self.wait_until_element_available(submit_form).click()
        self.wait_until_element_available(bank_test_load)
        self.browser.find_element(By.XPATH, "//*[@type='submit']").click()
        response_code = self.browser.find_element(*bank_test_code).text.replace('"CardHolderPan"', ',"CardHolderPan"')
        print(response_code)
        self.browser.quit()
        response_json = json5.loads(response_code)
        if response_json.get(""):
            response_json["RefId"] = response_json[""]
            del response_json[""]
        return response_json


# BankTest().bank_test_automation(ref_id="data")

app = Flask(__name__)
app.config["DEBUG"] = 'True'
app.config["TRACE_LOG"] = 'True'
auth = HTTPBasicAuth()
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Login Successfully"
app.secret_key = 'some_secret'
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@login_manager.user_loader
def load_user(username, password):
    if username == 'mshokri' and password == 123:
        return 1
    return 2


@auth.verify_password
def verify_password(username, password):
    if username == 'mshokri' and password == 123:
        return 1
    return 2


@app.route('/login', methods=['GET', 'POST'])
def login():
    return True


@app.route('/bank_test', methods=['POST'])
def bank_test():
    data = request.get_json()
    print(data)
    response = BankTest().bank_test_automation(data['ref_id'])
    return response


app.run(port=5080, debug=True)
