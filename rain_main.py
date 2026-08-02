import requests
import os
# Download the helper library from https://www.twilio.com/docs/python/install
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
API_KEY = os.environ.get("API_KEY")
API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast?"
MY_PHONE = os.environ.get("MY_PHONE")
print(API_KEY)

params = {
    "lat": 34.871849,
    "lon": 138.258514,
    "cnt" : 4,
    "appid": API_KEY
}

with requests.get(API_ENDPOINT, params) as connection:
    connection.raise_for_status()
    data = connection.json()

def send_sms():
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    account_sid = TWILIO_ACCOUNT_SID  # os.environ["TWILIO_ACCOUNT_SID"]
    auth_token = TWILIO_AUTH_TOKEN  # os.environ["TWILIO_AUTH_TOKEN"]
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(to=f"+{MY_PHONE}", from_="+4915888620339", body="sms_account_alerts")
    print(message.status)

def bring_umbrella():
    """Returns true, if ut is needed (will precipitate)"""
    for weather in data["list"]:
        if weather["weather"][0]["id"] < 700:
            return True
    return False

if bring_umbrella():
    send_sms()

