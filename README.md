# Personalized News Agent

An AI-powered news agent built with Google's Agent Development Kit (ADK) that delivers personalized news content based on user preferences and interests.

## Features

- Fetch news articles by category (technology, business, sports, health, science)
- Search for news on specific topics
- Discover trending topics
- Save articles to a reading list
- Personalized recommendations based on user preferences

## Prerequisites

- Python 3.10 or higher
- A Google API key for Gemini models
- A NewsAPI key for fetching real news (free tier available)

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

4. Set up your API keys:

```bash
cp .env.example .env
# Edit .env and add your API keys
```

You'll need two API keys:
- **Google API Key**: Get it from [Google AI Studio](https://aistudio.google.com/apikey)
- **NewsAPI Key**: Get a free key from [NewsAPI](https://newsapi.org/register)

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

## Project Structure

```
personalized-news-agent/
├── news_agent/
│   ├── __init__.py      # Package initialization
│   ├── agent.py         # Main agent definition
│   └── tools.py         # Custom tool functions
├── run_agent.py         # Script to run agent programmatically
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment variables
└── README.md            # This file
```

## Custom Tools

The agent includes several custom tools:

- `get_current_datetime`: Get the current date and time
- `fetch_news_by_category`: Fetch news by category
- `search_news`: Search for news on specific topics
- `get_user_preferences`: Get user personalization settings
- `save_article`: Save an article to reading list
- `get_trending_topics`: Get currently trending topics

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
