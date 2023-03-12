#!/usr/local/bin/python
import PySimpleGUI as sg
from datetime import datetime

from datetime import datetime as dt

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def getRightNow():
    rightNow=datetime.now()
    return rightNow

def getCurrentDate(rightNow):
  currentDateString = custom_strftime('%A, %B {S}, %Y', rightNow)
  return currentDateString

def getCurrentTime(rightNow):
  currentTimeString = rightNow.strftime('%M:%S')
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

def getCurrentTemp():
  currentTempValue = '109º'
  return currentTempValue

def getHighTemp():
  highTempValue = '129º'
  return highTempValue

def getLowTemp():
  lowTempValue = '101º'
  return lowTempValue

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
    font=('Digital-7 Mono', 128),
    text_color='#FFFB00',
    background_color='#0000FF',
    key='currentTime'
  )
  return currentTime

def setAMText(amTextValue):
  amText = sg.Text(
    amTextValue,
    font=('Helvetica',48),
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


# print custom_strftime('%B {S}, %Y', dt.now())

"""
    Dashboard using blocks of information.

    Copyright 2020 PySimpleGUI.org
"""
rightNow = getRightNow()

theme_dict = {'BACKGROUND': '#2B475D',
                'TEXT': '#FFFFFF',
                'INPUT': '#F2EFE8',
                'TEXT_INPUT': '#000000',
                'SCROLL': '#F2EFE8',
                'BUTTON': ('#000000', '#C2D4D8'),
                'PROGRESS': ('#FFFFFF', '#C7D5E0'),
                'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 10)
BPAD_RIGHT = ((10,20), (10, 20))

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
        setCurrentTemp(getCurrentTemp())
      ],
    ], title='Current', size=(250,100), title_color='#0000FF', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
  ],
  [
    sg.Frame(layout=[
      [
        setLowTemp(getLowTemp())
      ],
    ], title='low', size=(125,100), title_color='#000000', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
    sg.Frame(layout=[
      [
        setHighTemp(getHighTemp())
      ],
    ], title='high', size=(125,100), title_color='#000000', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
  ],
]

currentDateColumn = sg.Column(
  [
    [
      setDateText(getCurrentDate(rightNow))
    ]
  ],
  size=(800, 75),
  pad=(0,0),
  background_color='#FF7F7F',
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
  background_color='#0000FF'
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
  setDateText(getCurrentDate(rightNow))
]

timeRow = [
  [
    timeColumn,
    amPMColumn,
    tempColumn,
  ]
]

buttonRow = [
  [sg.Column([[sg.Column(exitButton, size=(75,25),  pad=(0,0))]], pad=(0,0), background_color=BORDER_COLOR),]
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


while True:             # Event Loop
  rightNow = getRightNow()
  
  event, values = window.read(timeout=1000,timeout_key = "__TIMEOUT__")

  if event == "__TIMEOUT__":
    window['currentTime'].update(str(getCurrentTime(rightNow)))
    window.refresh()

  if event == sg.WIN_CLOSED or event == 'Exit':
    break


window.close()