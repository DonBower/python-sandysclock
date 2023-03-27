import os
import json
import weatherkit

# Load the credentials from wherever you store them securely
team_id = os.environ.get('APPLE_TEAM_ID')
key_id = os.environ.get('APPLE_KEY_ID')
service_id = os.environ.get('APPLE_SERVICE_ID')
private_key = os.environ.get('APPLE_PRIVATE_KEY')

curl "https://weatherkit.apple.com/api/v1/weather/en/34.031392/-117.41704?dataSets=forecastDaily&countryCode=US&timezone=US/Los_Angeles" \
  --header 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IkxCVjVXMjZaUkoiLCJpZCI6Ikw3NjYyQzdLWTYubmV0LmFnNmhxLnNhbmR5c2Nsb2NrIn0.eyJzdWIiOiJuZXQuYWc2aHEuc2FuZHlzY2xvY2siLCJpc3MiOiJMNzY2MkM3S1k2IiwiZXhwIjoxNjc5OTg2ODU3LCJpYXQiOjE2Nzk5MDA0NTcsImF1ZCI6Imh0dHBzOi8vd2VhdGhlcmtpdC5hcHBsZS5jb20vYXBpL3YxIn0.dzurOGHSE61Q2fipqn4wvFHSSLZc1l5geD1QDLO9WdFDiegUBO0lX2ehNYZNMTzyJjt3v-msibSrgbyJbVE8XA'

# Instantiate the WeatherKit object
wk_client = weatherkit.WeatherKit(team_id, service_id, private_key, key_id)

# Include any/all of the datasets we want to pull in the list
datasets = [
    'forecastHourly',
    'forecastDaily',
    'currentWeather',
    'forecastNextHour',
]

# Fetch the API
forecasts = wk_client.fetch(datasets, 39.5900, -104.726763, 'US', 'US/Mountain')

# There is a convenience method for converting the forecast response object to JSON
forecasts_json = forecasts.as_json()

with open('wxKitPython.json','w') as jsonF:
  jsonF.write(json.dumps(forecasts_json, indent=2, default='str'))