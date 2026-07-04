"""
Example: Collect comments from a single Instagram post.

Usage:
    export BRIGHT_DATA_API_TOKEN=your_token
    python examples/collect_comments.py
"""

from instagram_comments_scraper import InstagramCommentsScraper


def main():
    scraper = InstagramCommentsScraper()  # reads BRIGHT_DATA_API_TOKEN from env

    post_url = "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/?img_index=1"

    print(f"Fetching comments for: {post_url}")
    print("-" * 60)

    results = scraper.collect_by_url(post_url)

    for comment in results:
        print(f"User:    {comment.get('comment_user', 'N/A')}")
        print(f"Date:    {comment.get('comment_date', 'N/A')}")
        print(f"Comment: {comment.get('comment', 'N/A')}")
        print(f"Likes:   {comment.get('likes_number', 0)}")

        replies = comment.get("replies", [])
        if replies:
            print(f"Replies ({len(replies)}):")
            for reply in replies:
                print(f"  - @{reply.get('comment_user', '?')}: {reply.get('comment', '')}")

        print("-" * 60)

    print(f"\nTotal comments returned: {len(results)}")


if __name__ == "__main__":
    main()
