"""User preferences storage and management.

This module handles storing and retrieving user preferences
based on their feedback (likes/dislikes) on news articles.
"""

import json
import os
from datetime import datetime
from typing import Dict, List


# In production, this would be a database
PREFERENCES_FILE = "user_preferences.json"


def _load_preferences() -> Dict:
    """Load user preferences from file."""
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def _save_preferences(preferences: Dict) -> None:
    """Save user preferences to file."""
    with open(PREFERENCES_FILE, "w") as f:
        json.dump(preferences, f, indent=2)


def record_feedback(
    user_id: str,
    article_id: str,
    category: str,
    action: str
) -> dict:
    """Record user feedback on an article.

    Args:
        user_id: The user identifier
        article_id: Unique identifier for the article
        category: News category (technology, business, etc.)
        action: Either 'like' or 'dislike'

    Returns:
        dict: Status of the operation
    """
    try:
        preferences = _load_preferences()

        if user_id not in preferences:
            preferences[user_id] = {
                "likes": [],
                "dislikes": [],
                "category_scores": {},
            }

        # Record the feedback
        feedback_entry = {
            "article_id": article_id,
            "category": category,
            "timestamp": datetime.now().isoformat(),
        }

        if action == "like":
            preferences[user_id]["likes"].append(feedback_entry)
            # Increase category score
            current_score = preferences[user_id]["category_scores"].get(category, 0)
            preferences[user_id]["category_scores"][category] = current_score + 1
        elif action == "dislike":
            preferences[user_id]["dislikes"].append(feedback_entry)
            # Decrease category score
            current_score = preferences[user_id]["category_scores"].get(category, 0)
            preferences[user_id]["category_scores"][category] = current_score - 1

        _save_preferences(preferences)

        return {
            "status": "success",
            "message": f"Feedback recorded: {action} for {category}",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to record feedback: {str(e)}",
        }


def get_user_preferences_detailed(user_id: str) -> dict:
    """Get detailed user preferences based on feedback history.

    Args:
        user_id: The user identifier

    Returns:
        dict: User preferences including favorite categories and statistics
    """
    try:
        preferences = _load_preferences()

        if user_id not in preferences:
            # Return default preferences
            return {
                "status": "success",
                "user_id": user_id,
                "favorite_categories": ["technology", "science", "business"],
                "category_scores": {},
                "total_likes": 0,
                "total_dislikes": 0,
                "engagement_rate": 0,
            }

        user_data = preferences[user_id]
        category_scores = user_data.get("category_scores", {})

        # Sort categories by score
        sorted_categories = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # Get top 3 favorite categories
        favorite_categories = [cat for cat, score in sorted_categories if score > 0][:3]

        # If no favorites yet, use defaults
        if not favorite_categories:
            favorite_categories = ["technology", "science", "business"]

        total_likes = len(user_data.get("likes", []))
        total_dislikes = len(user_data.get("dislikes", []))
        total_feedback = total_likes + total_dislikes

        engagement_rate = (total_likes / total_feedback * 100) if total_feedback > 0 else 0

        return {
            "status": "success",
            "user_id": user_id,
            "favorite_categories": favorite_categories,
            "category_scores": category_scores,
            "total_likes": total_likes,
            "total_dislikes": total_dislikes,
            "engagement_rate": round(engagement_rate, 2),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get preferences: {str(e)}",
        }


def get_recommended_categories(user_id: str, limit: int = 3) -> List[str]:
    """Get recommended news categories based on user feedback.

    Args:
        user_id: The user identifier
        limit: Number of categories to recommend

    Returns:
        List[str]: List of recommended category names
    """
    prefs = get_user_preferences_detailed(user_id)
    return prefs.get("favorite_categories", ["technology", "science", "business"])[:limit]
