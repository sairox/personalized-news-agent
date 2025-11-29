#!/usr/bin/env python3
"""Feedback webhook server for handling like/dislike clicks from emails.

This server receives feedback from the email buttons and records
user preferences for personalization.
"""

import os
from urllib.parse import parse_qs

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from news_agent.user_preferences import record_feedback


# Simple HTTP server to handle feedback
def create_feedback_handler():
    """Create a simple HTTP request handler for feedback."""
    from http.server import BaseHTTPRequestHandler

    class FeedbackHandler(BaseHTTPRequestHandler):
        """HTTP handler for processing feedback requests."""

        def do_GET(self):
            """Handle GET requests from email button clicks."""
            if self.path.startswith("/feedback"):
                # Parse query parameters
                if "?" in self.path:
                    _, query_string = self.path.split("?", 1)
                    params = parse_qs(query_string)

                    user_id = params.get("user_id", ["demo_user"])[0]
                    article_id = params.get("article_id", ["unknown"])[0]
                    category = params.get("category", ["general"])[0]
                    action = params.get("action", ["like"])[0]

                    # Record the feedback
                    result = record_feedback(user_id, article_id, category, action)

                    # Send response
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()

                    if result.get("status") == "success":
                        response_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Feedback Recorded</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100vh;
                                    margin: 0;
                                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                }}
                                .container {{
                                    background: white;
                                    padding: 40px;
                                    border-radius: 10px;
                                    text-align: center;
                                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                                }}
                                h1 {{
                                    color: #333;
                                    margin-bottom: 20px;
                                }}
                                p {{
                                    color: #666;
                                    font-size: 18px;
                                }}
                                .emoji {{
                                    font-size: 64px;
                                    margin-bottom: 20px;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <div class="emoji">{'👍' if action == 'like' else '👎'}</div>
                                <h1>Thank You!</h1>
                                <p>Your feedback has been recorded.</p>
                                <p>We'll use this to personalize your future news digests.</p>
                            </div>
                        </body>
                        </html>
                        """
                    else:
                        response_html = f"""
                        <!DOCTYPE html>
                        <html>
                        <head>
                            <title>Error</title>
                            <style>
                                body {{
                                    font-family: Arial, sans-serif;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                    height: 100vh;
                                    margin: 0;
                                    background: #f44336;
                                }}
                                .container {{
                                    background: white;
                                    padding: 40px;
                                    border-radius: 10px;
                                    text-align: center;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="container">
                                <h1>Oops!</h1>
                                <p>Something went wrong recording your feedback.</p>
                                <p>{result.get('message')}</p>
                            </div>
                        </body>
                        </html>
                        """

                    self.wfile.write(response_html.encode())
                else:
                    # No parameters provided
                    self.send_response(400)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(b"<h1>400 Bad Request</h1><p>Missing parameters</p>")
            else:
                # Invalid path
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"<h1>404 Not Found</h1>")

        def log_message(self, format, *args):
            """Custom log message format."""
            print(f"[{self.log_date_time_string()}] {format % args}")

    return FeedbackHandler


def run_server(port: int = 5000):
    """Run the feedback webhook server.

    Args:
        port: Port to run the server on (default 5000)
    """
    from http.server import HTTPServer

    handler = create_feedback_handler()
    server = HTTPServer(("0.0.0.0", port), handler)

    print("=" * 60)
    print("  Feedback Webhook Server")
    print("=" * 60)
    print(f"\nServer running on: http://localhost:{port}")
    print(f"Feedback endpoint: http://localhost:{port}/feedback")
    print("\nThis server tracks user feedback from email buttons.")
    print("Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        server.shutdown()


def main():
    """Main entry point for the feedback server."""
    import argparse

    parser = argparse.ArgumentParser(description="Feedback Webhook Server")
    parser.add_argument(
        "--port",
        type=int,
        default=5000,
        help="Port to run the server on (default 5000)"
    )

    args = parser.parse_args()
    run_server(args.port)


if __name__ == "__main__":
    main()
