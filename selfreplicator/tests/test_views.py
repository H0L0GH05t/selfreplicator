import pytest
import requests

from selfreplicator.views import *

# TODO set up test cases with data

# def test_get_authenticated_user(monkeypatch):
#     def mock_get(*args, **kwargs):
#         return None

#     monkeypatch.setattr(requests, 'get', mock_get)

#     headers = {'Authorization' : 'token %s' % access_token}
#     result_status = "success"


#     username, result_msgs, result_status = get_authenticated_user(headers, result_msgs, result_status)
#     assert result_status == "success"

class MockResponse:
    # mock json() method always returns a specific testing dictionary
    @staticmethod
    def json():
        return {'result_msgs': ['Successfully obtained access token from GitHub'],
                          'result_status': "success",
                          'success_result': "display:block;"}
    class GET:
        def get(code):
            return 'fakecode'


# Test that we can reach the home page
def test_index():
    url = "https://selfreplicator.onrender.com/"
    response = requests.get(url)

    # Verify status code
    assert response.status_code == 200


def test_results(monkeypatch):
    def mock_get(*args, **kwargs):
        return 'fakecode'
    def mock_post(*args, **kwargs):
        return 200

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'post', mock_post)

    with self.settings(CLIENT_ID='fakeclientid', CLIENT_SECRET='fakeclientsecret'):
        result = results(MockResponse())

    assert result['result_status'] == "success"


# def test_create_repo(monkeypatch):

#     def mock_post(*args, **kwargs):
#         return None

#     monkeypatch.setattr(requests, 'post', mock_post)
#     access_token = "mock_token"
#     result_msgs = []

#     result_status, result_msgs, new_repo_url = create_repo(access_token, result_msgs)
#     assert result_status == "success"