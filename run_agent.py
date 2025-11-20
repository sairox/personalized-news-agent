#!/usr/bin/env python3
"""Run the Personalized News Agent interactively.

This script demonstrates how to run an ADK agent programmatically
without using the CLI tools (adk web, adk run).
"""

import asyncio
import os
from uuid import uuid4

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from news_agent import root_agent


async def run_agent_interactive():
    """Run the news agent in an interactive loop."""
    # Load environment variables (for API keys)
    load_dotenv()

    # Verify API key is set
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("Please set it in a .env file or export it in your shell:")
        print("  export GOOGLE_API_KEY='your-api-key-here'")
        return

    # Create session service and runner
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="personalized_news_agent",
        session_service=session_service,
    )

    # Create a new session
    user_id = "demo_user"
    session_id = str(uuid4())
    session = await session_service.create_session(
        app_name="personalized_news_agent",
        user_id=user_id,
        session_id=session_id,
    )

    print("=" * 60)
    print("  Personalized News Agent")
    print("  Powered by Google ADK")
    print("=" * 60)
    print("\nWelcome! I'm your personalized news assistant.")
    print("I can help you with:")
    print("  - Fetching news by category (technology, business, sports, etc.)")
    print("  - Searching for specific topics")
    print("  - Finding trending topics")
    print("  - Saving articles for later")
    print("\nType 'quit' or 'exit' to end the session.\n")

    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ["quit", "exit", "q"]:
                print("\nThank you for using the Personalized News Agent. Goodbye!")
                break

            # Create the user message content
            content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)],
            )

            # Run the agent and collect response
            print("\nAgent: ", end="", flush=True)

            response_text = ""
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content,
            ):
                # Check for text content in the event
                if hasattr(event, "content") and event.content:
                    if hasattr(event.content, "parts"):
                        for part in event.content.parts:
                            if hasattr(part, "text") and part.text:
                                response_text += part.text

            if response_text:
                print(response_text)
            else:
                print("[No response generated]")

            print()  # Add spacing

        except KeyboardInterrupt:
            print("\n\nInterrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print("Please try again.\n")


def main():
    """Entry point for the script."""
    asyncio.run(run_agent_interactive())


if __name__ == "__main__":
    main()
