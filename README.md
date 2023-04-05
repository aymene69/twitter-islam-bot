# twitter-islam-bot
Twitter bot that uploads hadiths and Quran on a defined basis.

It sends once a Black video with random ayas (not randomly exactly, but ayas starting from a random position. i.e: surah 2 starting from 255) and a hadith twice everyday.

# Usage
You need to get Mutagen and tweepy libraries for Python, and ffmpeg in your PATH.

Don't forget to change your computer time to fetch correct times.
Don't forget to change files paths in main.py and test.py (or clone it in /home/ubuntu for a ready-to-go launch)
Don't forget to insert your Twitter Keys in main.py and test.py
For hadiths, you need a Mawaqit API key (it's only in French, you can ask them in their website by contacting them) and put it in line 67

You can then launch main.py and it will check every hour if it is the correct time.
