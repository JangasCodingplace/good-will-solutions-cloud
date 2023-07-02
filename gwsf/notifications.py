import requests

from . import configs


def send_discord_notifications(message: str):
    data = {"content": message}
    response = requests.post(configs.DISCORD_WEBHOOK, data=data)
    return response.status_code, response.text
