import unittest
import os
os.environ['TESTING'] = 'true'

from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "<title>MLH Fellow</title>" in html
        assert '<div class="divider-custom divider-light intro"></div>' in html
        assert '<img class="masthead-avatar mb-5" src="assets/img/logo.jpg" alt="..." />' in html
        assert '<li class="nav-item mx-0 mx-lg-1"><a class="nav-link py-3 px-0 px-lg-3 rounded" href="/places_visited">Extra</a></li>' in html
        assert '<button class="btn btn-primary btn-xl disabled" id="submitButton" type="submit">Send</button>' in html
    
   
    def test_timeline(self):
        response = self.client.get("/api/timeline_post")
        assert response.status_code == 200
        assert response.is_json
        json = response.get_json()
        assert "timeline_posts" in json
        assert json["timeline_posts"] == 0
    
    def test_timeline_post_valid(self):
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "jdoe@example.com", "content": "Hello, world!"})
        assert response.status_code == 200

        # Parse the JSON response
        json_response = response.get_json()
        assert "name" in json_response
        assert "email" in json_response
        assert "content" in json_response

        # Verify that the data in the response matches the data in the request
        self.assertEqual(json_response['name'], 'John Doe')
        self.assertEqual(json_response['email'], 'jdoe@example.com')
        self.assertEqual(json_response['content'], 'Hello, world!')
        


    def test_timeline_page(self):
        response = self.client.get("/timeline")
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        # Check if name, email, and content is set to required
        assert '<input class="form-control" name="name" id="name" type="text" placeholder="Enter your name..." required />' in html
        assert '<input class="form-control" name="email" id="email" type="email" placeholder="name@example.com" required />' in html
        assert '<textarea class="form-control" name="content" id="message" type="text" placeholder="Enter your content here..." style="height: 10rem" required></textarea>' in html


    def test_malformed_timeline_post(self):
        # POST request missing name
        response = self.client.post("/api/timeline_post", data={"email": "jdoe@ex.com", "content": "Hi, I\'m John Doe"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Name" in html

        # POST content empty container
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "jdoe@ex.com", "content": ""})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Content" in html

        # POST request with malformed email
        response = self.client.post("/api/timeline_post", data={"name": "John Doe", "email": "jdoe-ex-com", "content": "Hi, I\'m John Doe"})
        assert response.status_code == 400
        html = response.get_data(as_text=True)
        assert "Invalid Email" in html

    





