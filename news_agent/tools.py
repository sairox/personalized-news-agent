"""Custom tools for the Personalized News Agent.

This module defines tool functions that the AI agent can use to perform
specific tasks like fetching news, filtering by category, and summarizing.
"""

import os
from datetime import datetime
from typing import Optional, List, Dict

import httpx

from .email_service import create_news_digest_html, send_email
from .user_preferences import (
    record_feedback,
    get_user_preferences_detailed,
    get_recommended_categories,
)
from .long_term_memory import (
    store_conversation,
    store_article_interaction,
    get_conversation_history,
    get_user_profile,
    update_user_profile,
    get_reading_recommendations,
)

# NewsAPI configuration
NEWSAPI_BASE_URL = "https://newsapi.org/v2"


def _get_api_key() -> str:
    """Get the NewsAPI key from environment variables."""
    api_key = os.getenv("NEWS_API_KEY")
    if not api_key:
        raise ValueError(
            "NEWS_API_KEY environment variable not set. "
            "Get a free API key at https://newsapi.org/register"
        )
    return api_key


def _format_articles(articles: list) -> list:
    """Format API response articles into a consistent structure."""
    formatted = []
    for article in articles:
        formatted.append({
            "title": article.get("title", "No title"),
            "summary": article.get("description") or article.get("content", "No description available"),
            "source": article.get("source", {}).get("name", "Unknown"),
            "url": article.get("url", ""),
            "published_at": article.get("publishedAt", ""),
        })
    return formatted


def get_current_datetime() -> dict:
    """Returns the current date and time.

    Use this tool when you need to know the current date or time
    to provide context for news recency.

    Returns:
        dict: A dictionary containing the current datetime information.
    """
    now = datetime.now()
    return {
        "status": "success",
        "datetime": now.isoformat(),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day_of_week": now.strftime("%A"),
    }


def fetch_news_by_category(category: str, limit: int = 5) -> dict:
    """Fetches news articles for a specific category from NewsAPI.

    Use this tool to retrieve news articles based on user interests.
    Supported categories: business, entertainment, general, health,
    science, sports, technology.

    Args:
        category: The news category to fetch (e.g., 'technology', 'sports').
        limit: Maximum number of articles to return (default: 5, max: 100).

    Returns:
        dict: A dictionary containing news articles for the category.
    """
    valid_categories = [
        "business", "entertainment", "general", "health",
        "science", "sports", "technology"
    ]

    category_lower = category.lower()
    if category_lower not in valid_categories:
        return {
            "status": "error",
            "message": f"Unknown category: {category}. Available: {', '.join(valid_categories)}",
            "articles": [],
        }

    try:
        api_key = _get_api_key()

        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{NEWSAPI_BASE_URL}/top-headlines",
                params={
                    "category": category_lower,
                    "language": "en",
                    "pageSize": min(limit, 100),
                    "apiKey": api_key,
                }
            )
            response.raise_for_status()
            data = response.json()

        if data.get("status") != "ok":
            return {
                "status": "error",
                "message": data.get("message", "Unknown error from NewsAPI"),
                "articles": [],
            }

        articles = _format_articles(data.get("articles", []))

        return {
            "status": "success",
            "category": category,
            "count": len(articles),
            "total_results": data.get("totalResults", 0),
            "articles": articles,
        }

    except ValueError as e:
        return {"status": "error", "message": str(e), "articles": []}
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "message": f"API request failed: {e.response.status_code}",
            "articles": [],
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch news: {str(e)}",
            "articles": [],
        }


def search_news(query: str, limit: int = 5) -> dict:
    """Searches for news articles matching a query using NewsAPI.

    Use this tool when the user wants to find news about a specific
    topic, event, or keyword that may not fit a standard category.

    Args:
        query: The search term or phrase to look for in news.
        limit: Maximum number of results to return (default: 5, max: 100).

    Returns:
        dict: A dictionary containing matching news articles.
    """
    try:
        api_key = _get_api_key()

        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{NEWSAPI_BASE_URL}/everything",
                params={
                    "q": query,
                    "language": "en",
                    "sortBy": "publishedAt",
                    "pageSize": min(limit, 100),
                    "apiKey": api_key,
                }
            )
            response.raise_for_status()
            data = response.json()

        if data.get("status") != "ok":
            return {
                "status": "error",
                "message": data.get("message", "Unknown error from NewsAPI"),
                "articles": [],
            }

        articles = _format_articles(data.get("articles", []))

        return {
            "status": "success",
            "query": query,
            "count": len(articles),
            "total_results": data.get("totalResults", 0),
            "articles": articles,
        }

    except ValueError as e:
        return {"status": "error", "message": str(e), "articles": []}
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "message": f"API request failed: {e.response.status_code}",
            "articles": [],
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to search news: {str(e)}",
            "articles": [],
        }


def get_user_preferences(user_id: str) -> dict:
    """Retrieves user preferences for news personalization.

    Use this tool to get a user's preferred categories, reading history,
    and personalization settings.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        dict: A dictionary containing user preferences and settings.
    """
    # In production, this would query a database
    return {
        "status": "success",
        "user_id": user_id,
        "preferences": {
            "favorite_categories": ["technology", "science", "business"],
            "notification_enabled": True,
            "summary_length": "medium",
            "language": "en",
        },
    }


def save_article(user_id: str, article_title: str) -> dict:
    """Saves an article to the user's reading list.

    Use this tool when the user wants to bookmark or save an article
    for later reading.

    Args:
        user_id: The unique identifier for the user.
        article_title: The title of the article to save.

    Returns:
        dict: A dictionary confirming the save operation.
    """
    # In production, this would save to a database
    return {
        "status": "success",
        "message": f"Article '{article_title}' saved to your reading list.",
        "user_id": user_id,
    }


def get_trending_topics(region: Optional[str] = None) -> dict:
    """Gets currently trending news topics from top headlines.

    Use this tool to discover what topics are currently popular
    in the news, optionally filtered by country.

    Args:
        region: Optional country code (e.g., 'us', 'gb', 'de', 'fr').

    Returns:
        dict: A dictionary containing trending topics.
    """
    try:
        api_key = _get_api_key()

        params = {
            "language": "en",
            "pageSize": 20,
            "apiKey": api_key,
        }

        # Map common region names to country codes
        country_map = {
            "us": "us", "usa": "us", "united states": "us",
            "uk": "gb", "gb": "gb", "united kingdom": "gb", "britain": "gb",
            "de": "de", "germany": "de",
            "fr": "fr", "france": "fr",
            "ca": "ca", "canada": "ca",
            "au": "au", "australia": "au",
        }

        if region:
            country_code = country_map.get(region.lower(), region.lower())
            params["country"] = country_code

        with httpx.Client(timeout=30.0) as client:
            response = client.get(
                f"{NEWSAPI_BASE_URL}/top-headlines",
                params=params
            )
            response.raise_for_status()
            data = response.json()

        if data.get("status") != "ok":
            return {
                "status": "error",
                "message": data.get("message", "Unknown error from NewsAPI"),
                "topics": [],
            }

        # Extract topics from article titles
        articles = data.get("articles", [])
        topics = []
        seen = set()

        for article in articles:
            title = article.get("title", "")
            # Get first few words as topic indicator
            if title and title not in seen:
                topics.append({
                    "headline": title,
                    "source": article.get("source", {}).get("name", "Unknown"),
                })
                seen.add(title)

        return {
            "status": "success",
            "region": region or "global",
            "count": len(topics),
            "topics": topics[:10],  # Return top 10
            "updated_at": datetime.now().isoformat(),
        }

    except ValueError as e:
        return {"status": "error", "message": str(e), "topics": []}
    except httpx.HTTPStatusError as e:
        return {
            "status": "error",
            "message": f"API request failed: {e.response.status_code}",
            "topics": [],
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to fetch trending topics: {str(e)}",
            "topics": [],
        }


def collect_daily_digest(user_id: str = "demo_user") -> dict:
    """Collects 6 news articles for daily digest (2 tech, 2 politics, 2 world news).

    Use this tool to collect curated news articles for the daily email digest.
    Articles are selected based on user preferences if available.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        dict: A dictionary containing collected articles for the digest.
    """
    try:
        # Get user's preferred categories or use defaults
        user_prefs = get_user_preferences_detailed(user_id)
        favorite_categories = user_prefs.get("favorite_categories", [])

        # Define categories for digest: tech, politics/general, world news
        categories_to_fetch = [
            ("technology", 2),
            ("general", 2),  # Politics usually falls under general
            ("business", 2),  # Alternative to world news
        ]

        # If user has preferences, try to incorporate them
        if favorite_categories:
            # Use favorite categories but ensure variety
            categories_to_fetch = []
            for cat in favorite_categories[:3]:
                categories_to_fetch.append((cat, 2))

        all_articles = []

        for category, count in categories_to_fetch:
            result = fetch_news_by_category(category, limit=count)
            if result.get("status") == "success":
                articles = result.get("articles", [])
                # Add category to each article for tracking
                for article in articles:
                    article["category"] = category
                    all_articles.append(article)

        return {
            "status": "success",
            "user_id": user_id,
            "total_articles": len(all_articles),
            "articles": all_articles,
            "personalized": bool(favorite_categories),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to collect daily digest: {str(e)}",
            "articles": [],
        }


def send_daily_digest_email(user_id: str = "demo_user", recipient_email: str = None) -> dict:
    """Sends the daily news digest email with like/dislike buttons.

    Use this tool to send a personalized daily news digest to the user's email.
    The email contains 6 articles with interactive like/dislike buttons for feedback.

    Args:
        user_id: The unique identifier for the user.
        recipient_email: Email address to send to (optional, uses env var if not provided).

    Returns:
        dict: Status of the email sending operation.
    """
    try:
        # Collect articles for digest
        digest_result = collect_daily_digest(user_id)

        if digest_result.get("status") != "success":
            return digest_result

        articles = digest_result.get("articles", [])

        if not articles:
            return {
                "status": "error",
                "message": "No articles available for digest",
            }

        # Create HTML email
        html_content = create_news_digest_html(articles, user_id)

        # Get recipient email
        if not recipient_email:
            recipient_email = os.getenv("RECIPIENT_EMAIL")

        if not recipient_email:
            return {
                "status": "error",
                "message": "Recipient email not provided. Set RECIPIENT_EMAIL in .env",
            }

        # Send email
        subject = f"📰 Your Daily News Digest - {datetime.now().strftime('%B %d, %Y')}"
        result = send_email(recipient_email, subject, html_content)

        return result

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send daily digest: {str(e)}",
        }


def track_article_feedback(
    user_id: str,
    article_id: str,
    category: str,
    action: str
) -> dict:
    """Records user feedback (like/dislike) on a news article.

    Use this tool when the user provides feedback on an article.
    This helps personalize future news recommendations.

    Args:
        user_id: The unique identifier for the user.
        article_id: Unique identifier for the article.
        category: The category of the article (e.g., 'technology', 'business').
        action: Either 'like' or 'dislike'.

    Returns:
        dict: Confirmation of the feedback recording.
    """
    return record_feedback(user_id, article_id, category, action)


def get_personalized_preferences(user_id: str) -> dict:
    """Gets detailed user preferences based on feedback history.

    Use this tool to understand user preferences and personalize content.
    Returns favorite categories, engagement statistics, and recommendation data.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        dict: Detailed preference information and statistics.
    """
    return get_user_preferences_detailed(user_id)


# ============================================================================
# LONG-TERM MEMORY TOOLS
# ============================================================================


def remember_conversation(user_id: str, topic: str, summary: str) -> dict:
    """Store important conversation context in long-term memory.

    Use this tool to remember key points from the conversation that should
    be recalled in future sessions. This helps provide continuity across sessions.

    Args:
        user_id: The unique identifier for the user.
        topic: The topic or category of the conversation.
        summary: A brief summary of what was discussed.

    Returns:
        dict: Confirmation that the memory was stored.
    """
    return store_conversation(
        user_id=user_id,
        user_message=topic,
        agent_response=summary,
        context={"type": "memory_note"}
    )


def recall_past_conversations(user_id: str, limit: int = 5) -> dict:
    """Recall recent conversation history from long-term memory.

    Use this tool to get context from previous conversations with the user.
    This helps you remember what you've discussed before and provide
    personalized, contextual responses.

    Args:
        user_id: The unique identifier for the user.
        limit: Number of recent conversations to recall (default: 5).

    Returns:
        dict: Recent conversation history with context.
    """
    return get_conversation_history(user_id, limit)


def get_user_memory_profile(user_id: str) -> dict:
    """Get comprehensive user profile from long-term memory.

    Use this tool to understand the user's complete history including:
    - Reading patterns and interests
    - Engagement statistics
    - Conversation history
    - Preferences and favorite topics

    Args:
        user_id: The unique identifier for the user.

    Returns:
        dict: Complete user profile with memory and statistics.
    """
    return get_user_profile(user_id)


def update_user_info(
    user_id: str,
    name: str = None,
    interests: str = None
) -> dict:
    """Update user profile information in long-term memory.

    Use this tool when the user tells you their name, interests, or preferences.
    This helps personalize future interactions.

    Args:
        user_id: The unique identifier for the user.
        name: User's name (optional).
        interests: Comma-separated interests (e.g., "technology, science, politics").

    Returns:
        dict: Confirmation of profile update.
    """
    interests_list = None
    if interests:
        interests_list = [i.strip() for i in interests.split(",")]

    return update_user_profile(user_id, name=name, interests=interests_list)


def get_smart_recommendations(user_id: str) -> dict:
    """Get AI-powered article recommendations based on user's memory.

    Use this tool to get personalized recommendations based on the user's
    complete interaction history, reading patterns, and preferences.

    Args:
        user_id: The unique identifier for the user.

    Returns:
        dict: Personalized category and topic recommendations.
    """
    return get_reading_recommendations(user_id)


def track_article_view(
    user_id: str,
    article_title: str,
    article_url: str,
    category: str
) -> dict:
    """Track when a user views an article (for memory/analytics).

    Use this tool to record that the user has seen an article.
    This helps avoid showing duplicate content and improves recommendations.

    Args:
        user_id: The unique identifier for the user.
        article_title: Title of the article.
        article_url: URL of the article.
        category: News category.

    Returns:
        dict: Confirmation that the view was recorded.
    """
    return store_article_interaction(
        user_id=user_id,
        article_title=article_title,
        article_url=article_url,
        category=category,
        action="viewed"
    )
