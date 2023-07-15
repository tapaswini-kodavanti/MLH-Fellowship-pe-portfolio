from flask import Flask, redirect, render_template, send_from_directory, request
from peewee import *
from playhouse.shortcuts import model_to_dict
import os
import datetime

app = Flask(__name__)

mydb = MySQLDatabase(
    os.getenv("MYSQL_DATABASE"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    host = os.getenv("MYSQL_HOST"),
    port = 3306
)

print(mydb)

class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = mydb
mydb.connect()
mydb.create_tables([TimelinePost])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/places_visited')
def places_visited():
    return render_template('places_visited.html')


@app.route('/assets/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

# @app.route('/api/timeline_post', methods=['DELETE'])
# def delete_time_line_post():
#     return None
@app.route('/api/timeline_post/<int:post_id>', methods=['DELETE'])
def delete_timeline_post(post_id):
    try:
        timeline_post = TimelinePost.get_by_id(post_id)
        timeline_post.delete_instance()
        return {'message': 'Post deleted successfully'}
    except TimelinePost.DoesNotExist:
        return {'error': 'Post not found'}

if __name__ == '__main__':
    app.run(debug=True)
#host='0.0.0.0',port=5000