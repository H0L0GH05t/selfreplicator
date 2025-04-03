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

# Test that we can reach the home page
def test_index():
    print("Starting home page test...")
    url = "https://selfreplicator.onrender.com/"  # Replace with your mock API URL
    response = requests.get(url)

    # Verify status code
    assert response.status_code == 200

    print("End of home page test!")


def test_results(monkeypatch):
    print("Starting results view test...")
    def mock_get(*args, **kwargs):
        return None
    def mock_post(*args, **kwargs):
        return 200

    monkeypatch.setattr(requests, 'get', mock_get)
    monkeypatch.setattr(requests, 'post', mock_get)

    assert "Successfully obtained access token from GitHub" in result_msgs
    assert result_status == "success"
    assert success_result == "display:block;"

    print("End of results view test!")

# def test_create_repo(monkeypatch):

#     def mock_post(*args, **kwargs):
#         return None

#     monkeypatch.setattr(requests, 'post', mock_post)
#     access_token = "mock_token"
#     result_msgs = []

#     result_status, result_msgs, new_repo_url = create_repo(access_token, result_msgs)
#     assert result_status == "success"