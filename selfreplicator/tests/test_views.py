from selfreplicator.views import *

# TODO FOR results()
# TODO: figure out how we can test the repo creation (create_repo()) with fake data
# TODO: need to fake the auth_response as well most likely
# TODO: expect to also use fake new_repo_url

# def test_results(request):
#     response = results(request)
#     assert response.status_code == 200

#TODO set up test cases with data
#TODO mb just test create_repo which calls the below
# def test_get_authenticated_user(monkeypatch):
#     def mock_get(*args, **kwargs):
#         return None

#     monkeypatch.setattr(requests, 'get', mock_get)

#     headers = {'Authorization' : 'token %s' % access_token}
#     result_status = "success"


#     username, result_msgs, result_status = get_authenticated_user(headers, result_msgs, result_status)
#     assert result_status == "success"

def test_create_repo(monkeypatch):

    def mock_post(*args, **kwargs):
        return None

    monkeypatch.setattr(requests, 'post', mock_post)
    access_token = "mock_tocken"
    result_msgs = []

    result_status, result_msgs, new_repo_url = create_repo(access_token, result_msgs)
    assert result_status == "success"