"""Personalized News Agent using Google ADK.

This module defines the main AI agent for delivering personalized news
content to users based on their preferences and interests.
"""

from google.adk.agents import Agent

from .tools import (
    fetch_news_by_category,
    get_current_datetime,
    get_trending_topics,
    get_user_preferences,
    save_article,
    search_news,
)

# Agent system instruction
AGENT_INSTRUCTION = """You are a helpful personalized news assistant that helps users
stay informed about topics they care about.

Your capabilities include:
- Fetching news articles by category (technology, business, sports, health, science)
- Searching for news on specific topics
- Identifying trending topics
- Saving articles to a user's reading list
- Retrieving user preferences for personalization

When interacting with users:
1. Be concise but informative when presenting news
2. Organize information clearly with headlines and brief summaries
3. Offer to provide more details if the user is interested
4. Suggest related topics based on their interests
5. Remember to check trending topics if users want to know what's popular

Always be helpful, accurate, and respect the user's time by providing
relevant information efficiently. If you don't have specific information,
use the available tools to fetch it.
"""

# Define the root agent
root_agent = Agent(
    name="personalized_news_agent",
    model="gemini-2.0-flash",
    instruction=AGENT_INSTRUCTION,
    description="A personalized news assistant that delivers relevant news content based on user preferences and interests.",
    tools=[
        get_current_datetime,
        fetch_news_by_category,
        search_news,
        get_user_preferences,
        save_article,
        get_trending_topics,
    ],
)
