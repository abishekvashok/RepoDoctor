# RepoDoctor

Repo Doctor is a web app that can be used to detect secuirty vulnerabilities in open source projects.

## Inspiration

Our inspiration comes from the fact that many static analyzers are not used by open source programmer because they are really hard to setup and often result in requiring significant changes to code. To bridge this gap and bring much more sense of security to open source projects, we build RepoDoctor. With RepoDoctor you can check repositories for a myriad of common vulnerabilities and get the findings delivered in a responsible and private manner to your inbox - all for free.
 
## Requirements

This project requires Python version 3.8 or higher.
Install python dependencies using:
```bash
pip install -r requirements.txt
```

## Setup

Setup a python virtual environment:
```bash
python -m venv ./venv
source ./venv/bin/activate
```

## Configuration

You need to edit `main.py` and provide in a username, password pair for the smtp client to send an email from. Also please be aware that you migh thave to lower
the security priveleges if you are trying to use your gmail username and password.

## Running the app

To run the app run:
```bash
python3 app.py
```


This will launch the flask app at the latest available port (starting from 5000) at your local system. eg) http://localhost:5000/

<img width="1440" alt="RepoDoctor working" src="https://user-images.githubusercontent.com/8947010/134706421-0d7b4010-a913-480f-b6f3-597679b6e609.png">

## What's next for RepoDoctor

We would like to add in support for more languages and support the broad open source communities out there. Another improvement we can think of would be to provide the user with recurrent jobs so that we could mail them results after each commit is made in the repository or PR.
