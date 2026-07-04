# Bright Data Instagram Comments Scraper

[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Bright Data](https://img.shields.io/badge/Powered%20by-Bright%20Data-orange.svg)](https://get.brightdata.com/1tndi4600b25)

A Python wrapper for the [Bright Data](https://get.brightdata.com/1tndi4600b25) Instagram Comments scraper API. Retrieve up to **15 latest comments** (including full reply threads) from any Instagram post or reel.

## Features

- Collect up to **15 latest comments per post** with a single call
- Full **reply threads** included for every comment
- Works with both **posts** and **reels**
- Batch collection from multiple URLs in one request
- Rich comment metadata: likes, dates, hashtags, tagged users
- Simple, Pythonic interface

## Prerequisites

- Python 3.8 or higher
- A [Bright Data](https://get.brightdata.com/1tndi4600b25) account with API access
- An active Bright Data API token

## Installation

1. Clone the repository:

```bash
git clone https://github.com/luminati-io/bright-data-instagram-comments-scraper.git
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
    "comment_user": "cat_lover",
    "comment_user_url": "https://www.instagram.com/cat_lover/",
    "comment_date": "2024-03-15T10:30:00.000Z",
    "comment": "So cute! I love this little fluffball",
    "likes_number": 12,
    "replies_number": 2,
    "replies": [
      {
        "comment_user": "pet_fan",
        "comment_user_url": "https://www.instagram.com/pet_fan/",
        "comment_date": "2024-03-15T11:00:00.000Z",
        "comment": "I agree! Adorable!",
        "likes_number": 3
      },
      {
        "comment_user": "animal_photos",
        "comment_user_url": "https://www.instagram.com/animal_photos/",
        "comment_date": "2024-03-15T12:15:00.000Z",
        "comment": "Totally!",
        "likes_number": 1
      }
    ],
    "hashtag_comment": ["#cats", "#catsofinstagram"],
    "tagged_users_in_comment": ["@friend_account"]
  }
]
```

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

## Running Tests

```bash
python -m pytest tests/ -v
```

## Why Bright Data?

[Bright Data](https://get.brightdata.com/1tndi4600b25) provides reliable, scalable data collection infrastructure trusted by Fortune 500 companies. Key advantages for Instagram scraping:

- **Reliable extraction** -- consistent results even as Instagram updates its platform
- **Structured data** -- clean JSON output with all comment metadata
- **Scalable** -- collect from one post or thousands in a single batch
- **Compliant** -- built-in compliance and ethical data collection practices
- **Fast** -- average response time of ~4 seconds per request

[Get started with Bright Data](https://get.brightdata.com/1tndi4600b25)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

**Disclosure:** Some links in this document are affiliate links. If you sign up for Bright Data through these links, I may earn a commission at no extra cost to you. This helps support the maintenance of this project.
