"""
Example: Collect comments from multiple Instagram posts and reels at once.

Usage:
    export BRIGHT_DATA_API_TOKEN=your_token
    python examples/batch_comments.py
"""

from instagram_comments_scraper import InstagramCommentsScraper


def main():
    scraper = InstagramCommentsScraper()  # reads BRIGHT_DATA_API_TOKEN from env

    urls = [
        "https://www.instagram.com/cats_of_instagram/reel/C4GLo_eLO2e/",
        "https://www.instagram.com/catsofinstagram/p/CesFC7JLyFl/?img_index=1",
        "https://www.instagram.com/cats_of_instagram/reel/C2TmNOVMSbG/",
    ]

    print(f"Fetching comments for {len(urls)} posts/reels...")
    print("=" * 60)

    results = scraper.collect_by_url(urls)

    # Group comments by source URL
    by_post: dict[str, list] = {}
    for comment in results:
        post_url = comment.get("url", "unknown")
        by_post.setdefault(post_url, []).append(comment)

    for post_url, comments in by_post.items():
        print(f"\nPost: {post_url}")
        print(f"Comments found: {len(comments)}")
        print("-" * 60)

        for comment in comments:
            user = comment.get("comment_user", "N/A")
            date = comment.get("comment_date", "N/A")
            text = comment.get("comment", "N/A")
            likes = comment.get("likes_number", 0)
            replies_count = comment.get("replies_number", 0)
            hashtags = comment.get("hashtag_comment", [])
            tagged = comment.get("tagged_users_in_comment", [])

            print(f"  @{user} ({date}) - {likes} likes, {replies_count} replies")
            print(f"    {text}")
            if hashtags:
                print(f"    Hashtags: {', '.join(hashtags)}")
            if tagged:
                print(f"    Tagged: {', '.join(tagged)}")

    print("=" * 60)
    print(f"Total comments across all posts: {len(results)}")


if __name__ == "__main__":
    main()
