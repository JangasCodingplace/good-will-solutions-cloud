from datetime import datetime

import requests

from .configs import DISCORD_WEBHOOK_URL
from .functions import CreditApplication


def send_discord_notifications(message: str):
    data = {"content": message}
    response = requests.post(DISCORD_WEBHOOK_URL, data=data)
    return response.status_code, response.text


def get_service_message(application: CreditApplication) -> str:
    message = (
        f"New Application received from {application.last_name}, {application.first_name} \n"
        f"amount: {application.amount}"
    )
    return message


def get_supervisor_message(applications: list[CreditApplication]):
    first_name = applications[0].first_name
    last_name = applications[0].last_name
    application_list = [
        (
            f"{datetime.fromtimestamp(application.timestamp).strftime('%Y-%m-%d')}"
            f" - amount: {application.amount}"
        )
        for application in applications
    ]
    date_str = "\n".join(application_list)
    message = f"New Application received from {last_name}, {first_name} \n{date_str}"
    return message
