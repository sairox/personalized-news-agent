"""Custom tools for the Personalized News Agent.

This module defines tool functions that the AI agent can use to perform
specific tasks like fetching news, filtering by category, and summarizing.
"""

import os
from datetime import datetime
from typing import Optional

import httpx

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
