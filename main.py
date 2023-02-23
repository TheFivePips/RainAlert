import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
api_key = os.environ.get("API_KEY")

weather_params = {
    "lon": -80.8431,
    "lat": 35.2271,
    "appid": api_key
}


url = "https://api.openweathermap.org/data/2.5/forecast?"
response = requests.get(url, params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data["list"][:5]

will_rain = False

for tri_hour_data in weather_slice:
    condition_code = tri_hour_data["weather"][0]["id"]
    if condition_code < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's going to rain today. Bring an umbrella",
        from_='+18446791169',
        to=os.environ.get("MY_NUMBER")
    )
    print(message.status)
else:
    print("it will not rain")
