from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, mock_open, MagicMock
import json

# The path to views file
VIEWS_PATH = 'selfreplicator.views'

class SelfReplicatorViewTests(TestCase):

    def test_index_view_loads_correctly(self):
        """
        Test that index responds with status code 200
        and uses the correct template
        """

        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    @patch(f'{VIEWS_PATH}.requests.post')
    @patch(f'{VIEWS_PATH}.requests.get')
    @patch(f'{VIEWS_PATH}.requests.put')
    @patch(f'{VIEWS_PATH}.os.path.exists')
    @patch(f'{VIEWS_PATH}.open', new_callable=mock_open)
    def test_results_view_full_success(self, mock_file_open, mock_exists, mock_put, mock_get, mock_post):
        """
        Test end-to-end flow of the results view
        """
        
        # Mock the initial token exchange POST request
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'access_token=MOCK_ACCESS_TOKEN&scope=repo&token_type=bearer'
        
        # Mock the POST request for creating the repo
        mock_post_repo = MagicMock(status_code=201, text='{"url": "mock_repo_url"}')
        # Mock the repo creation POST call
        mock_post.side_effect = [mock_post.return_value, mock_post_repo]
        
        # Mock the GET request for username
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'login': 'testuser'}
        
        # Mock the PUT request for replicating a file
        mock_put.return_value.status_code = 201
        
        # Mock the file existence check and open call
        mock_exists.return_value = True
        mock_file_open.return_value.read.return_value = b'Mock file content'

        response = self.client.get(reverse('results'), {'code': 'mock_auth_code'})

        # Assert the final response is successful and uses the right template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
        self.assertContains(response, "Successfully obtained access token")
        self.assertContains(response, "Successfully created new repo")
        self.assertContains(response, "Successfully found username testuser")

        # Assert that the external calls were made with the expected arguments
        self.assertEqual(mock_post.call_count, 2)
        mock_get.assert_called_once()
        # The number of files is 29, so assert 29 calls
        self.assertEqual(mock_put.call_count, 29)

    @patch(f'{VIEWS_PATH}.requests.post')
    def test_results_view_auth_failure(self, mock_post):
        """
        Test the error path when authentication with GitHub fails.
        """

        # Mock failed authentication
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = '{"error": "bad_code"}'

        response = self.client.get(reverse('results'), {'code': 'bad_code'})

        # Assert the response and messages match the error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'results.html')
        self.assertContains(response, "There was a problem with authentication")

    @patch(f'{VIEWS_PATH}.requests.post')
    @patch(f'{VIEWS_PATH}.requests.get')
    def test_results_view_repo_creation_failure(self, mock_get, mock_post):
        """
        Test the error path when the new repository cannot be created.
        """

        # Mock the token exchange success
        mock_post.return_value.status_code = 200
        mock_post.return_value.text = 'access_token=MOCK_ACCESS_TOKEN&scope=repo&token_type=bearer'
        
        # Mock failed repo creation POST call
        mock_post_repo = MagicMock(status_code=422, text='{"error": "Repo already exists"}')
        mock_post.side_effect = [mock_post.return_value, mock_post_repo]
        
        response = self.client.get(reverse('results'), {'code': 'mock_code'})
        
        # Assert the response matches the repo creation error
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Failed to create new repo")
        
        # Assert that get_authenticated_user and replicate_file were never called
        mock_get.assert_not_called()

    @patch(f'{VIEWS_PATH}.requests.post')
    @patch(f'{VIEWS_PATH}.requests.get')
    @patch(f'{VIEWS_PATH}.requests.put')
    @patch(f'{VIEWS_PATH}.os.path.exists')
    def test_results_view_missing_file_warning(self, mock_exists, mock_put, mock_get, mock_post):
        """
        Test the warning path when a file to be replicated is missing locally.
        """

        # Mocks initial authentication and repo creation
        mock_post.return_value.status_code = 200
        mock_post_repo = MagicMock(status_code=201)
        mock_post.side_effect = [mock_post.return_value, mock_post_repo]
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {'login': 'testuser'}
        
        # Mock to return False for one of the files
        exists_side_effect = [True] * 28 + [False]
        mock_exists.side_effect = exists_side_effect
        
        response = self.client.get(reverse('results'), {'code': 'mock_code'})
        
        # Assert the response and messages match the warning state
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "!! Missing file:")