"""
Python test module for testing that django-admin startproject worked or not
"""
from django.test import TestCase, Client


class ProjectTest(TestCase):

    def test_server(self):
        """Test wether the server is working or not."""
        client = Client()
        response = client.get("/admin")
        self.assertEqual(response.status_code, 301)
