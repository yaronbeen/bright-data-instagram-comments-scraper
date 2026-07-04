"""
Unit tests for InstagramCommentsScraper.

Run with:
    python -m pytest tests/ -v
"""

import os
import unittest
from unittest.mock import patch, MagicMock

import requests

from instagram_comments_scraper import InstagramCommentsScraper


class TestInstagramCommentsScraperInit(unittest.TestCase):
    """Tests for __init__ / authentication."""

    def test_init_with_explicit_token(self):
        scraper = InstagramCommentsScraper(api_token="test_token_123")
        self.assertEqual(scraper.api_token, "test_token_123")

    @patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_token_456"})
    def test_init_with_env_token(self):
        scraper = InstagramCommentsScraper()
        self.assertEqual(scraper.api_token, "env_token_456")

    @patch.dict(os.environ, {}, clear=True)
    def test_init_missing_token_raises(self):
        with self.assertRaises(ValueError) as ctx:
            InstagramCommentsScraper()
        self.assertIn("API token is required", str(ctx.exception))

    def test_explicit_token_takes_precedence_over_env(self):
        with patch.dict(os.environ, {"BRIGHT_DATA_API_TOKEN": "env_tok"}):
            scraper = InstagramCommentsScraper(api_token="explicit_tok")
        self.assertEqual(scraper.api_token, "explicit_tok")


class TestCollectByUrl(unittest.TestCase):
    """Tests for collect_by_url."""

    def setUp(self):
        self.scraper = InstagramCommentsScraper(api_token="test_token")
        self.mock_response_data = [
            {
                "url": "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/",
                "comment_user": "cat_lover",
                "comment_user_url": "https://www.instagram.com/cat_lover/",
                "comment_date": "2024-03-15T10:30:00.000Z",
                "comment": "So cute!",
                "likes_number": 12,
                "replies_number": 2,
                "replies": [
                    {
                        "comment_user": "pet_fan",
                        "comment": "I agree!",
                        "likes_number": 3,
                    }
                ],
                "hashtag_comment": ["#cats"],
                "tagged_users_in_comment": ["@friend"],
            }
        ]

    @patch("instagram_comments_scraper.requests.post")
    def test_collect_single_url_string(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        url = "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/"
        result = self.scraper.collect_by_url(url)

        self.assertEqual(result, self.mock_response_data)
        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(len(payload["input"]), 1)
        self.assertEqual(payload["input"][0]["url"], url)

    @patch("instagram_comments_scraper.requests.post")
    def test_collect_multiple_urls(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        urls = [
            "https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/",
            "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/",
            "https://www.instagram.com/cats_of_instagram/reel/C2TmNOVMSbG/",
        ]
        result = self.scraper.collect_by_url(urls)

        self.assertEqual(result, self.mock_response_data)
        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(len(payload["input"]), 3)
        for i, url in enumerate(urls):
            self.assertEqual(payload["input"][i]["url"], url)

    @patch("instagram_comments_scraper.requests.post")
    def test_correct_query_params(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        call_kwargs = mock_post.call_args
        params = call_kwargs.kwargs.get("params") or call_kwargs[1].get("params")
        self.assertEqual(params["dataset_id"], "gd_ltppn085pokosxh13")
        self.assertEqual(params["include_errors"], "true")
        self.assertNotIn("type", params)
        self.assertNotIn("discover_by", params)

    @patch("instagram_comments_scraper.requests.post")
    def test_correct_payload_structure(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertIn("input", payload)
        self.assertIn("limit_per_input", payload)
        self.assertIsInstance(payload["input"], list)
        self.assertIsInstance(payload["input"][0], dict)
        self.assertIn("url", payload["input"][0])

    @patch("instagram_comments_scraper.requests.post")
    def test_auth_headers(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        call_kwargs = mock_post.call_args
        headers = call_kwargs.kwargs.get("headers") or call_kwargs[1].get("headers")
        self.assertEqual(headers["Authorization"], "Bearer test_token")
        self.assertEqual(headers["Content-Type"], "application/json")

    @patch("instagram_comments_scraper.requests.post")
    def test_limit_per_input_default_none(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertIsNone(payload["limit_per_input"])

    @patch("instagram_comments_scraper.requests.post")
    def test_limit_per_input_custom_value(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/", limit_per_input=5)

        call_kwargs = mock_post.call_args
        payload = call_kwargs.kwargs.get("json") or call_kwargs[1].get("json")
        self.assertEqual(payload["limit_per_input"], 5)

    @patch("instagram_comments_scraper.requests.post")
    def test_request_url(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        call_args = mock_post.call_args
        called_url = call_args.args[0] if call_args.args else call_args.kwargs.get("url")
        self.assertEqual(called_url, "https://api.brightdata.com/datasets/v3/scrape")

    @patch("instagram_comments_scraper.requests.post")
    def test_http_401_raises(self, mock_post):
        mock_resp = MagicMock()
        http_error = requests.exceptions.HTTPError(response=mock_resp)
        mock_resp.raise_for_status.side_effect = http_error
        mock_resp.status_code = 401
        mock_post.return_value = mock_resp

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.collect_by_url("https://www.instagram.com/p/test/")

    @patch("instagram_comments_scraper.requests.post")
    def test_http_500_raises(self, mock_post):
        mock_resp = MagicMock()
        http_error = requests.exceptions.HTTPError(response=mock_resp)
        mock_resp.raise_for_status.side_effect = http_error
        mock_resp.status_code = 500
        mock_post.return_value = mock_resp

        with self.assertRaises(requests.exceptions.HTTPError):
            self.scraper.collect_by_url("https://www.instagram.com/p/test/")

    @patch("instagram_comments_scraper.requests.post")
    def test_connection_error_raises(self, mock_post):
        mock_post.side_effect = requests.exceptions.ConnectionError("Network down")

        with self.assertRaises(requests.exceptions.ConnectionError):
            self.scraper.collect_by_url("https://www.instagram.com/p/test/")

    @patch("instagram_comments_scraper.requests.post")
    def test_empty_response(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = []
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.collect_by_url("https://www.instagram.com/p/test/")
        self.assertEqual(result, [])

    @patch("instagram_comments_scraper.requests.post")
    def test_response_contains_comment_fields(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        comment = result[0]
        self.assertIn("url", comment)
        self.assertIn("comment_user", comment)
        self.assertIn("comment_user_url", comment)
        self.assertIn("comment_date", comment)
        self.assertIn("comment", comment)
        self.assertIn("likes_number", comment)
        self.assertIn("replies_number", comment)
        self.assertIn("replies", comment)
        self.assertIn("hashtag_comment", comment)
        self.assertIn("tagged_users_in_comment", comment)

    @patch("instagram_comments_scraper.requests.post")
    def test_response_replies_structure(self, mock_post):
        mock_resp = MagicMock()
        mock_resp.json.return_value = self.mock_response_data
        mock_resp.raise_for_status = MagicMock()
        mock_post.return_value = mock_resp

        result = self.scraper.collect_by_url("https://www.instagram.com/p/test/")

        replies = result[0]["replies"]
        self.assertIsInstance(replies, list)
        self.assertEqual(len(replies), 1)
        self.assertEqual(replies[0]["comment_user"], "pet_fan")
        self.assertEqual(replies[0]["comment"], "I agree!")


class TestScraperConstants(unittest.TestCase):
    """Tests for class-level constants."""

    def test_dataset_id(self):
        self.assertEqual(
            InstagramCommentsScraper.DATASET_ID, "gd_ltppn085pokosxh13"
        )

    def test_base_url(self):
        self.assertEqual(
            InstagramCommentsScraper.BASE_URL,
            "https://api.brightdata.com/datasets/v3/scrape",
        )


if __name__ == "__main__":
    unittest.main()
