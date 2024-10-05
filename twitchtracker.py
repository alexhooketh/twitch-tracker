import requests
import time
import json

# Replace these with your own credentials
config = json.load(open('config.json'))
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
CHANNEL_ID = config["channel_id"]
MODERATOR_ID = config["moderator_id"]
REFRESH_TOKEN = config["refresh_token"]
TELEGRAM_BOT_TOKEN = config["telegram_bot_token"]
TELEGRAM_CHAT_ID = config["telegram_chat_id"]

log_file = open(str(time.time()) + ".txt", "w")

def get_chatters(access_token):
    url = 'https://api.twitch.tv/helix/chat/chatters'
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {access_token}'
    }
    params = {'broadcaster_id': CHANNEL_ID, 'moderator_id': MODERATOR_ID}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def refresh(refresh_token):
    url = 'https://id.twitch.tv/oauth2/token'
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token'
    }
    response = requests.post(url, data=data)
    return response.json()

def log(message):
    dated = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {message}"
    log_file.write(dated + "\n")
    log_file.flush()
    print(dated)

    # not dated because tg messages have date in them
    requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?text={message}&chat_id={TELEGRAM_CHAT_ID}")

def main():
    previous_chatters = set()

    access_token = None
    refresh_token = REFRESH_TOKEN

    while True:

        response = get_chatters(access_token)
    
        if response.get("status") == 401:
            log("Refreshing token")
            auth_data = refresh(refresh_token)
            access_token = auth_data["access_token"]
            refresh_token = auth_data["refresh_token"]
            log(str(auth_data))
            continue

        current_chatters = set([chatter["user_name"] for chatter in response["data"]])
    
        new_chatters = current_chatters - previous_chatters
        left_chatters = previous_chatters - current_chatters
        
        for chatter in new_chatters:
            log(f"{chatter} joined the stream")
        
        for chatter in left_chatters:
            log(f"{chatter} left the stream")
        
        previous_chatters = current_chatters
        
        time.sleep(30)  # Wait for 30 seconds before next check

if __name__ == "__main__":
    main()