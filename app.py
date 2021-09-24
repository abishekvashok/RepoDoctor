from flask import Flask, render_template, request
from flask_executor import Executor
from pathlib import Path
from email.message import EmailMessage

import json
import os
import re
import shutil
import smtplib
import subprocess

app = Flask(__name__)
executor = Executor(app)
EMAIL_ADDRESS = "abi.next.io@gmail.com"
EMAIL_PASSWORD = ""

def email_user(email, message):
    msg = EmailMessage()
    msg['Subject'] = 'RepoDoctor repository static analysis results'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = email
    msg.set_content(f'''
        <!DOCTYPE html>
        <html>
            <body>
            {message}
            </body>
        </html>''', subtype='html')
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def scan_repo(email, url):
    try:
        subprocess.check_output(["git", "clone", url, "--depth=1"], timeout=20)
    except subprocess.CalledProcessError as e:
        code = str(e).split("status ")[1]
        print(code)
        if code == "128.": # Repo already exists, is scanning, skip
            return
        raise
    except subprocess.TimeoutExpired:
        # Repo url is incorrect, mail the error
        email_user(email, "The provided repository url was incorrect, please try again")
        return
    repo_dir = url.split("/")[4].split(".")[0]
    if not os.path.isdir(repo_dir):
        email_user(email, "The provided repository url is incorrect, please try again")
        return
    command = "pip install -r requirements.txt"
    os.environ["PYRE_TYPESHED"] = str(Path(os.getcwd()) / "typeshed")
    os.chdir(Path(__file__).parent / repo_dir)
    if os.path.isfile("requirements.txt"):
        subprocess.check_call(["bash", "-c", f"{command}"])
    command = "pip install pyre-check"
    subprocess.check_call(["bash", "-c", f"{command};"])
    if not os.path.isfile(".pyre_configuration"):
        subprocess.check_call(["bash", "-c", "printf 'n\n\n' | pyre init"])
    command = "pyre --noninteractive analyze --no-verify"
    out = subprocess.check_output(command.split(" "), text=False)
    os.chdir("../")
    shutil.rmtree(repo_dir)
    output = json.loads(out)
    if len(output) == 0:
        email_user(email, "Pyre found 0 vulnerabilties in your repository")
        return
    msg = "Pyre found the following vulnerabilties in your repository: "
    msg += str(out.decode("utf-8").replace("\n", "<br>"))
    email_user(email, msg)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/analyze_repository", methods=["POST"])
def analyze_repository():
    email = request.form["email"]
    url = request.form["url"]
    errors = []
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        errors.append("Please enter a valid email address")
    if any(errors):
        return render_template("error.html", errors=errors)
    executor.submit(scan_repo, email, url)
    return render_template("success.html", email=email)

app.run()
