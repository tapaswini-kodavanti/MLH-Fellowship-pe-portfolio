import unittest
from peewee import *

from app import TimelinePost


MODELS = [TimelinePost]

test_db = SqliteDatabase(':memory:')

class TestTimelinePost(unittest.TestCase):
    def setUp(self):
        # Bind model classes to test db. Since we have a complete list of
        # all models, we do not need to recursively bind dependencies
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

        test_db.connect()
        test_db.create_tables(MODELS)

    def tearDown(self):
        # Not strictly necessary since SQLite in-memory databases only live
        # for the duration of the connection, and in the next step, we close 
        # the connection...but a good practice

        test_db.drop_tables(MODELS)

        # Close the connection to db
        test_db.close()

    
    def test_timeline_post(self):
        # Create 2 timeline posts
        first_post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello World, I\'m John')
        assert first_post.id == 1
        second_post = TimelinePost.create(name='Jane Doe', email='jane@example.com', content='Hello World, I\'m Jane')
        assert second_post.id == 2

    def test_timeline_get(self):
            post = TimelinePost.create(name='John Doe', email='john@example.com', content='Hello World, I\'m John')

            # Get by ID
            get_post = TimelinePost.get_by_id(post.id)

            # Assertions for retrieved post
            self.assertEqual(get_post.name, 'John Doe')
            self.assertEqual(get_post.email, 'john@example.com')
            self.assertEqual(get_post.content, 'Hello World, I\'m John')







