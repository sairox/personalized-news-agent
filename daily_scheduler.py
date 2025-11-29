#!/usr/bin/env python3
"""Daily news digest scheduler.

This script schedules and sends daily news digest emails at 7:00 AM.
It can be run as a standalone service or configured as a cron job.
"""

import asyncio
import os
import time
from datetime import datetime, time as dt_time
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:
    load_dotenv = None

from news_agent.tools import send_daily_digest_email


def should_send_digest(target_hour: int = 7, target_minute: int = 0) -> bool:
    """Check if it's time to send the digest.

    Args:
        target_hour: Hour to send (0-23), default 7 for 7 AM
        target_minute: Minute to send (0-59), default 0

    Returns:
        bool: True if current time matches target time
    """
    now = datetime.now()
    return now.hour == target_hour and now.minute == target_minute


def send_digest_now(user_id: str = "demo_user", recipient_email: Optional[str] = None):
    """Send the daily digest immediately.

    Args:
        user_id: User identifier
        recipient_email: Email to send to (uses .env if not provided)
    """
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Sending daily digest...")

    result = send_daily_digest_email(user_id, recipient_email)

    if result.get("status") == "success":
        print(f"✅ {result.get('message')}")
    else:
        print(f"❌ Error: {result.get('message')}")

    return result


def run_scheduler(
    user_id: str = "demo_user",
    recipient_email: Optional[str] = None,
    send_hour: int = 7,
    check_interval: int = 60
):
    """Run the scheduler continuously.

    Args:
        user_id: User identifier
        recipient_email: Email to send to
        send_hour: Hour to send (0-23), default 7 for 7 AM
        check_interval: Seconds between checks, default 60
    """
    print("=" * 60)
    print("  Daily News Digest Scheduler")
    print("=" * 60)
    print(f"\nScheduled to send at: {send_hour}:00 every day")
    print(f"Checking every: {check_interval} seconds")
    print(f"User ID: {user_id}")
    print(f"Recipient: {recipient_email or 'from .env'}")
    print("\nPress Ctrl+C to stop\n")

    last_sent_date = None

    try:
        while True:
            now = datetime.now()
            current_date = now.date()

            # Check if it's time to send and we haven't sent today yet
            if should_send_digest(send_hour, 0) and last_sent_date != current_date:
                send_digest_now(user_id, recipient_email)
                last_sent_date = current_date
                print(f"\n✓ Next digest scheduled for tomorrow at {send_hour}:00\n")
            else:
                # Show current time periodically
                if now.minute % 10 == 0 and now.second < check_interval:
                    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for {send_hour}:00...")

            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\nScheduler stopped by user.")


def main():
    """Main entry point for the scheduler."""
    import argparse

    parser = argparse.ArgumentParser(description="Daily News Digest Scheduler")
    parser.add_argument(
        "--user-id",
        default="demo_user",
        help="User ID for personalization"
    )
    parser.add_argument(
        "--email",
        help="Recipient email address (overrides .env)"
    )
    parser.add_argument(
        "--hour",
        type=int,
        default=7,
        help="Hour to send (0-23), default 7 for 7 AM"
    )
    parser.add_argument(
        "--now",
        action="store_true",
        help="Send digest immediately instead of scheduling"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Check interval in seconds (default 60)"
    )

    args = parser.parse_args()

    # Load environment variables
    if load_dotenv:
        load_dotenv()

    if args.now:
        # Send immediately
        send_digest_now(args.user_id, args.email)
    else:
        # Run scheduler
        run_scheduler(
            user_id=args.user_id,
            recipient_email=args.email,
            send_hour=args.hour,
            check_interval=args.interval
        )


if __name__ == "__main__":
    main()
