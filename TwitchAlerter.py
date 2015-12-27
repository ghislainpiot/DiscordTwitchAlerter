#! python3.5
import discord
import argparse
from urllib.request import urlopen
from urllib.error import URLError
import json
from threading import Timer
import time
## Twitch Alerter v1 by Djipi

#Parameters
MAIL = "Your@Mail.com" #The mail for your discord account
PASSWORD = "YourPassword" #The password of the discord account
STREAMERS = ["BestStreamer", "BestStreamer2"] #The list of your streamers
streamers_laststate = [3, 3] # Put as many "3," as your number of streamers
CHECK_INTERVAL = 30 #The interval between checks

MSG_ISNOWSTREAMING = " is now streaming."
MSG_ISNOLONGERSTREAMING = " is no longer streaming."
MSG_ISSTREAMING = " is currently streaming."
MSG_ISNOTSTREAMING = " is not currently streaming."
#End of parameters

default_channel = 0
client = discord.Client()

def check_user(user):
    url = 'https://api.twitch.tv/kraken/streams/' + user
    try:
        info = json.loads(urlopen(url, timeout = 15).read().decode('utf-8'))
        if info['stream'] == None:
            status = 1
        else:
            status = 0
    except URLError as e:
        if e.reason == 'Not Found' or e.reason == 'Unprocessable Entity':
            status = 2
        else:
            status = 3
    return status

@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    global default_channel
    default_channel = client.servers[0].get_default_channel()
@client.event
def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!check'):
        for streamer in STREAMERS:
           if (check_user(streamer) == 0):
                client.send_message(message.channel, streamer + MSG_ISSTREAMING)
           else:
                client.send_message(message.channel, streamer + MSG_ISNOTSTREAMING)

def check_streamers_timer():
    global streamers_laststate
    t = Timer(CHECK_INTERVAL, check_streamers_timer)
    t.start()
    for idx, streamer in enumerate(STREAMERS):
        state = check_user(streamer)
        if (state != streamers_laststate[idx]):
            if state == 0 and streamers_laststate[idx] == 1:
                client.send_message(channel_default, streamer + MSG_ISNOWSTREAMING)
            elif state == 1 and streamers_laststate[idx] == 0:
                client.send_message(channel_default, streamer + MSG_ISNOLONGERSTREAMING)
        streamers_laststate[idx] = check_user(streamer)

def check_streamers_first():
    global streamers_laststate
    for idx, streamer in enumerate(STREAMERS):
        streamers_laststate[idx] = check_user(streamer)

check_streamers_first()
client.login(MAIL, PASSWORD)
t = Timer(CHECK_INTERVAL, check_streamers_timer)
client.run()
t.start()

