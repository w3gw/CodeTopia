
from django.test import TestCase, Client


class CoreViewTests(TestCase):

    def test_homepage(self):
        """test the index route"""
        client = Client()
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
