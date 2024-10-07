import unittest
from fastapi.testclient import TestClient
from main import app

class TestLLMAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_article_analyse(self):
        article = {
            "article": "This is a test article for analysis.",
            "language": "ENG"
        }
        response = self.client.post("/article_analyse", json=article)
        self.assertEqual(response.status_code, 200)
        self.assertIn("summary", response.json())

if __name__ == '__main__':
    unittest.main()
