tmux kill-session
git fetch && git reset origin/main --hard
tmux new
tmux send-keys "source python3-virtualenv/bin/activate" Enter
tmux send-keys "pip install -r requirements.txt" Enter
tmux send-keys "flask run --host=0.0.0.0" Enter