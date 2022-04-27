import tweepy
import requests
import datetime
import time
import os
from keep_alive import keep_alive
consumer_key= os.environ['consumer_key']
consumer_secret = os.environ['consumer_secret']

key = os.environ['key']
secret = os.environ['secret']

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(key,secret)

api = tweepy.API(auth)
def eq():
    response = requests.get('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson')
    currID = ''
    i_val = 0
    gotIt = False
    i = 0
    for earthquake in reversed(response.json()['features']):
        file = open('prevID.txt','r')
        prevID = file.read().strip()
        file.close()
        if earthquake['type'] == 'Feature':
            if not gotIt:
                i_val += 1
            if prevID == earthquake['id']:
                gotIt = True
        i += 1
    if gotIt == False:
        i_val = -1
    i = 0
    e_list = response.json()['features']
    if prevID != e_list[0]['id']:
        for earthquake in reversed(response.json()['features']):
            if earthquake['type'] == 'Feature':
                file = open('prevID.txt','r')
                prevID = file.read().strip()
                file.close()
                if prevID == earthquake['id']:
                    break
                target_time_ms = earthquake['properties']['time']
                base_datetime = datetime.datetime(1970,1,1)
                delta = datetime.timedelta(0,0,0,target_time_ms)
                target_date = base_datetime+delta
                print(earthquake['id'])
                if i > i_val:
                    print('am here')
                    try:
                        api.update_status('There was a '+str(earthquake['properties']['mag'])+' magnitude earthquake '+str(earthquake['properties']['place']))
                        time.sleep(10)
                    except tweepy.TweepyException as e:
                        print(e.response)
                        time.sleep(10)
            i += 1
        features = response.json()['features']
        currID = features[0]['id']
        print('finalID:' +str(currID))
        f = open('prevID.txt','w')
        f.write(currID)
        f.close
keep_alive()
while True:
    eq()
    time.sleep(10)