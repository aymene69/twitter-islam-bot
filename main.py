import tweepy
import requests
import json
import time
import subprocess
import os

from random import randint
from mutagen.mp3 import MP3
from datetime import datetime

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

TWEET_MAX_LENGTH = 275

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret, access_token, access_token_secret
)

api = tweepy.API(auth)


heures = ["12:00", "20:00"]


while True:
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    if current_time == "22:00":
        sourate = randint(1, 114)
        files = os.listdir("/home/ubuntu/islam-twitter-bot/audio/" + str(sourate).zfill(3))
        aya = randint(0, len(files))
        ayadebut = aya
        sourates = []
        duration = 0
        while duration < 120:
            try:
                sourates.append(("/home/ubuntu/islam-twitter-bot/audio/" + str(sourate).zfill(3) + "/" + str(aya).zfill(3) + ".mp3"))
                duration += MP3("/home/ubuntu/islam-twitter-bot/audio/" + str(sourate).zfill(3) + "/" + str(aya).zfill(3) + ".mp3").info.length
                aya +=1
                ayafin = aya
                if aya-2 == len(files):
                    duration = 140
            except:
                duration = 140
        souratesvalides = []
        for elem in sourates:
            if os.path.isfile(elem):
                souratesvalides.append(elem)
        filesffmpeg = "|".join(souratesvalides)
        os.system("ffmpeg -y -i 'concat:"+filesffmpeg+"' -acodec copy /home/ubuntu/islam-twitter-bot/output.mp3")
        os.system("ffmpeg -y -loop 1 -i /home/ubuntu/islam-twitter-bot/black.png -i '/home/ubuntu/islam-twitter-bot/output.mp3' -c:v libx264 -vf format=yuv420p -tune stillimage -c:a aac -movflags +faststart -t 00:02:20 '/home/ubuntu/islam-twitter-bot/output.mp4'")

        def getSurahName(surahNumber):
            url = "https://api.alquran.cloud/v1/surah/" + str(surahNumber)
            response = requests.get(url)
            data = response.json()
            return data["data"]["englishName"]
        print("Sending tweet")
        os.system("python3 /home/ubuntu/islam-twitter-bot/test.py '🌃 🌙 - Prenez quelques secondes pour écouter du Coran avant de dormir !\n📖 Versets de sourate " + getSurahName(sourate).replace("'","")+"'")
    if current_time in heures:
        try:

            req = requests.get("https://mawaqit.net/api/2.0/hadith/random?lang=fr", headers={"Api-Access-Token": ""})
            json = req.json()
            tweet = "ðŸ“š" + json["text"]
            tweets = [tweet]
            to_tweet = []
            for tweet in tweets:
                while len(tweet) > TWEET_MAX_LENGTH:

                    # Take only first 280 chars
                    cut = tweet[:TWEET_MAX_LENGTH]

                    # Save as separate tweet to do later
                    to_tweet.append(cut)

                    # replace the existing 'tweet' variable with remaining chars
                    tweet = tweet[TWEET_MAX_LENGTH:]

                # Gets last tweet or those < 280
                to_tweet.append(tweet)

            original_tweet = api.update_status(status=to_tweet[0])
            
            if to_tweet[1]:
                reply1_tweet = api.update_status(status=to_tweet[1], in_reply_to_status_id=original_tweet.id, auto_populate_reply_metadata=True)

            if to_tweet[2]:
                reply2_tweet = api.update_status(status=to_tweet[2], in_reply_to_status_id=reply1_tweet.id, auto_populate_reply_metadata=True)

            if to_tweet[3]:
                reply3_tweet = api.update_status(status=to_tweet[3], in_reply_to_status_id=reply2_tweet.id, auto_populate_reply_metadata=True)

            if to_tweet[4]:
                reply4_tweet = api.update_status(status=to_tweet[4], in_reply_to_status_id=reply3_tweet.id, auto_populate_reply_metadata=True)

            if to_tweet[5]:
                reply5_tweet = api.update_status(status=to_tweet[5], in_reply_to_status_id=reply4_tweet.id, auto_populate_reply_metadata=True)
        except:
            pass
    time.sleep(60)
