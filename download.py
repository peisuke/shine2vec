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
    r = requests.get('https://slack.com/api/users.list',
                     params={'token': SLACK_TOKEN})
    return r.json()['members']


def get_channel_list():
    r = requests.get('https://slack.com/api/channels.list',
                     params={'token': SLACK_TOKEN})
    return r.json()['channels']


def get_channel_messages(channel, from_date, to_date, retry=20):
    latest = to_date
    oldest = from_date
    has_more = True
    messages = []
    while(has_more):
        payload={
            "token": SLACK_TOKEN,
            "channel": channel["id"],
            "latest": latest,
            "oldest": oldest
        }
        for i in range(retry):
            try:
                r = requests.get("https://slack.com/api/channels.history", params=payload)
            except BaseError as e:
                t, v, tb = sys.exc_info()
                print(traceback.format_exception(t,v,tb))
                print(traceback.format_tb(e.__traceback__))
                
            if r.status_code == 429:
                sleep_time = int(r.headers["Retry-After"])
                time.sleep(sleep_time)
                continue
            else:
                break
        else:
            print('cannot load channel history')
            print(payload)
            continue
        d = r.json()
        messages += d['messages']
        has_more =  'has_more' in d and d['has_more']
        if has_more:
            latest = int(float(d["messages"][-1]["ts"]))
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
