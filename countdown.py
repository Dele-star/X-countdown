import os
import datetime
from PIL import Image, ImageDraw, ImageFont
import tweepy

# Target Date: November 1, 2026 00:00:00 UTC
TARGET_DATE = datetime.datetime(2026, 11, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

# Pink color extracted from the CC logo image
PINK_COLOR = (255, 59, 107)  # #FF3B6B
BG_COLOR = (15, 15, 15)      # Dark clean background

def generate_banner():
    now = datetime.datetime.now(datetime.timezone.utc)
    time_left = TARGET_DATE - now

    # Check if the countdown has reached or passed the target date
    if time_left.total_seconds() <= 0:
        countdown_text = "LIVE NOW!"
    else:
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_text = f"{days:02d}D : {hours:02d}H : {minutes:02d}M : {seconds:02d}S"

    # Banner dimensions for X (1500 x 500)
    width, height = 1500, 500
    image = Image.new("RGB", (width, height), color=BG_COLOR)
    draw = ImageDraw.Draw(image)

    # Use default PIL font or scalable TrueType font
    font_size = 110
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Get text bounding box to center it
    bbox = draw.textbbox((0, 0), countdown_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = (width - text_width) / 2
    y = (height - text_height) / 2 - 20

    # Draw main text in Pink
    draw.text((x, y), countdown_text, fill=PINK_COLOR, font=font)

    banner_path = "banner.png"
    image.save(banner_path)
    return banner_path

def update_x_banner():
    consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
    consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
    access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)

    banner_path = generate_banner()
    api.update_profile_banner(banner_path)
    print("X banner updated successfully!")

if __name__ == "__main__":
    update_x_banner()