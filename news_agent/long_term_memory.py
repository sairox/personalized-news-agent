"""Long-term memory system for the Personalized News Agent.

This module handles persistent memory across sessions including:
- Conversation history
- Article reading history
- User profile and interests
- Context-aware recommendations
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict


MEMORY_FILE = "agent_memory.json"


def _load_memory() -> Dict:
    """Load the complete memory from file."""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return _create_empty_memory()
    return _create_empty_memory()


def _create_empty_memory() -> Dict:
    """Create an empty memory structure."""
    return {
        "users": {},
        "version": "1.0",
        "created_at": datetime.now().isoformat(),
    }


def _save_memory(memory: Dict) -> None:
    """Save memory to file."""
    memory["last_updated"] = datetime.now().isoformat()
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def _get_user_memory(user_id: str) -> Dict:
    """Get or create memory for a specific user."""
    memory = _load_memory()

    if user_id not in memory["users"]:
        memory["users"][user_id] = {
            "profile": {
                "created_at": datetime.now().isoformat(),
                "name": None,
                "interests": [],
                "preferences": {},
            },
            "conversations": [],
            "reading_history": [],
            "article_interactions": {
                "viewed": [],
                "liked": [],
                "disliked": [],
                "saved": [],
            },
            "statistics": {
                "total_conversations": 0,
                "total_articles_viewed": 0,
                "total_emails_sent": 0,
                "favorite_topics": {},
                "engagement_score": 0,
            },
            "context": {
                "last_session": None,
                "recent_topics": [],
                "pending_questions": [],
            }
        }
        _save_memory(memory)

    return memory["users"][user_id]


def store_conversation(
    user_id: str,
    user_message: str,
    agent_response: str,
    context: Optional[Dict] = None
) -> dict:
    """Store a conversation exchange in long-term memory.

    Args:
        user_id: The user identifier
        user_message: What the user said
        agent_response: How the agent responded
        context: Additional context (tools used, articles shown, etc.)

    Returns:
        dict: Confirmation of storage
    """
    try:
        memory = _load_memory()
        user_memory = memory["users"].get(user_id)

        if not user_memory:
            user_memory = _get_user_memory(user_id)
            memory["users"][user_id] = user_memory

        conversation_entry = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "agent": agent_response,
            "context": context or {},
        }

        user_memory["conversations"].append(conversation_entry)
        user_memory["statistics"]["total_conversations"] += 1
        user_memory["context"]["last_session"] = datetime.now().isoformat()

        # Keep only last 100 conversations to avoid file bloat
        if len(user_memory["conversations"]) > 100:
            user_memory["conversations"] = user_memory["conversations"][-100:]

        memory["users"][user_id] = user_memory
        _save_memory(memory)

        return {
            "status": "success",
            "message": "Conversation stored in long-term memory",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to store conversation: {str(e)}",
        }


def store_article_interaction(
    user_id: str,
    article_title: str,
    article_url: str,
    category: str,
    action: str
) -> dict:
    """Store user interaction with an article.

    Args:
        user_id: The user identifier
        article_title: Title of the article
        article_url: URL of the article
        category: News category
        action: Type of interaction (viewed, liked, disliked, saved)

    Returns:
        dict: Confirmation of storage
    """
    try:
        memory = _load_memory()
        user_memory = memory["users"].get(user_id)

        if not user_memory:
            user_memory = _get_user_memory(user_id)
            memory["users"][user_id] = user_memory

        interaction = {
            "timestamp": datetime.now().isoformat(),
            "title": article_title,
            "url": article_url,
            "category": category,
        }

        # Store in appropriate list
        if action in user_memory["article_interactions"]:
            user_memory["article_interactions"][action].append(interaction)

        # Update statistics
        if action == "viewed":
            user_memory["statistics"]["total_articles_viewed"] += 1

        # Track favorite topics
        topics = user_memory["statistics"]["favorite_topics"]
        topics[category] = topics.get(category, 0) + 1

        # Keep recent topics in context
        if category not in user_memory["context"]["recent_topics"]:
            user_memory["context"]["recent_topics"].append(category)
            if len(user_memory["context"]["recent_topics"]) > 5:
                user_memory["context"]["recent_topics"].pop(0)

        memory["users"][user_id] = user_memory
        _save_memory(memory)

        return {
            "status": "success",
            "message": f"Article interaction '{action}' recorded",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to store interaction: {str(e)}",
        }


def get_conversation_history(
    user_id: str,
    limit: int = 10
) -> dict:
    """Retrieve recent conversation history for context.

    Args:
        user_id: The user identifier
        limit: Number of recent conversations to retrieve

    Returns:
        dict: Recent conversation history
    """
    try:
        user_memory = _get_user_memory(user_id)
        recent = user_memory["conversations"][-limit:]

        return {
            "status": "success",
            "user_id": user_id,
            "conversations": recent,
            "total_conversations": len(user_memory["conversations"]),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to retrieve history: {str(e)}",
            "conversations": [],
        }


def get_user_profile(user_id: str) -> dict:
    """Get comprehensive user profile with memory and statistics.

    Args:
        user_id: The user identifier

    Returns:
        dict: Complete user profile including interests, history, and stats
    """
    try:
        user_memory = _get_user_memory(user_id)

        # Calculate engagement score based on interactions
        total_interactions = (
            len(user_memory["article_interactions"]["liked"]) +
            len(user_memory["article_interactions"]["disliked"]) +
            len(user_memory["article_interactions"]["saved"])
        )

        viewed = user_memory["statistics"]["total_articles_viewed"]
        engagement_score = (total_interactions / max(viewed, 1)) * 100

        # Get top interests
        topics = user_memory["statistics"]["favorite_topics"]
        top_interests = sorted(topics.items(), key=lambda x: x[1], reverse=True)[:5]

        return {
            "status": "success",
            "user_id": user_id,
            "profile": user_memory["profile"],
            "statistics": {
                **user_memory["statistics"],
                "engagement_score": round(engagement_score, 2),
            },
            "top_interests": [{"topic": t, "count": c} for t, c in top_interests],
            "recent_topics": user_memory["context"]["recent_topics"],
            "last_session": user_memory["context"]["last_session"],
            "total_articles_liked": len(user_memory["article_interactions"]["liked"]),
            "total_articles_disliked": len(user_memory["article_interactions"]["disliked"]),
            "total_articles_saved": len(user_memory["article_interactions"]["saved"]),
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get profile: {str(e)}",
        }


def update_user_profile(
    user_id: str,
    name: Optional[str] = None,
    interests: Optional[List[str]] = None,
    preferences: Optional[Dict] = None
) -> dict:
    """Update user profile information.

    Args:
        user_id: The user identifier
        name: User's name
        interests: List of interest topics
        preferences: Additional preferences dict

    Returns:
        dict: Confirmation of update
    """
    try:
        memory = _load_memory()
        user_memory = memory["users"].get(user_id)

        if not user_memory:
            user_memory = _get_user_memory(user_id)
            memory["users"][user_id] = user_memory

        if name:
            user_memory["profile"]["name"] = name

        if interests:
            user_memory["profile"]["interests"] = interests

        if preferences:
            user_memory["profile"]["preferences"].update(preferences)

        memory["users"][user_id] = user_memory
        _save_memory(memory)

        return {
            "status": "success",
            "message": "User profile updated successfully",
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to update profile: {str(e)}",
        }


def get_reading_recommendations(user_id: str) -> dict:
    """Get personalized article recommendations based on memory.

    Args:
        user_id: The user identifier

    Returns:
        dict: Recommended categories and topics
    """
    try:
        user_memory = _get_user_memory(user_id)

        # Analyze liked vs disliked articles
        liked_categories = defaultdict(int)
        disliked_categories = defaultdict(int)

        for article in user_memory["article_interactions"]["liked"]:
            liked_categories[article.get("category", "general")] += 1

        for article in user_memory["article_interactions"]["disliked"]:
            disliked_categories[article.get("category", "general")] -= 1

        # Combine scores
        category_scores = {}
        for cat, score in liked_categories.items():
            category_scores[cat] = score + disliked_categories.get(cat, 0)

        # Sort by score
        recommended = sorted(
            category_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return {
            "status": "success",
            "user_id": user_id,
            "recommended_categories": [cat for cat, score in recommended if score > 0],
            "avoid_categories": [cat for cat, score in recommended if score < 0],
            "recent_interests": user_memory["context"]["recent_topics"],
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to get recommendations: {str(e)}",
            "recommended_categories": [],
        }
