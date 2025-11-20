"""Custom tools for the Personalized News Agent.

This module defines tool functions that the AI agent can use to perform
specific tasks like fetching news, filtering by category, and summarizing.
"""

from datetime import datetime
from typing import Optional


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
    """Fetches news articles for a specific category.

    Use this tool to retrieve news articles based on user interests.
    Supported categories include: technology, business, sports,
    entertainment, health, science, politics.

    Args:
        category: The news category to fetch (e.g., 'technology', 'sports').
        limit: Maximum number of articles to return (default: 5).

    Returns:
        dict: A dictionary containing news articles for the category.
    """
    # Mock news data - in production, this would call a real news API
    mock_news = {
        "technology": [
            {"title": "AI Advances in 2025", "summary": "New breakthroughs in artificial intelligence reshape industries."},
            {"title": "Quantum Computing Milestone", "summary": "Researchers achieve new quantum computing breakthrough."},
            {"title": "5G Expansion Continues", "summary": "Global 5G coverage reaches 60% of urban areas."},
            {"title": "Electric Vehicles Surge", "summary": "EV sales continue record growth worldwide."},
            {"title": "Cybersecurity Trends", "summary": "New approaches to protecting digital infrastructure."},
        ],
        "business": [
            {"title": "Markets Rally on Earnings", "summary": "Stock markets reach new highs on strong earnings."},
            {"title": "Startup Funding Rebounds", "summary": "Venture capital investments show strong recovery."},
            {"title": "Remote Work Evolution", "summary": "Companies adopt hybrid work models permanently."},
            {"title": "Supply Chain Innovation", "summary": "New technologies improve global supply chains."},
            {"title": "Green Energy Investments", "summary": "Renewable energy sector attracts record investment."},
        ],
        "sports": [
            {"title": "Championship Finals Preview", "summary": "Teams prepare for upcoming championship games."},
            {"title": "Athlete Transfer News", "summary": "Major transfers shake up professional leagues."},
            {"title": "Olympic Preparations", "summary": "Cities gear up for upcoming Olympic events."},
            {"title": "New Sports Tech", "summary": "Technology transforms athlete training and analysis."},
            {"title": "Youth Sports Programs", "summary": "Community initiatives expand youth sports access."},
        ],
        "health": [
            {"title": "Medical Research Breakthrough", "summary": "Scientists discover new treatment approaches."},
            {"title": "Mental Health Awareness", "summary": "New initiatives promote mental health support."},
            {"title": "Fitness Technology Trends", "summary": "Wearables and apps transform personal health tracking."},
            {"title": "Nutrition Science Updates", "summary": "Research reveals new insights about healthy eating."},
            {"title": "Healthcare Innovation", "summary": "Digital health solutions improve patient care."},
        ],
        "science": [
            {"title": "Space Exploration Updates", "summary": "New discoveries from recent space missions."},
            {"title": "Climate Research Findings", "summary": "Scientists publish new climate change data."},
            {"title": "Biology Discoveries", "summary": "Researchers uncover new species and mechanisms."},
            {"title": "Physics Experiments", "summary": "Particle physics experiments yield new insights."},
            {"title": "Ocean Exploration", "summary": "Deep sea expeditions reveal unknown ecosystems."},
        ],
    }

    category_lower = category.lower()
    if category_lower not in mock_news:
        return {
            "status": "error",
            "message": f"Unknown category: {category}. Available: {', '.join(mock_news.keys())}",
            "articles": [],
        }

    articles = mock_news[category_lower][:limit]
    return {
        "status": "success",
        "category": category,
        "count": len(articles),
        "articles": articles,
    }


def search_news(query: str, limit: int = 5) -> dict:
    """Searches for news articles matching a query.

    Use this tool when the user wants to find news about a specific
    topic, event, or keyword that may not fit a standard category.

    Args:
        query: The search term or phrase to look for in news.
        limit: Maximum number of results to return (default: 5).

    Returns:
        dict: A dictionary containing matching news articles.
    """
    # Mock search results - in production, this would use a real search API
    return {
        "status": "success",
        "query": query,
        "count": min(limit, 3),
        "articles": [
            {"title": f"Latest on {query}", "summary": f"Recent developments related to {query}."},
            {"title": f"{query} Analysis", "summary": f"Expert analysis of {query} trends and implications."},
            {"title": f"{query} Impact Report", "summary": f"How {query} affects various sectors."},
        ][:limit],
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
    # Mock user preferences - in production, this would query a database
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
    return {
        "status": "success",
        "message": f"Article '{article_title}' saved to your reading list.",
        "user_id": user_id,
    }


def get_trending_topics(region: Optional[str] = None) -> dict:
    """Gets currently trending news topics.

    Use this tool to discover what topics are currently popular
    in the news, optionally filtered by region.

    Args:
        region: Optional region filter (e.g., 'US', 'EU', 'Asia').

    Returns:
        dict: A dictionary containing trending topics.
    """
    trending = [
        "Artificial Intelligence",
        "Climate Change",
        "Economic Policy",
        "Space Exploration",
        "Healthcare Innovation",
    ]

    return {
        "status": "success",
        "region": region or "global",
        "topics": trending,
        "updated_at": datetime.now().isoformat(),
    }
