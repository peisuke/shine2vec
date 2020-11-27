import argparse
import os
import json
import time
import sys
import traceback
import requests
from datetime import date, datetime, timedelta
from tqdm import tqdm

SLACK_TOKEN = os.environ['SLACK_TOKEN']

def get_user_list():
    next_cursor = None
    members = []

    while True:
        payload = {
            'token': SLACK_TOKEN
        }
        if next_cursor:
            payload['cursor'] = next_cursor
        
        r = requests.get('https://slack.com/api/users.list',
                         params=payload)
        r = r.json()
        members.extend(r['members'])
    
        next_cursor = r['response_metadata']['next_cursor']
        if len(next_cursor) == 0:
            break

    return members

def get_channel_list():
    next_cursor = None
    channels = []

    while True:
        payload = {
            'token': SLACK_TOKEN
        }
        if next_cursor:
            payload['cursor'] = next_cursor
        
        r = requests.get('https://slack.com/api/conversations.list',
                         params=payload)
        r = r.json()
        channels.extend(r['channels'])
    
        next_cursor = r['response_metadata']['next_cursor']
        if len(next_cursor) == 0:
            break

    return channels

def get_channel_messages(channel, from_date, to_date, retry=20):
    latest = to_date
    oldest = from_date
    next_cursor = None

    messages = []
    retry_count = 10
    
    while True:
        payload={
            "token": SLACK_TOKEN,
            "channel": channel["id"],
            "latest": latest,
            "oldest": oldest
        }
        if next_cursor:
            payload['cursor'] = next_cursor

        r = {'ok': False}
        for i in range(retry_count):
            try:
                r = requests.get("https://slack.com/api/conversations.history", 
                                 params=payload)
                r = r.json()
                if r['ok'] == True:
                    break
            except requests.exceptions.RequestException as e:
                pass
        
        if r['ok'] == False:
            break
        
        messages.extend(r['messages'])
            
        if r['has_more'] == False:
            break
        else: 
            next_cursor = r['response_metadata']['next_cursor']

    return messages

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', '-o', type=str, default='log.json')
    args = parser.parse_args()

    output_filename = args.output
    
    users = get_user_list()
    channels = get_channel_list()
    
    today = date.today()
    
    messages = {}
    for channel in tqdm(channels):
        if channel['is_archived'] == False:
            messages[channel['id']] = get_channel_messages(channel,
                                            from_date=int(time.mktime((today - timedelta(60)).timetuple())),
                                            to_date=int(time.mktime(today.timetuple())))
    
    data = {'users': users,
            'channels': channels,
            'messages': messages}
    
    json.dump(data, open(output_filename, 'w'))    
