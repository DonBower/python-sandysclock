import os
import json
import weatherkit

# Load the credentials from wherever you store them securely
team_id = os.environ.get('APPLE_TEAM_ID')
key_id = os.environ.get('APPLE_KEY_ID')
service_id = os.environ.get('APPLE_SERVICE_ID')
private_key = os.environ.get('APPLE_PRIVATE_KEY')

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
print(forecasts_json['forecast_daily'][0]['conditions'])

with open('wxKitPython.json','w') as jsonF:
  jsonF.write(json.dumps(forecasts_json, indent=2, default='str'))