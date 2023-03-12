#!/usr/local/bin/python
import PySimpleGUI as sg
from datetime import datetime

from datetime import datetime as dt

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def getCurrentTime():
  global currentDayString, currentTimeString, amTextValue, pmTextValue

  rightNow          = datetime.now()
  currentDayString  = custom_strftime('%A, %B {S}, %Y', rightNow)
  currentTimeString = rightNow.strftime('%I:%M')
  currentTimeSet    = rightNow.strftime('%p')
  if currentTimeSet == "PM":
    amTextValue=""
    pmTextValue="PM"
  else:
    amTextValue="AM"
    pmTextValue="  "

  setTimeFrame()

def setTimeFrame():
  global currentTime, currentDayString
  currentTime = sg.Text(
    currentTimeString,
    justification='center',
    font=('Digital-7 Mono', 144),
    text_color='#FFFB00',
    background_color='#0000FF'
  )


# print custom_strftime('%B {S}, %Y', dt.now())

"""
    Dashboard using blocks of information.

    Copyright 2020 PySimpleGUI.org
"""
while True:             # Event Loop
  getCurrentTime()


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

  getCurrentTime()


      
  exitButton = [[sg.Button('Exit')]]

  currentTempValue='104º'
  lowTempValue='101º'
  highTempValue='113º'

  currentDay = sg.Text(
    currentDayString,
    font=('Helvetica', 42),
    justification='center',
    text_color='#000000',
    background_color='#FF7F7F'
  )


  currentTemp = sg.Text(
    currentTempValue,
    font=('Helvetica',54),
    text_color='#000000', 
    background_color='#00FF00'
  )

  lowTemp = sg.Text(
    lowTempValue,
    font=('Helvetica',36),
    text_color='#000000', 
    background_color='#00FF00'
  )

  highTemp = sg.Text(
    highTempValue,
    font=('Helvetica',36),
    text_color='#000000', 
    background_color='#00FF00'
  )


  amText = sg.Text(
    amTextValue,
    font=('Helvetica',48),
    text_color='#FFFB00', 
    background_color='#0000FF',
  )

  pmText = sg.Text(
    pmTextValue,
    font=('Helvetica',48),
    text_color='#FFFB00', 
    background_color='#0000FF',
  )

  amPMLayout = [
    [
      sg.Frame(
        layout=[
          [
            amText
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
            pmText
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


  column3 = sg.Frame(
    layout=[
    [
      sg.Text('103º', font=('Helvetica',54), text_color='#000000', background_color='#FFFF7F')
    ],
    ], 
    title='Current', 
    size=(240,100), 
    title_color='#0000FF', 
    background_color='#FFFF7F', 
    element_justification='center', 
    vertical_alignment='center', 
    border_width=None, 
    pad=(0,0)
  )

  tempLayout = [
    [
      sg.Frame(
        layout=[
        [
          currentTemp
        ],
      ], title='Current', size=(240,100), title_color='#0000FF', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
    ],
    [
      sg.Frame(layout=[
        [
          lowTemp
        ],
      ], title='low', size=(120,100), title_color='#000000', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
      sg.Frame(layout=[
        [
          highTemp
        ],
      ], title='high', size=(120,100), title_color='#000000', background_color='#FFFF7F', element_justification='center', vertical_alignment='center', border_width=None, pad=(0,0)),
    ],
  ]

  currentDayColumn = sg.Column(
    [
      [
        currentDay
      ]
    ],
    size=(700, 75),
    pad=(0,0),
    background_color='#FF7F7F',
    justification='center',
    vertical_alignment='center',
  )

  timeColumn = sg.Column(
    [
      [
        currentTime
      ]
    ], 
    size=(350, 200), 
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

  row1 = [
    currentDayColumn
  ]

  row2 = [
    [
      timeColumn,
      amPMColumn,
      tempColumn,
    ]
  ]

  row3 = [
    [sg.Column([[sg.Column(exitButton, size=(75,25),  pad=(0,0))]], pad=(0,0), background_color=BORDER_COLOR),]
  ]

  layout = [
    row1,
    row2,
    row3
  ]


  window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0,0), background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)


  event, values = window.read(timeout=1000)
  if event == sg.WIN_CLOSED or event == 'Exit':
    break


window.close()