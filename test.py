import unittest
import requests

class WebhookTestCase(unittest.TestCase):
    def test_webhook(self):
        url = 'http://localhost:5000/webhook'
        data = {
                "sec_key":"12345",
                "ticker":"BTCUSDT",
                "action":"sell"
                }
        response = requests.post(url, json=data)

if __name__ == '__main__':
    unittest.main()
