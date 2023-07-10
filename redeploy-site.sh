tmux kill-session
git fetch && git reset origin/main --hard
tmux new
source python3-virtualenv/bin/activate
pip install -r requirements.txt
flask run --host=0.0.0.0