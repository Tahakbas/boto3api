# Boto3 API

## Project Setup

 - Clone the project with `https://github.com/Tahakbas/boto3api.git`
 - Create virtual environment 
 - - For Linux `python3 -m venv env`
 - - For Windows `python -m venv env`
 - Active virtual environment
 - - For Linux `source <venv>/bin/activate`
 - - For Windows `<venv>\Scripts\Activate.ps1`
 - Create `config.py` and fill in the contents of this file like `example_config.py`
 ## Run
 - For Linux:
 - - `export FLASK_APP=<example.py>`
 - - `flask run`
 - For Windows:
 - - `set FLASK_APP=example.py`
 - - `$env:FLASK_APP = "example.py"`
 - - `flask run`
 ## Endpoints
 - Instances Id List
 - - Go to `http://<api_host>:<api_port>/ec2/list`
 - Instance's detail
 - - Go to `http://<api_host>:<api_port>/ec2/list/detail`
 - Start Instance
 - - Go to `http://<api_host>:<api_port>/ec2/start`
 - Stop Instance
 - - Go to ` http://<api_host>:<api_port>/ec2/stop`
