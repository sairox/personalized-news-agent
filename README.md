# Personalized News Agent

An AI-powered news agent built with Google's Agent Development Kit (ADK) that delivers personalized news content based on user preferences and interests.

## Features

### Core News Capabilities
- Fetch news articles by category (technology, business, sports, health, science)
- Search for news on specific topics
- Discover trending topics
- Save articles to a reading list

### Personalization & Learning
- **Long-term memory** - Remembers conversations across sessions
- **User profile building** - Learns your interests over time
- **Like/Dislike feedback system** - Trains on your preferences
- **Smart recommendations** - AI-powered content suggestions based on your history
- **Reading history tracking** - Never shows you duplicate articles

### Daily Email Digests
- **Automated email digests** with 6 curated articles (2 tech, 2 politics, 2 business)
- **Interactive emails** with like/dislike buttons for feedback
- **Personalized content** based on your engagement history
- **Scheduled delivery** at 7:00 AM (configurable)

## Prerequisites

- Python 3.10 or higher
- A Google API key for Gemini models
- A NewsAPI key for fetching real news (free tier available)
- An email account for sending digests (Gmail recommended)
- (Optional) A publicly accessible URL for feedback webhooks in production

## Installation

1. Clone the repository and navigate to the project directory:

```bash
cd personalized-news-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your configuration:

```bash
cp .env.example .env
# Edit .env and add your credentials
```

You'll need to configure:
- **Google API Key**: Get it from [Google AI Studio](https://aistudio.google.com/apikey)
- **NewsAPI Key**: Get a free key from [NewsAPI](https://newsapi.org/register)
- **Email Settings**: Configure SMTP for sending daily digests
  - For Gmail: Use an [App Password](https://support.google.com/accounts/answer/185833)
  - Set `EMAIL_ADDRESS`, `EMAIL_PASSWORD`, and `RECIPIENT_EMAIL`

## Usage

### Option 1: Run with ADK CLI (Recommended for Development)

Use the ADK web interface for an interactive chat experience:

```bash
adk web news_agent
```

Then open http://localhost:8000 in your browser.

Or run in the terminal:

```bash
adk run news_agent
```

### Option 2: Run Programmatically

Run the agent directly with Python:

```bash
python run_agent.py
```

This starts an interactive command-line session with the agent.

### Option 3: Daily Email Digest

Send personalized news digests via email with like/dislike feedback.

#### Quick Test - Send Email from Chat

Just chat with the agent and ask it to send an email:

```bash
python run_agent.py
```

Then type:
- "Send me a news digest email"
- "Email me today's news"
- "Send the daily digest to my email"

The agent will collect 6 articles and email them to you!

#### Or Use the Test Script

```bash
python test_email.py
```

This sends a digest immediately without the chat interface.

#### Set Up Automatic Daily Emails

**1. Start the feedback webhook server (in one terminal):**

```bash
python feedback_server.py
```

This server handles like/dislike button clicks from emails.

**2. Send a test digest (in another terminal):**

```bash
python daily_scheduler.py --now
```

**3. Schedule automatic daily digests at 7:00 AM:**

```bash
python daily_scheduler.py
```

**Optional arguments:**
- `--hour 8`: Send at different hour (e.g., 8 AM)
- `--email user@example.com`: Override recipient email
- `--user-id myuser`: Specify user ID for personalization

**Using cron for production (Linux/Mac):**

```bash
# Edit crontab
crontab -e

# Add this line to send daily at 7:00 AM
0 7 * * * cd /path/to/personalized-news-agent && /path/to/venv/bin/python daily_scheduler.py --now
```

### How Personalization Works

1. **Initial Digest**: You receive 6 articles (2 tech, 2 politics/general, 2 business)
2. **Provide Feedback**: Click 👍 Like or 👎 Dislike on articles in the email
3. **Learning**: The agent tracks your preferences by category
4. **Personalized Content**: Future digests adapt to show more of what you like

The agent learns from your interactions and adjusts:
- Category preferences (e.g., if you like tech but dislike sports)
- Article selection based on engagement history
- Recommendations tailored to your interests

### Long-Term Memory System

The agent has **persistent memory** that remembers you across sessions:

**What it remembers:**
- 📝 **Conversation history** - Past discussions and context
- 📖 **Reading history** - Articles you've seen (avoids duplicates)
- ❤️ **Preferences** - Your likes, dislikes, and interests
- 📊 **Statistics** - Engagement patterns and favorite topics
- 👤 **Profile** - Your name, interests, and personalization settings

**How to use memory:**

```bash
python run_agent.py
```

Try these commands:
- "Remember that I'm interested in AI and robotics"
- "What have we talked about before?"
- "What are my favorite topics?"
- "Show me my reading statistics"
- "My name is John" (agent will remember for next session)

**Memory is stored locally** in `agent_memory.json` - your data never leaves your machine!

**Example conversation:**
```
Session 1:
You: My name is Sarah and I love technology news
Agent: Nice to meet you, Sarah! I'll remember that you're interested in technology.

Session 2 (next day):
You: What's new today?
Agent: Welcome back, Sarah! Based on your interest in technology, here are today's top tech stories...
```

## Project Structure

```
personalized-news-agent/
├── news_agent/
│   ├── __init__.py              # Package initialization
│   ├── agent.py                 # Main agent definition
│   ├── tools.py                 # Custom tool functions
│   ├── email_service.py         # Email sending and HTML templates
│   ├── user_preferences.py      # User preference tracking
│   └── long_term_memory.py      # Long-term memory system
├── run_agent.py                 # Interactive agent runner
├── daily_scheduler.py           # Daily digest scheduler
├── feedback_server.py           # Webhook server for feedback
├── test_email.py                # Quick email testing script
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── agent_memory.json            # Long-term memory storage (auto-created)
└── README.md                    # This file
```

## Custom Tools

The agent includes several custom tools:

**News Fetching:**
- `fetch_news_by_category`: Fetch real news by category (tech, business, sports, etc.)
- `search_news`: Search for news on specific topics
- `get_trending_topics`: Get currently trending topics

**Personalization:**
- `get_user_preferences`: Get user personalization settings (legacy)
- `get_personalized_preferences`: Get detailed preferences based on feedback history
- `track_article_feedback`: Record user likes/dislikes on articles
- `save_article`: Save an article to reading list

**Daily Digest:**
- `collect_daily_digest`: Collect 6 curated articles for email digest
- `send_daily_digest_email`: Send personalized digest with like/dislike buttons

**Long-Term Memory:**
- `recall_past_conversations`: Retrieve previous conversation history
- `get_user_memory_profile`: Get complete user profile with stats
- `remember_conversation`: Store important context for future sessions
- `update_user_info`: Update user name and interests
- `get_smart_recommendations`: AI-powered content recommendations
- `track_article_view`: Record when user views an article

**Utilities:**
- `get_current_datetime`: Get the current date and time

## Extending the Agent

### Adding New Tools

1. Define a new function in `news_agent/tools.py`:

```python
def my_new_tool(param: str) -> dict:
    """Description of what the tool does.

    Args:
        param: Description of the parameter.

    Returns:
        dict: Description of the return value.
    """
    return {"status": "success", "result": "..."}
```

2. Add the tool to the agent's tools list in `news_agent/agent.py`:

```python
from .tools import my_new_tool

root_agent = Agent(
    # ...
    tools=[
        # existing tools...
        my_new_tool,
    ],
)
```

### News API Integration

This agent uses [NewsAPI](https://newsapi.org/) to fetch real news articles. The integration supports:

- **Top Headlines by Category**: business, entertainment, general, health, science, sports, technology
- **Search**: Full-text search across millions of articles
- **Trending Topics**: Current top headlines by region

The free tier allows 100 requests per day, which is suitable for development and personal use.

## License

Apache 2.0 License

## Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google ADK GitHub](https://github.com/google/adk-python)
- [ADK Samples](https://github.com/google/adk-samples)
