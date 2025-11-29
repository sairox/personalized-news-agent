"""Email service for sending news digests.

This module handles sending HTML emails with news articles
and tracking user preferences through like/dislike buttons.
"""

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Dict


def _get_email_config() -> Dict[str, str]:
    """Get email configuration from environment variables."""
    return {
        "smtp_server": os.getenv("SMTP_SERVER", "smtp.gmail.com"),
        "smtp_port": int(os.getenv("SMTP_PORT", "587")),
        "email_address": os.getenv("EMAIL_ADDRESS"),
        "email_password": os.getenv("EMAIL_PASSWORD"),
        "recipient_email": os.getenv("RECIPIENT_EMAIL"),
    }


def create_news_digest_html(articles: List[Dict], user_id: str = "demo_user") -> str:
    """Create HTML email template for news digest with like/dislike buttons.

    Args:
        articles: List of article dictionaries with title, summary, url, category
        user_id: User identifier for tracking preferences

    Returns:
        str: HTML formatted email content
    """
    # Base URL for tracking - in production, this would be your server
    # For now, we'll use localhost (you'll need to set up a simple web server)
    base_url = os.getenv("FEEDBACK_BASE_URL", "http://localhost:5000")

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }
            .article {
                padding: 20px;
                border-bottom: 1px solid #e0e0e0;
            }
            .article:last-child {
                border-bottom: none;
            }
            .category {
                display: inline-block;
                background-color: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: bold;
                text-transform: uppercase;
                margin-bottom: 10px;
            }
            .article-title {
                font-size: 18px;
                font-weight: bold;
                color: #333;
                margin: 10px 0;
                text-decoration: none;
            }
            .article-title a {
                color: #333;
                text-decoration: none;
            }
            .article-title a:hover {
                color: #667eea;
            }
            .article-summary {
                color: #666;
                font-size: 14px;
                line-height: 1.6;
                margin: 10px 0;
            }
            .article-source {
                color: #999;
                font-size: 12px;
                margin: 5px 0;
            }
            .feedback-buttons {
                margin-top: 15px;
                display: flex;
                gap: 10px;
            }
            .btn {
                display: inline-block;
                padding: 8px 20px;
                border-radius: 5px;
                text-decoration: none;
                font-weight: bold;
                font-size: 14px;
                transition: all 0.3s;
            }
            .btn-like {
                background-color: #4CAF50;
                color: white;
            }
            .btn-like:hover {
                background-color: #45a049;
            }
            .btn-dislike {
                background-color: #f44336;
                color: white;
            }
            .btn-dislike:hover {
                background-color: #da190b;
            }
            .footer {
                text-align: center;
                padding: 20px;
                color: #999;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📰 Your Daily News Digest</h1>
                <p>Personalized news just for you</p>
            </div>
    """

    for i, article in enumerate(articles):
        article_id = f"{user_id}_{i}_{article.get('title', '')[:20].replace(' ', '_')}"
        category = article.get("category", "general")
        title = article.get("title", "No title")
        summary = article.get("summary", "")[:200] + "..."
        url = article.get("url", "#")
        source = article.get("source", "Unknown")

        # Truncate long summaries
        if len(summary) > 200:
            summary = summary[:200] + "..."

        html += f"""
            <div class="article">
                <span class="category">{category}</span>
                <div class="article-title">
                    <a href="{url}" target="_blank">{title}</a>
                </div>
                <div class="article-summary">{summary}</div>
                <div class="article-source">Source: {source}</div>
                <div class="feedback-buttons">
                    <a href="{base_url}/feedback?article_id={article_id}&user_id={user_id}&action=like&category={category}"
                       class="btn btn-like">👍 Like</a>
                    <a href="{base_url}/feedback?article_id={article_id}&user_id={user_id}&action=dislike&category={category}"
                       class="btn btn-dislike">👎 Dislike</a>
                </div>
            </div>
        """

    html += """
            <div class="footer">
                <p>You're receiving this because you subscribed to daily news digests.</p>
                <p>Your feedback helps us personalize your news experience.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return html


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    from_email: str = None,
) -> dict:
    """Send an HTML email using SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        html_content: HTML formatted email body
        from_email: Sender email (optional, will use config if not provided)

    Returns:
        dict: Status of the email sending operation
    """
    try:
        config = _get_email_config()

        if not config["email_address"] or not config["email_password"]:
            return {
                "status": "error",
                "message": "Email credentials not configured. Set EMAIL_ADDRESS and EMAIL_PASSWORD in .env"
            }

        from_email = from_email or config["email_address"]

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = to_email

        # Attach HTML content
        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(config["smtp_server"], config["smtp_port"]) as server:
            server.starttls()
            server.login(config["email_address"], config["email_password"])
            server.send_message(msg)

        return {
            "status": "success",
            "message": f"Email sent successfully to {to_email}"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }
