import unittest
from myapp.app import app

class ArabicAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health(self):
        """Проверка эндпоинта health-check"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ok', response.data)

    def test_index_page(self):
        """Проверка главной страницы"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_metrics_page(self):
        """Проверка доступности метрик Prometheus"""
        response = self.app.get('/metrics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'http_requests_total', response.data)

    def test_add_word(self):
        """Проверка добавления слова через POST запрос"""
        response = self.app.post('/add', data=dict(arabic='kitab', translation='book'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'book', response.data)

if __name__ == '__main__':
    unittest.main()