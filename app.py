from flask import Flask, request, render_template, send_from_directory, jsonify
from peewee import *
import os
import datetime
from playhouse.shortcuts import model_to_dict

app = Flask(__name__)

mydb = MySQLDatabase(os.getenv("MYSQL_DATABASE"),
       user=os.getenv("MYSQL_USER"),
       password=os.getenv("MYSQL_PASSWORD"),
       host=os.getenv("MYSQL_HOST"),
       port=3306
)

print(mydb)

# Peewee saves us the trouble of creating tables manually; we just need a class and the table would be created
# ORM model
class TimelinePost(Model):
    name = CharField()
    email = CharField()
    content = TextField()
    created_at = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        database = mydb

mydb.connect()
mydb.create_tables([TimelinePost])

# Endpoint to save and retrieve all our timeline posts
# POST route to add new timeline
@app.route('/api/timeline_post', methods=['POST'])
def postTimelinePost():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    timeline_post = TimelinePost.create(name=name, email=email, content=content)

    return model_to_dict(timeline_post)

@app.route('/api/timeline_post', methods=['GET'])
def getTimelinePost():
    return {
        'timeline_posts': [
            model_to_dict(p)
            for p in 
TimelinePost.select().order_by(TimelinePost.created_at.desc())
        ]
    }

from flask import jsonify
from peewee import DoesNotExist

@app.route('/api/timeline_post', methods=['DELETE'])
def deleteTimelinePosts():
    try:    
        # Delete all timeline posts
        TimelinePost.delete().execute()

        return jsonify({'status': 'success', 'message': 'All timeline posts deleted successfully'})
    except DoesNotExist:
        return jsonify({'status': 'error', 'message': 'No timeline posts found'})   


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