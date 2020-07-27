import requests
import json
import sys

BOT_URL = "https://api.telegram.org/bot*******/"
MY_ID = "****"

def after_start():
    url = BOT_URL + "getUpdates?offset=-1"
    response = requests.get(url)
    last_msg = response.json()['result'][0]['message']['message_id']
    return last_msg

def send_request(user_id, text):
    url = BOT_URL + "sendMessage?chat_id=" + user_id + "&text=" + text + "&parse_mode=HTML"
    response = requests.get(url)
    if response.status_code == 200:
        print("Success!")
    else:
        print("Error!")
        sys.exit()

def receive_request():
    url = BOT_URL + "getUpdates?offset=-1"
    response = requests.get(url)
    source_id = response.json()['result'][0]['message']['from']['id']
    text = response.json()['result'][0]['message']['text']
    id_msg = response.json()['result'][0]['message']['message_id']
    try:
        entities = response.json()['result'][0]['message']['entities'][0]['type']
        if entities == "bold":
            text = "<b>" + text + "</b>"
        elif entities == "italic":
            text = "<i>" + text + "</i>"
    except KeyError:
        pass
    return source_id, text, id_msg

if __name__ == "__main__":
    id_last_msg = after_start()
    while True:
        user_id, text, message_id = receive_request()
        if message_id != id_last_msg:
            send_request(str(user_id), text)
            id_last_msg = message_id

