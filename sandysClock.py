#!/usr/bin/python
import json
import time
import jwt
import requests
import os.path

import PySimpleGUI as sg
from datetime import datetime
from dateutil import tz

from ambient_api.ambientapi import AmbientAPI
from pathlib import Path
#
# Constants
#
DEBUG                   = 0
USER_HOME_PATH          = str(Path('~').expanduser())
TZ_ZULU                 = tz.gettz('UTC')
TZ_LOCAL                = tz.gettz('America/Los_Angeles')
DIM_HOUR_NIGHT          = 15
DIM_HOUR_DAY            = 7
DIM_BRIGHTNESS_NIGHT    = 31
DIM_BRIGHTNESS_DAY      = 255
DIM_BRIGHTNESS_FILE     = '/sys/devices/platform/soc/3f205000.i2c/i2c-11/i2c-10/10-0045/backlight/10-0045/brightness'
CLOCK_FONT_TIME_SIZE    = 192
CLOCK_FONT_TIME_NAME    = 'Digital-7 Mono'
CLOCK_FONT_TIME_SIZE    = 128
CLOCK_FONT_TIME_NAME    = 'Helvetica'
CLOCK_FONT_HOUR_SIZE    = 36
CLOCK_FONT_HOUR_NAME    = 'Helvetica'
GPS_LAT                 = 34.03139251897727
GPS_LON                 = -117.41704704143667
with open(USER_HOME_PATH + "/.ssh/AuthKey_LBV5W26ZRJ.p8", "r") as f:
  WEATHERKIT_KEY        = f.read()
WEATHERKIT_SERVICE_ID   = "net.ag6hq.sandysclock"  # Create service like (use same ending): com.example.weatherkit-client
WEATHERKIT_TEAM_ID      = "L7662C7KY6"
WEATHERKIT_KID          = "LBV5W26ZRJ"  # key ID
WEATHERKIT_FULL_ID      = f"{WEATHERKIT_TEAM_ID}.{WEATHERKIT_SERVICE_ID}"
awnAPI                  = AmbientAPI()
awnDevices              = awnAPI.get_devices()
try:
  AWN_DEVICE            = awnDevices[0]
except:
  print('Could not get AWN Devices')
  print(awnDevices)
  exit()
TEMP_AS_F               = 'ºF'
TEMP_AS_C               = 'ºC'
TEMP_AS_DEFAULT         = TEMP_AS_F
time.sleep(1)
theme_dict              = {
  'BACKGROUND': '#2B475D',
  'TEXT': '#FFFFFF',
  'INPUT': '#F2EFE8',
  'TEXT_INPUT': '#000000',
  'SCROLL': '#F2EFE8',
  'BUTTON': ('#000000', '#C2D4D8'),
  'PROGRESS': ('#FFFFFF', '#C7D5E0'),
  'BORDER': 1,'SLIDER_DEPTH': 0,
  'PROGRESS_DEPTH': 0
}

BORDER_COLOR            = '#C7D5E0'
DARK_HEADER_COLOR       = '#1B2838'
BPAD_TOP                = ((20,20), (20, 10))
BPAD_LEFT               = ((20,10), (0, 10))
BPAD_LEFT_INSIDE        = (0, 10)
BPAD_RIGHT              = ((10,20), (10, 20))

def cToF(c):
  f = ((9/5) * c) + 32
  return f'{f:.1f}'

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def columnFixedSize(layout, size=(None, None), *args, **kwargs):
  # An addition column is needed to wrap the column with the Sizers because the colors will not be set on the space the sizers take
  return sg.Column([[sg.Column([[sg.Sizer(0,size[1]-1), sg.Column([[sg.Sizer(size[0]-2,0)]] + layout, *args, **kwargs, pad=(0,0))]], *args, **kwargs)]],pad=(0,0))

def getRightNow():
    rightNow=datetime.now()
    return rightNow

def getCurrentDate(rightNow):
  currentDateString = custom_strftime('%A, %B {S}, %Y', rightNow)
  return currentDateString

def getCurrentTime(rightNow):
  currentTimeString = rightNow.strftime('%H:%M')
  return currentTimeString

def getAMText(rightNow):
  if rightNow.strftime('%p') == "AM":
    amTextValue="AM"
  else:
    amTextValue=""
  return amTextValue

def getPMText(rightNow):
  if rightNow.strftime('%p') == "PM":
    pmTextValue="PM"
  else:
    pmTextValue=""
  return pmTextValue

def getCurrentWx(AWN_DEVICE):
  global lastEpoch, wxInfo, wxKitInfo, wxKitForecastTime
  wxResponse    = requests.get("https://api.weather.gov/gridpoints/SGX/56,72/forecast")
  currentEpoch  = int(time.time())
  if DEBUG > 1:
    print(currentEpoch)

  currentTime   = datetime.fromtimestamp(currentEpoch)
  currentTime   = currentTime.astimezone(TZ_LOCAL)
  if DEBUG > 1:
    print(currentTime)

  if currentTime > wxKitForecastTime:
    wxKitInfo           = getWxKit()
    wxKitForecastTime   = datetime.strptime(wxKitInfo.json()['forecastDaily']['days'][0]['forecastEnd'], '%Y-%m-%dT%H:%M:%SZ')
    wxKitForecastTime   = wxKitForecastTime.astimezone(TZ_LOCAL)
    if DEBUG > 1:
      print(str(currentTime) + " is later than " + str(wxKitForecastTime))
  else:
    if DEBUG > 1:
      print("Next wxKit Retrival is: " + str(wxKitForecastTime))

  if int(lastEpoch + 600) < currentEpoch:
    if DEBUG > 1:
      print("we have time: " + str(lastEpoch + 600) + " < " + str(currentEpoch))
    wxInfo      = {}
    awnData     = AWN_DEVICE.get_data()
    lastEpoch   = currentEpoch

    if DEBUG > 1:
      print("awnData:")
      print(awnData)
      print()
      with open('wxAWN.json','w') as jsonF:
        jsonF.write(json.dumps(awnData,indent=2,default='str'))


    if DEBUG > 1:
      wxJSON = wxResponse.json()

      with open('wxGov.json','w') as jsonF:
        jsonF.write(json.dumps(wxJSON,indent=2,default='str'))

    wxInfo['time']    = currentEpoch
    wxInfo['current'] = awnData[0]['tempf']

    if wxKitInfo.status_code == 200:
      wxInfo['low']   = cToF(wxKitInfo.json()['forecastDaily']['days'][0]['temperatureMin'])
      wxInfo['high']  = cToF(wxKitInfo.json()['forecastDaily']['days'][0]['temperatureMax'])
    else:
      wxInfo['low']   = wxJSON['properties']['periods'][1]['temperature']
      wxInfo['high']  = wxJSON['properties']['periods'][0]['temperature']

    wxInfo['rain']    = {}
    wxInfo['rain']['probability'] = 100

    if DEBUG > 1:
      print(wxInfo)
      with open('wxInfo.json','w') as jsonF:
        jsonF.write(json.dumps(wxInfo,indent=2,default='str'))
  return wxInfo

def getCurrentTemp(wxInfo):
  currentTempValue = float(wxInfo['current'])
  return f'{currentTempValue:.1f}' + TEMP_AS_DEFAULT

def getHighTemp(wxInfo):
  currentTempValue = float(wxInfo['high'])
  return f'{currentTempValue:.1f}' + TEMP_AS_DEFAULT

def getLowTemp(wxInfo):
  currentTempValue = float(wxInfo['low'])
  return f'{currentTempValue:.1f}' + TEMP_AS_DEFAULT

def setDateText(currentDateString):
  currentDate = sg.Text(
    currentDateString,
    font=('Helvetica', 42),
    justification='center',
    text_color='#000000',
    background_color='#FF7F7F',
    key='currentDate'
  )
  return currentDate

def setTimeText(currentTimeString):
  currentTime = sg.Text(
    currentTimeString,
    justification='center',
    font=(CLOCK_FONT_TIME_NAME, CLOCK_FONT_TIME_SIZE),
    text_color='#FFFB00',
    background_color='#000000',
    key='currentTime',
  )
  return currentTime

def setAMText(amTextValue):
  amText = sg.Text(
    amTextValue,
    font=(CLOCK_FONT_HOUR_NAME, CLOCK_FONT_HOUR_SIZE),
    size=(100, 100),
    text_color='#FFFB00', 
    background_color='#0000FF',
    key='amText'
  )
  return amText

def setPMText(pmTextValue):
  pmText = sg.Text(
    pmTextValue,
    font=('Helvetica',48),
    size=(100, 100),
    text_color='#FFFB00', 
    background_color='#0000FF',
    key='pmText'
  )
  return pmText

def setCurrentTemp(currentTempValue):
  currentTemp = sg.Text(
    currentTempValue,
    font=('Helvetica',54),
    text_color='#000000', 
    background_color='#00FF00',
    key='currentTemp'
  )
  return currentTemp

def setLowTemp(lowTempValue):
  lowTemp = sg.Text(
    lowTempValue,
    font=('Helvetica',36),
    text_color='#000000', 
    background_color='#00FF00',
    key='lowTemp'
  )
  return lowTemp

def setHighTemp(highTempValue):
  highTemp = sg.Text(
    highTempValue,
    font=('Helvetica',36),
    text_color='#000000', 
    background_color='#00FF00',
    key='highTemp'
  )
  return highTemp

def getWxKit(
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

  token = jwt.encode(token_payload, WEATHERKIT_KEY, headers=token_header, algorithm="ES256")
  if DEBUG > 1:
    print('token:')
    print(token)
    
  response = requests.get(url, headers={'Authorization': f'Bearer {token}'})
 
  if DEBUG > 1:
    with open('wxKit.json','w') as jsonF:
      jsonF.write(json.dumps(response.json(),indent=2,default='str'))

  return response

"""
    Sandy's Clock using blocks of information.
    Inspired by 2020 Dashboard PySimpleGUI.org
    Copyright 2023 ag6hq.net
"""
#
# Initalize Program
#
rightNow              = getRightNow()
lastEpoch             = int(time.time()-601)
wxInfo                = {}
wxKitForecastTime     = datetime.fromtimestamp(lastEpoch)
wxKitForecastTime     = wxKitForecastTime.astimezone(TZ_LOCAL)
wxInfo                = getCurrentWx(AWN_DEVICE)
currentBrightness     = DIM_BRIGHTNESS_DAY

sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

if DEBUG > 0:
  print("Version Info: \n" + sg.main_get_debug_data())
  # print(sg.sys.version)

exitButton = [[sg.Button('Exit')]]

amPMLayout = [
  [
    sg.Frame(
      layout=[
        [
          setAMText(getAMText(rightNow))
        ],
      ],
      title=None,
      title_color='#0000FF',
      background_color='#0000FF',
      size=(100,100),
      element_justification='center',
      vertical_alignment='center',
      border_width=None,
      pad=(0,0)
    ),
  ],
  [
    sg.Frame(
      layout=[
        [
          setPMText(getPMText(rightNow))
        ],
      ], 
      title=None, 
      title_color='#0000FF', 
      background_color='#0000FF', 
      size=(100,100),
      element_justification='center', 
      vertical_alignment='center', 
      border_width=None,
      pad=(0,0)
    ),
  ]
]

tempLayout = [
  [
    sg.Frame(
      layout=[
        [
          setCurrentTemp(getCurrentTemp(wxInfo))
        ],
      ],
      title='Current', 
      size=(250,100),
      title_color='#0000FF',
      background_color='#FFFF7F',
      element_justification='center',
      vertical_alignment='center',
      border_width=None,
      pad=(0,0)
    ),
  ],
  [
    sg.Frame(
      layout=[
        [
          setLowTemp(getLowTemp(wxInfo))
        ],
      ],
      title='low',
      size=(125,100),
      title_color='#000000',
      background_color='#FFFF7F',
      element_justification='center',
      vertical_alignment='center',
      border_width=None,
      pad=(0,0)
    ),
    sg.Frame(
      layout=[
        [
          setHighTemp(getHighTemp(wxInfo))
        ],
      ],
      title='high',
      size=(125,100),
      title_color='#000000',
      background_color='#FFFF7F',
      element_justification='center',
      vertical_alignment='center',
      border_width=None,
      pad=(0,0)
    ),
  ],
]

dateColumn = sg.Column(
  [
    [
      setDateText(getCurrentDate(rightNow))
    ]
  ],
  size=(800, 75),
  pad=(0,0),
  background_color='#FF7F7F',
  element_justification='center',
  justification='center',
  vertical_alignment='center',
)

timeColumn = sg.Column(
  [
    [
      setTimeText(getCurrentTime(rightNow))
    ]
  ], 
  size=(450, 200), 
  pad=(0,0), 
  background_color='#0000FF',
  vertical_alignment='center',
  element_justification='center',
  justification='center'
)

amPMColumn = sg.Column(
  amPMLayout, 
  size=(100, 200),
  pad=(0,0),
  background_color='#00007F'
)

tempColumn = sg.Column(
  tempLayout, 
  size=(250, 200), 
  pad=(0,0), 
  background_color='#00FF00'
) 

dateRow = [
  [
    dateColumn
  ]
]

timeRow = [
  [
    timeColumn,
    amPMColumn,
    tempColumn,
  ]
]

buttonRow = [
  [
    sg.Column(
      [
        [
          sg.Column(
            exitButton, 
            size=(75,25),  
            pad=(0,0)
          )
        ]
      ], 
      pad=(0,0), 
      background_color=BORDER_COLOR
    ),
  ]
]


layout = [
  dateRow,
  timeRow,
  buttonRow
]


window = sg.Window(
  'Dashboard PySimpleGUI-Style',
  layout,
  size=(800,480),
  margins=(0,0),
  background_color=BORDER_COLOR,
  no_titlebar=True,
  grab_anywhere=False
)

def setBrightness(thisSetting):
  if os.path.exists(DIM_BRIGHTNESS_FILE):
    with open(DIM_BRIGHTNESS_FILE, 'w') as f:
      f.write(thisSetting)


while True:             # Event Loop
  rightNow          = getRightNow()
  thisHour          = int(rightNow.strftime('%H'))
  if thisHour >= DIM_HOUR_NIGHT:
    if currentBrightness != DIM_BRIGHTNESS_NIGHT:
      setBrightness(DIM_BRIGHTNESS_NIGHT)
      currentBrightness = DIM_BRIGHTNESS_NIGHT
  else:
    if thisHour >= DIM_HOUR_DAY:
      if currentBrightness != DIM_BRIGHTNESS_DAY:
        setBrightness(DIM_BRIGHTNESS_DAY)
        currentBrightness = DIM_BRIGHTNESS_DAY

  wxInfo            = getCurrentWx(AWN_DEVICE)
#
# Sync clock to exact second
#
  currentEpoch      = time.time()
  timeout           = (1 - (currentEpoch - int(currentEpoch))) * 1000
 
  event, values = window.read(timeout=timeout,timeout_key = "__TIMEOUT__")

  if event == "__TIMEOUT__":
    window['currentTime'].update(str(getCurrentTime(rightNow)))
    window.refresh()

  if event == sg.WIN_CLOSED or event == 'Exit':
    break


window.close()