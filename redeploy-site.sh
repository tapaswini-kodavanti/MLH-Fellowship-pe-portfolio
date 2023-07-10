tmux kill-session
git fetch && git reset origin/main --hard
tmux new-session -s my_session -d
tmux send-keys -t my_session "source python3-virtualenv/bin/activate" Enter
tmux send-keys -t my_session "pip install -r requirements.txt" Enter
tmux send-keys -t my_session "flask run --host=0.0.0.0" Enter