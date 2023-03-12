#!/usr/local/bin/python
import PySimpleGUI as sg
from datetime import datetime
import json

def getCurrentTime():
  rightNow          = datetime.now()
  currentTimeString = rightNow.strftime('%M:%S')
  return currentTimeString

def setTimeText(currentTimeString):
  currentTime = sg.Text(
    currentTimeString,
    justification='center',
    font=('Digital-7 Mono', 144),
    text_color='#FFFB00',
    background_color='#0000FF',
    key='currentTime'
  )
  return currentTime


# print custom_strftime('%B {S}, %Y', dt.now())

"""
    Dashboard using blocks of information.

    Copyright 2020 PySimpleGUI.org
"""


theme_dict = {
  'BACKGROUND': '#2B475D',
  'TEXT': '#FFFFFF',
  'INPUT': '#F2EFE8',
  'TEXT_INPUT': '#000000',
  'SCROLL': '#F2EFE8',
  'BUTTON': ('#000000', '#C2D4D8'),
  'PROGRESS': ('#FFFFFF', '#C7D5E0'),
  'BORDER': 1,
  'SLIDER_DEPTH': 0,
  'PROGRESS_DEPTH': 0
}

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

timeColumn = sg.Column(
  [
    [
      setTimeText(getCurrentTime())
    ]
  ], 
  size=(450, 200), 
  pad=(0,0), 
  background_color='#0000FF'
)

exitButton = [[sg.Button('Exit')]]

timeRow = [
  [
    timeColumn,
  ]
]

buttonRow = [
  [sg.Column([[sg.Column(exitButton, size=(75,25),  pad=(0,0))]], pad=(0,0), background_color=BORDER_COLOR),]
]


layout = [
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
  grab_anywhere=True
)
new_value = 1

while True:             # Event Loop
  
  getCurrentTime()
  window.refresh()
  event, values = window.read(timeout=1000,timeout_key = "__TIMEOUT__")

  with open('window.element.list','w') as elemF:
    elemF.write(str(window.element_list()))
  window.save_to_disk('window.save')
  # break

  new_value = new_value + 1  
  if event == "__TIMEOUT__":
    
    window['currentTime'].update(getCurrentTime())
    window.refresh()

  if event == sg.WIN_CLOSED or event == 'Exit':
    break


window.close()