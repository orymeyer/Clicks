import os
import app
import unittest
import tempfile


class CicksTestCase(unittest.TestCase):
    def setUp(self):
        app.app.secret_key="adhaskhas773e9&^%%"
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_init(self):
        rv = self.app.get('/',follow_redirects=True)
        assert 'Welcome' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ),headers=[('X-Requested-With', 'XMLHttpRequest')])

    def test_login_logout(self):

        rv = self.login('orymeyer', 'password')
        assert 'LoggedIN' in rv.data

        rv = self.login('adminx', 'default')
        assert 'AuthFailed' in rv.data


    def test_shortURLPage(self):
        rv = self.login('orymeyer', 'password')

        rv = self.app.get('/')
        assert 'Shorten Links Easily' in rv.data

    def sendbURL(self,bURL):
        return self.app.post('/link/generate',
                             data=dict(URL=bURL),
                             headers=[('X-Requested-With', 'XMLHttpRequest')])

    def test_short_link_functionality(self):
        rv = self.login('orymeyer', 'password')
        rv = self.app.get('/')
        rv = self.sendbURL("http://www.google.com")
        assert "Success" in rv.data


    def passChange(self,op,np):
        return self.app.post('/updateAccount',data=dict(
            oldPassword=op,
            newPassword=np
        ),headers=[('X-Requested-With', 'XMLHttpRequest')])

    def test_pass_change(self):
        rv = self.login('orymeyer','password')
        rv = self.passChange('password','isolation')
        rv = self.get('/accounts')
        assert 'success' in rv.data
        self.app.passChange('isolation','password')

if __name__ == '__main__':
    unittest.main()