# Bright Data Instagram Comments Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for Bright Data's Instagram Comments scraper API. Retrieve up to **15 latest comments** (including full reply threads) from any Instagram post or reel.

> **All Instagram scrapers:** [Profile Scraper](https://github.com/yaronbeen/bright-data-instagram-profile-scraper) · [Profile Discovery](https://github.com/yaronbeen/bright-data-instagram-profile-discovery) · [Posts Scraper](https://github.com/yaronbeen/bright-data-instagram-posts-scraper) · [Posts Discovery](https://github.com/yaronbeen/bright-data-instagram-posts-discovery) · [Reels Scraper](https://github.com/yaronbeen/bright-data-instagram-reels-scraper) · [Reels Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-discovery) · [Reels (All) Discovery](https://github.com/yaronbeen/bright-data-instagram-reels-all-discovery) · **Comments Scraper**

## Features

- Collect up to **15 latest comments per post** with a single call
- Full **reply threads** included for every comment
- Works with both **posts** and **reels**
- Batch collection from multiple URLs in one request
- Rich comment metadata: likes, dates, hashtags, tagged users
- Simple, Pythonic interface

## Use Cases

- Run sentiment analysis on audience reactions
- Identify frequently asked questions from followers
- Monitor brand mentions and tagged users in comments
- Track reply engagement patterns

## Prerequisites

- Python 3.8 or higher
- A Bright Data account with API access (create an account at https://brightdata.com)
- An active Bright Data API token

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yaronbeen/bright-data-instagram-comments-scraper.git
cd bright-data-instagram-comments-scraper
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your API token:

```bash
cp .env.example .env
# Edit .env and add your Bright Data API token
```

Or export it directly:

```bash
export BRIGHT_DATA_API_TOKEN="your_api_token_here"
```

## Quick Start

```python
from instagram_comments_scraper import InstagramCommentsScraper

scraper = InstagramCommentsScraper(api_token="your_api_token")

# Get comments from a single post
results = scraper.collect_by_url(
    "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/"
)

for comment in results:
    print(f"@{comment['comment_user']}: {comment['comment']}")
```

## API Reference

### `InstagramCommentsScraper(api_token=None)`

Create a new scraper instance.

| Parameter   | Type            | Required | Description                                                                 |
|-------------|-----------------|----------|-----------------------------------------------------------------------------|
| `api_token` | `str` or `None` | No       | Bright Data API token. Falls back to the `BRIGHT_DATA_API_TOKEN` env var.   |

### `collect_by_url(urls, limit_per_input=None)`

Collect comments from Instagram post or reel URLs. Returns the **latest 15 comments per post**.

| Parameter         | Type                | Required | Description                                      |
|-------------------|---------------------|----------|--------------------------------------------------|
| `urls`            | `str` or `list[str]`| Yes      | One or more Instagram post/reel URLs.            |
| `limit_per_input` | `int` or `None`     | No       | Cap on the number of results per input URL.      |

**Returns:** Parsed JSON response (list of comment objects).

**Supported URL formats:**

```
https://www.instagram.com/username/p/POST_ID/
https://www.instagram.com/username/reel/REEL_ID/
```

## Example Output

```json
[
  {
    "url": "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/",
    "comment_user": "meow_daily",
    "comment_user_url": "https://www.instagram.com/meow_daily/",
    "comment_date": "2024-03-15T10:30:00.000Z",
    "comment": "Our tabby does the exact same thing with her paws!",
    "likes_number": 7,
    "replies_number": 2,
    "replies": [
      {
        "comment_user": "rescued_kitties",
        "comment_user_url": "https://www.instagram.com/rescued_kitties/",
        "comment_date": "2024-03-15T11:04:00.000Z",
        "comment": "Mine too haha it's a tabby thing",
        "likes_number": 2
      },
      {
        "comment_user": "catmom_jen",
        "comment_user_url": "https://www.instagram.com/catmom_jen/",
        "comment_date": "2024-03-15T12:18:00.000Z",
        "comment": "So funny! Ours does it when she wants treats",
        "likes_number": 1
      }
    ],
    "hashtag_comment": ["#tabbycats", "#catlife"],
    "tagged_users_in_comment": ["@rescued_kitties"]
  }
]
```

> Note: This is a representative example. Actual field values and available fields may vary.

> **Note:** The API returns the **latest 15 comments** per post. For posts with fewer than 15 comments, all available comments are returned.

## Output Fields

| Field                       | Type     | Description                              |
|-----------------------------|----------|------------------------------------------|
| `url`                       | `str`    | URL of the source post                   |
| `comment_user`              | `str`    | Username of the commenter                |
| `comment_user_url`          | `str`    | Profile URL of the commenter             |
| `comment_date`              | `str`    | Timestamp of the comment                 |
| `comment`                   | `str`    | The comment text                         |
| `likes_number`              | `int`    | Number of likes on the comment           |
| `replies_number`            | `int`    | Number of replies to the comment         |
| `replies`                   | `list`   | Array of reply objects                   |
| `hashtag_comment`           | `list`   | Hashtags used in the comment             |
| `tagged_users_in_comment`   | `list`   | Usernames tagged in the comment          |

## Error Handling

The scraper raises standard exceptions you can catch:

```python
import requests
from instagram_comments_scraper import InstagramCommentsScraper

try:
    scraper = InstagramCommentsScraper()
    results = scraper.collect_by_url("https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/")
except ValueError as e:
    print(f"Configuration error: {e}")
except requests.exceptions.HTTPError as e:
    print(f"API error: {e}")
except requests.exceptions.ConnectionError:
    print("Could not connect to the API")
```

| Exception                          | Cause                                  |
|------------------------------------|----------------------------------------|
| `ValueError`                       | Missing API token.                     |
| `requests.exceptions.HTTPError`    | API returned 4xx/5xx (auth, rate limit, etc.). |
| `requests.exceptions.ConnectionError` | Network connectivity issue.         |
| `requests.exceptions.ReadTimeout`  | Request took longer than 30 seconds.   |

## Rate Limits

- **Sync mode:** Results returned directly in the response. Best for small batches (1-10 inputs).
- **Async mode:** For larger jobs, use the async API. See [Bright Data API docs](https://docs.brightdata.com/datasets/functions/introduction).
- **No hard rate limit** on API calls, but performance varies with batch size.
- **Pricing:** $0.0015 per record ($1.50 per 1,000 records).
- **15 comments max** per post URL.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

Comment threads are the hardest Instagram data to scrape reliably. Bright Data specializes in conversation data:

- **Full reply threads returned** - Not just top-level comments, but nested replies with metadata
- **Commenter profiles, like counts, and tagged users** included in every record
- **Works on both posts and reels** - Same API call, same response format
- **Latest 15 comments per post** at $0.0015/record
- **No infrastructure to maintain** - Anti-bot handling and proxy rotation managed for you

For full API documentation, see the [Bright Data API Reference](https://docs.brightdata.com/datasets/functions/introduction).

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
