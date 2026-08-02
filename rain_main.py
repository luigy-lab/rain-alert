import os

import requests
from twilio.rest import Client


TWILIO_ACCOUNT_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("AUTH_TOKEN")
API_KEY = os.environ.get("API_KEY")
MY_PHONE = os.environ.get("MY_PHONE")
TEST_MODE = os.environ.get("TEST_MODE", "false").lower() == "true"

API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
TWILIO_PHONE_NUMBER = "+4915888620339"


required_variables = {
    "ACCOUNT_SID": TWILIO_ACCOUNT_SID,
    "AUTH_TOKEN": TWILIO_AUTH_TOKEN,
    "API_KEY": API_KEY,
    "MY_PHONE": MY_PHONE,
}

missing_variables = [
    name
    for name, value in required_variables.items()
    if not value
]

if missing_variables:
    raise RuntimeError(
        "Missing environment variables: "
        + ", ".join(missing_variables)
    )


params = {
    "lat": 34.871849,
    "lon": 138.258514,
    "cnt": 4,
    "appid": API_KEY,
}


def get_weather_data():
    response = requests.get(
        API_ENDPOINT,
        params=params,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()


def bring_umbrella(weather_data):
    """Return True if precipitation is forecast."""

    for forecast in weather_data["list"]:
        weather_id = forecast["weather"][0]["id"]

        if weather_id < 700:
            return True

    return False


def send_sms(message_body):
    phone_number = MY_PHONE.strip()

    if not phone_number.startswith("+"):
        phone_number = f"+{phone_number}"

    client = Client(
        TWILIO_ACCOUNT_SID,
        TWILIO_AUTH_TOKEN,
    )

    message = client.messages.create(
        to=phone_number,
        from_=TWILIO_PHONE_NUMBER,
        body=message_body,
    )

    print(f"SMS status: {message.status}")


def main():
    weather_data = get_weather_data()

    if TEST_MODE:
        send_sms(
            "Test successful: the GitHub rain alert workflow is working."
        )
        return

    if bring_umbrella(weather_data):
        send_sms(
            "Bring an umbrella. Precipitation is forecast."
        )
    else:
        print("No precipitation is forecast. No SMS was sent.")


if __name__ == "__main__":
    main()
