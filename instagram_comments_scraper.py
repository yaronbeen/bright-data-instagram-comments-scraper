"""
Bright Data Instagram Comments Scraper

A Python wrapper for the Bright Data Instagram Comments scraper API.
Returns the latest 15 comments per post, including replies.

Dataset ID: gd_ltppn085pokosxh13
Rate: $0.0015/record
Avg Response Time: 4s
"""

import os
import requests
from typing import List, Optional, Dict, Any, Union


class InstagramCommentsScraper:
    """Client for the Bright Data Instagram Comments scraper API.

    Collects up to 15 latest comments (with replies) from Instagram
    posts and reels via Bright Data's dataset endpoint.
    """

    BASE_URL = "https://api.brightdata.com/datasets/v3/scrape"
    DATASET_ID = "gd_ltppn085pokosxh13"

    def __init__(self, api_token: Optional[str] = None):
        """Initialize the scraper.

        Args:
            api_token: Bright Data API token. Falls back to the
                       BRIGHT_DATA_API_TOKEN environment variable.

        Raises:
            ValueError: If no API token is provided or found in the environment.
        """
        self.api_token = api_token or os.getenv("BRIGHT_DATA_API_TOKEN")
        if not self.api_token:
            raise ValueError(
                "API token is required. Pass it directly or set the "
                "BRIGHT_DATA_API_TOKEN environment variable."
            )

    def collect_by_url(
        self,
        urls: Union[str, List[str]],
        limit_per_input: Optional[int] = None,
    ) -> Any:
        """Collect comments from Instagram post or reel URLs.

        Returns the latest 15 comments per post, including reply threads.

        Args:
            urls: A single URL string or a list of Instagram post/reel URLs.
            limit_per_input: Optional cap on results returned per input URL.

        Returns:
            Parsed JSON response from the Bright Data API.

        Raises:
            requests.HTTPError: On non-2xx responses.
            requests.ConnectionError: On network failures.
        """
        if isinstance(urls, str):
            urls = [urls]

        payload: Dict[str, Any] = {
            "input": [{"url": url} for url in urls],
            "limit_per_input": limit_per_input,
        }

        params = {
            "dataset_id": self.DATASET_ID,
            "include_errors": "true",
        }

        return self._make_request(params, payload)

    def _make_request(self, params: Dict[str, str], payload: Dict[str, Any]) -> Any:
        """Send a POST request to the Bright Data scrape endpoint.

        Args:
            params: Query-string parameters.
            payload: JSON body.

        Returns:
            Parsed JSON response.

        Raises:
            requests.HTTPError: On non-2xx responses.
            requests.ConnectionError: On network failures.
        """
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

        response = requests.post(
            self.BASE_URL, headers=headers, params=params, json=payload
        )
        response.raise_for_status()
        return response.json()
