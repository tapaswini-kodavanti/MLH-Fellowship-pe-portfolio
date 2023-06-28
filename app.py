from flask import Flask, redirect, render_template, send_from_directory


app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/places_visited')
def places_visited():
    return render_template('places_visited.html')


@app.route('/assets/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)




if __name__ == '__main__':
    app.run(debug=True)