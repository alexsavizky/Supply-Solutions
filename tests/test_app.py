# import unittest
# from unittest import mock
# from app import app
#
#
# class TestApp(unittest.TestCase):
#
#     def setUp(self):
#         app.testing = True
#         self.app = app.test_client()
#
#     def test_register_not_successful(self):
#         with mock.patch('app.register') as mock_register_user:
#             mock_register_user.return_value = False
#             response = self.app.post('/register', data=dict(email='testuser@test.com', password='testpassword', firstname='shpih', Last_name='sagol'))
#             self.assertEqual(response.status_code, 200)
#             self.assertIn(b'register not successful', response.data)
#
#     def test_login_successful(self):
#         response = self.app.post('/login', data=dict(email='testuser@test.com', password='testpassword'))
#         self.assertEqual(response.status_code, 200)
#         self.assertIn(b'Login successful', response.data)
#
#     def test_login_invalid_credentials(self):
#         with mock.patch('app.login') as mock_authenticate_user:
#             mock_authenticate_user.return_value = False
#             response = self.app.post('/login', data=dict(email='testuser@test.com', password='invalidpassword'))
#             self.assertEqual(response.status_code, 200)
#             self.assertIn(b'Invalid username or password', response.data)
#
#
# if __name__ == '__main__':
#     unittest.main()
