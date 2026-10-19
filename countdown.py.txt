from datetime import datetime, timezone
from PIL import Image, ImageDraw, ImageFont
import tweepy
import os

CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("TWITTER_ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuth1UserHandler(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

# SET YOUR TARGET COUNTDOWN DATE & TIME (UTC)
TARGET_DATE = datetime(2026, 11, 1, 0, 0, tzinfo=timezone.utc) 

now = datetime.now(timezone.utc)
remaining = TARGET_DATE - now
days_left = max(0, remaining.days)

# Create 1500x500 banner image
banner = Image.new("RGB", (1500, 500), color=(15, 20, 25))
draw = ImageDraw.Draw(banner)

try:
    font_large = ImageFont.truetype("arial.ttf", 130)
    font_small = ImageFont.truetype("arial.ttf", 55)
except IOError:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

draw.text((750, 190), f"{days_left} DAYS LEFT", fill=(255, 255, 255), anchor="mm", font=font_large)
draw.text((750, 320), "Until the big event!", fill=(136, 153, 166), anchor="mm", font=font_small)

banner_path = "temp_banner.png"
banner.save(banner_path)

# Upload banner to X
api.update_profile_banner(banner_path)
print(f"Updated banner! Countdown: {days_left} days left.")

if os.path.exists(banner_path):
    os.remove(banner_path)