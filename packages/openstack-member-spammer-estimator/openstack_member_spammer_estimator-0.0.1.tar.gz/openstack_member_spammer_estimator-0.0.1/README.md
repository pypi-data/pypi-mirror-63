## Dependencies 

sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools sebastian+1tipit.net'

sudo apt install python3-venv

## Virtual Env

python3.6 -m venv env

source env/bin/activate

pip install -r requirements.txt 

pip freeze > requirements.txt