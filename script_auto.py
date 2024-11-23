import os
import asyncio
from telethon import TelegramClient
from telethon.errors import PeerFloodError, UsernameInvalidError, PhotoSaveFileInvalidError, FloodWaitError

# Fetch API credentials from environment variables
api_id = os.getenv("TELEGRAM_API_ID")  # Set as an environment variable in hosting
api_hash = os.getenv("TELEGRAM_API_HASH")  # Set as an environment variable in hosting

# List of Telegram group/channel links
group_links = [
    "https://t.me/Dark_escrow_group",
    "https://t.me/hackers_chatting_group",
    "https://t.me/mrxChaTting",
    "https://t.me/Darknetdiscussion",
    "https://t.me/+KDFn-JDLEUI3ZjNl",
    "https://t.me/VOLCONOGROUP",
    "https://t.me/chitchat_only",
    "https://t.me/bhcbbhghjkk",
    "https://t.me/HitlerChkChat",
    "https://t.me/FRIENDS_CHATTING_GROUPxWM",
    "https://t.me/sagar_trusted",
    "https://t.me/darkdealrzcc",
    "https://t.me/MonkDiscuss",
    "https://t.me/DirectDiscussion",
    "https://t.me/twinkleladdooofree",
    "https://t.me/trickhub_01",
    "https://t.me/swter1",
    "https://t.me/everycookieschat",
    "https://t.me/earnmoneychatting"
]

# Your message content
custom_text_message = """
||Unlock exclusive premium accounts with ease! 🎁
Get access to Netflix, Spotify, YouTube, and more for FREE through our referral system.||

🔑 Start now and enjoy premium perks today!
👉 Tap here: @ishteros_bot

🚀 Don’t miss out on this amazing opportunity!
"""

# Image URL (ensure it's direct)
image_url = 'https://i.imgur.com/a/5CcFTls.jpeg'  # Replace with your image URL

# Initialize the Telegram client
client = TelegramClient('my_session', api_id, api_hash)

async def send_to_group(group: str):
    """
    Sends a message with an image or text to a specific group.
    """
    try:
        # Attempt to send an image with a caption
        await client.send_file(group, image_url, caption=custom_text_message)
        print(f"Image with caption sent to {group}")
    except PeerFloodError:
        print(f"Rate limit exceeded for {group}. Skipping.")
    except PhotoSaveFileInvalidError:
        print(f"Invalid photo for {group}. Skipping.")
    except UsernameInvalidError:
        print(f"Invalid username for {group}. Skipping.")
    except FloodWaitError as e:
        print(f"Flood wait error: Sleeping for {e.seconds} seconds.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        print(f"Unexpected error sending image to {group}: {e}. Sending text message as fallback.")
        try:
            # Attempt to send text message as fallback
            await client.send_message(group, custom_text_message)
            print(f"Text message sent to {group}")
        except Exception as inner_e:
            print(f"Failed to send text message to {group}: {inner_e}")

async def send_messages():
    """
    Sends messages to all groups in the group list.
    """
    for group in group_links:
        print(f"Processing group: {group}")
        await send_to_group(group)
        await asyncio.sleep(10)  # Sleep to avoid hitting Telegram's rate limits

async def main():
    """
    Main function to handle continuous execution with a delay between iterations.
    """
    while True:
        print("Starting a new message batch...")
        await send_messages()
        print("Batch complete. Sleeping for 1 hour.")
        await asyncio.sleep(3600)  # Wait for 1 hour between batches

# Run the client and start the main function
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
