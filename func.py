
import requests

def check_file(filename):
    allowed_file = ['png', 'jpg', 'jpeg', 'gif']
    if filename.split(".")[-1] in allowed_file:
        return True
    return False

def call_tg(text):
    url = "https://api.telegram.org/bot8581676217:AAG7_CEJDyiAbwGp-q5ENxe-GCeU7FzzDNM/sendMessage"
    payload = {
        "text": text,
        "chat_id": 1660164169
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }
    return requests.post(url, json=payload, headers=headers)
