#!/usr/bin/python
import datetime
import time
from datetime import datetime
from dateutil import tz

# pip install requests PyJWT cryptography
import jwt
import requests
import json
from pathlib import Path

DEBUG                   = 1
USER_HOME_PATH          = str(Path('~').expanduser())
TZ_ZULU                 = tz.gettz('UTC')
TZ_LOCAL                = tz.gettz('America/Los_Angeles')


with open(USER_HOME_PATH + "/.ssh/AuthKey_LBV5W26ZRJ.p8", "r") as f:
  WEATHERKIT_KEY = str(f.read())

if DEBUG > 0:
  print("WEATHERKIT_KEY = " + str(WEATHERKIT_KEY))
  
WEATHERKIT_SERVICE_ID   = "net.ag6hq.sandysclock"  # Create service like (use same ending): com.example.weatherkit-client
WEATHERKIT_TEAM_ID      = "L7662C7KY6"
WEATHERKIT_KID          = "LBV5W26ZRJ"  # key ID
WEATHERKIT_FULL_ID      = f"{WEATHERKIT_TEAM_ID}.{WEATHERKIT_SERVICE_ID}"

GPS_LAT                 = 34.03139251897727
GPS_LON                 = -117.41704704143667

now                     = int(time.time())
currentTime             = datetime.fromtimestamp(now)
currentTime             = currentTime.astimezone(TZ_LOCAL)

print()
print(currentTime)

def fetch_weatherkit(
    lang="en",
    lat=GPS_LAT,
    lon=GPS_LON,
    country="US",
    timezone="US/Los_Angeles",
    # datasets = "currentWeather,forecastDaily,forecastHourly,forecastNextHour",
    datasets = "forecastDaily",
  ):
  
  url = f"https://weatherkit.apple.com/api/v1/weather/{lang}/{lat}/{lon}?dataSets={datasets}&countryCode={country}&timezone={timezone}"
  now = int(time.time())
  exp = now + (3600 * 24)

  token_payload = {
    "sub": WEATHERKIT_SERVICE_ID,
    "iss": WEATHERKIT_TEAM_ID,
    "exp": exp,
    "iat": now,
    "aud": "https://weatherkit.apple.com/api/v1",
  }
  token_header = {
    "kid": WEATHERKIT_KID,
    "id": WEATHERKIT_FULL_ID,
    "alg": "ES256",
    "typ": "JWT"
  }

  if DEBUG > 1:
    print("Header:")
    print(json.dumps(token_header,indent=2,default=str))
    print()
    print("Payload:")
    print(json.dumps(token_payload,indent=2,default=str))

  # token = jwt.encode(token_payload, WEATHERKIT_KEY, headers=token_header, algorithm="ES256").decode("utf-8")
  token = jwt.encode(token_payload, WEATHERKIT_KEY, "ES256", token_header)

  if DEBUG > 0:
    print()
    print('URL:')
    print(url)
    print()
    print('TOKEN:')
    print(token)

  if DEBUG > 0:
    print()
    print('CURL:')
    print('curl "' + url + '" --header ' + "'Authorization: " + f'Bearer {token}' + "'")

  response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
  if response.status_code != 200:
    print('Error retriving Apple WeatherKit REST API, Status: ' + str(response.status_code) + ' Reason: ' + str(response.json()['reason']))
    exit()
  return response

myFetch=fetch_weatherkit()
myStatus=myFetch.status_code
myJSON=myFetch.json()
myURL=myFetch.url
myHeaders=myFetch.headers
myRedirect=myFetch.is_redirect
myRequest=myFetch.request
if DEBUG > 1:
  if myStatus != 200:
    print("myJSON     = " + str(myJSON))
  print("myStatus   = " + str(myStatus))
  print("myRedirect = " + str(myRedirect))
  print("myURL      = " + str(myURL))
  print("myRequest  = " + str(myRequest))
  print("myHeaders  = " + str(myHeaders))

with open('wxKit.json','w') as jsonF:
  jsonF.write(json.dumps(myJSON,indent=2,default='str'))

forecastDaily = myJSON['forecastDaily']

for forecastDay in forecastDaily['days']:
  forecastTime = datetime.strptime(forecastDay['forecastStart'], '%Y-%m-%dT%H:%M:%SZ')
  forecastTime = forecastTime.astimezone(TZ_LOCAL)
  if forecastTime > currentTime:
     timeDifference = "ahead"
    #  print("ahead")
  else:
     timeDifference = "behind"
    #  print("behind")
  print(str(forecastTime) + " is " + timeDifference)