import requests
import time
import json
from twitchAPI.twitch import Twitch

# Replace these with your own credentials
config = json.load(open('config.json'))
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
CHANNEL_NAME = config["channel_name"]

# Initialize Twitch API
twitch = Twitch(CLIENT_ID, CLIENT_SECRET)
twitch.authenticate_app([])

def get_chatters(channel):
    url = f'https://tmi.twitch.tv/group/user/{channel}/chatters'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return set(data['chatters']['viewers'])
    return set()

def main():
    previous_chatters = set()
    
    while True:
        current_chatters = get_chatters(CHANNEL_NAME)
        
        new_chatters = current_chatters - previous_chatters
        left_chatters = previous_chatters - current_chatters
        
        for chatter in new_chatters:
            print(f"{chatter} joined the stream")
        
        for chatter in left_chatters:
            print(f"{chatter} left the stream")
        
        previous_chatters = current_chatters
        
        time.sleep(60)  # Wait for 60 seconds before next check

if __name__ == "__main__":
    main()