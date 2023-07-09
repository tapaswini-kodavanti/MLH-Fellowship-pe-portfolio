#!/bin/bash

tmux kill-session

cd /root/portfolio-site

git fetch && git reset origin/main --hard

source python3venv/bin/activate


pip install -r requirements.txt

tmux new-session -d -s portfolio-site 'cd /root/portfolio-site && source python3venv/bin/activate && flask run --host=0.0.0.0'



