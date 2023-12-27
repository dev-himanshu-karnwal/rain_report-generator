from twilio.rest import Client
from datetime import datetime, timedelta
import requests
API_KEY = "API_KEY"
LATITUDE = 30.168085
LONGITUDE = 77.296921
TWILIO_ID = "TWILIO_ID"
TWILIO_AUTH_TOKEN = "TWILIO_AUTH_TOKEN"


def get_rain_amount(rain_vol: int) -> str:
    if rain_vol < 0.5:
        return 'Slight Rain'
    elif rain_vol < 4:
        return 'Moderate Rain'
    elif rain_vol < 8:
        return 'Heavy Rain'
    else:
        return 'Very Heavy Rain'


def get_shower_amount(rain_vol: int) -> str:
    if rain_vol < 2:
        return 'Slight Shower'
    elif rain_vol < 10:
        return 'Moderate Shower'
    elif rain_vol < 50:
        return 'Heavy Shower'
    else:
        return 'Voilent Shower'


res = requests.get(
    f'https://api.openweathermap.org/data/2.5/forecast?lat={LATITUDE}&lon={LONGITUDE}&appid={API_KEY}')
res.raise_for_status()

weather_data = res.json()

mesaage_body = "Today's Rain report:\n"

will_rain = False

for i in range(0, 8):
    three_hr_weather_data = weather_data["list"][i]

    if three_hr_weather_data.get('rain'):
        will_rain = True
        # creating message
        start_time = datetime.strptime(
            three_hr_weather_data["dt_txt"], '%Y-%m-%d %H:%M:%S') + timedelta(hours=5, minutes=30)
        end_time = start_time+timedelta(hours=3)
        rain_volume = three_hr_weather_data["rain"]["3h"]

        rain_amount = get_rain_amount(rain_vol=rain_volume)
        shower_amount = get_shower_amount(rain_vol=rain_volume)

        mesaage_body += f'{start_time} to {end_time} -> {rain_amount} & {shower_amount}({rain_volume}mm rain)\n'


if will_rain:

    print(mesaage_body)
    # Sending message
    client = Client(TWILIO_ID, TWILIO_AUTH_TOKEN)

    message = client.messages \
                    .create(
                        body=mesaage_body,
                        from_='+15735273640',
                        to='+918222869464'
                    )

    print(message.status)
