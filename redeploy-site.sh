#!/bin/bash


cd /root/portfolio-site

git fetch && git reset origin/main --hard

source python3venv/bin/activate


pip install -r requirements.txt

systemctl daemon-reload

systemctl restart myportfolio