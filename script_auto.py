from telethon import TelegramClient
from telethon.errors import PeerFloodError, UsernameInvalidError, PhotoSaveFileInvalidError
import asyncio
import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading

# Fetch API credentials from environment variables
api_id = os.getenv("API_ID")  # Fetch from environment variable
api_hash = os.getenv("API_HASH")  # Fetch from environment variable

# List of group/channel links
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

client = TelegramClient('my_session', api_id, api_hash)

# Your custom message with spoiler and bot username
custom_text_message = """
||Unlock exclusive premium accounts with ease! 🎁
Get access to Netflix, Spotify, YouTube, and more for FREE through our referral system.||

🔑 Start now and enjoy premium perks today!
👉 Tap here: @ishteros_bot

🚀 Don’t miss out on this amazing opportunity!
"""

# Image URL from Imgur
image_url = 'https://i.imgur.com/a/5CcFTls.jpeg'  # Ensure this is the direct image URL

# Health check handler on port 8000
def start_health_check_server():
    handler = SimpleHTTPRequestHandler
    httpd = TCPServer(('', 8000), handler)
    print("Starting health check server on port 8000...")
    httpd.serve_forever()

# Start health check server in a separate thread
threading.Thread(target=start_health_check_server, daemon=True).start()

async def send_message():
    await client.start()
    for group in group_links:
        try:
            # Attempt to send image with caption
            await client.send_file(group, image_url, caption=custom_text_message)
            print(f"Image with caption sent to {group}")
            
        except PeerFloodError:
            print(f"Rate limit exceeded for {group}. Skipping.")
            continue  # Skip if the bot is rate-limited

        except PhotoSaveFileInvalidError:
            print(f"Invalid photo for {group}. Skipping.")
            continue  # Skip if photo upload fails

        except UsernameInvalidError:
            print(f"Invalid username for {group}. Skipping.")
            continue  # Skip if username is invalid for the group
        
        except Exception as e:
            # If image sending fails, fallback to sending text message
            print(f"Error sending image to {group}: {e}")
            try:
                # Attempt to send text message with spoiler
                await client.send_message(group, custom_text_message)
                print(f"Text message with spoiler sent to {group}")
            except Exception as e:
                print(f"Failed to send text message to {group}: {e}")
            continue  # Skip on errors

async def main():
    while True:
        await send_message()
        await asyncio.sleep(3600)  # Wait for 60 minutes before sending the next message

with client:
    client.loop.run_until_complete(main())
