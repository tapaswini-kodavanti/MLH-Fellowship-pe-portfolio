from flask import Flask, render_template, send_from_directory, request
from peewee import *
from playhouse.shortcuts import model_to_dict
from dotenv import load_dotenv
from data import data
import os
import datetime
import re

load_dotenv()

app = Flask(__name__)

if os.getenv("TESTING") == "true":
    print("Running in test mode")
    mydb = SqliteDatabase('file:memory?mode=memory&cache=shared', uri=True)
else:
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
    return render_template('index.html', data=data)


@app.route('/places_visited')
def places_visited():
    return render_template('places_visited.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')


@app.route('/app/static/assets/<path:path>')
def send_static(path):
    return send_from_directory('assets', path)

@app.route('/api/timeline_post', methods=['POST'])
def post_time_line_post():
    name = request.form.get('name')
    email = request.form.get('email')
    content = request.form.get('content')

    if not name:
        return {'error': 'Invalid Name'}, 400
    if not email:
        return {'error': 'Invalid Email'}, 400
    if not content:
        return {'error': 'Invalid Content'}, 400
    
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return {'error': 'Invalid Email: Please provide a valid email address.'}, 400

    
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def get_time_line_post():
   
    timeline_posts = [
        model_to_dict(p)
        for p in TimelinePost.select().order_by(TimelinePost.created_at.desc())
    ]

    if not timeline_posts:
        return {'timeline_posts': len(timeline_posts)}

    return {'timeline_posts': timeline_posts}
    
    
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