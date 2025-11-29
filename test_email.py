#!/usr/bin/env python3
"""Test email digest functionality - send a digest immediately.

This script allows you to test the email digest feature without scheduling.
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from news_agent.tools import send_daily_digest_email


def main():
    """Send a test digest email."""
    print("=" * 60)
    print("  Testing Email Digest")
    print("=" * 60)

    # Check if email is configured
    if not os.getenv("EMAIL_ADDRESS"):
        print("\n❌ Error: Email not configured!")
        print("\nPlease set these in your .env file:")
        print("  EMAIL_ADDRESS=sender@gmail.com")
        print("  EMAIL_PASSWORD=your-app-password")
        print("  RECIPIENT_EMAIL=recipient@example.com")
        print("\nFor Gmail, use an App Password:")
        print("  https://support.google.com/accounts/answer/185833")
        return

    print(f"\nSending from: {os.getenv('EMAIL_ADDRESS')}")
    print(f"Sending to: {os.getenv('RECIPIENT_EMAIL')}")
    print("\nCollecting news articles and sending email...")

    # Send the digest
    result = send_daily_digest_email()

    print("\n" + "=" * 60)
    if result.get("status") == "success":
        print("✅ SUCCESS!")
        print(f"\n{result.get('message')}")
        print("\nCheck your inbox for the digest!")
    else:
        print("❌ FAILED!")
        print(f"\nError: {result.get('message')}")
        print("\nPlease check your email configuration in .env")
    print("=" * 60)


if __name__ == "__main__":
    main()
