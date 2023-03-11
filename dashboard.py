#!/usr/local/bin/python

import PySimpleGUI as sg
from datetime import datetime

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
  'BORDER': 1,'SLIDER_DEPTH': 0, 'PROGRESS_DEPTH': 0
}

# sg.theme_add_new('Dashboard', theme_dict)     # if using 4.20.0.1+
sg.LOOK_AND_FEEL_TABLE['Dashboard'] = theme_dict
sg.theme('Dashboard')

BORDER_COLOR = '#C7D5E0'
DARK_HEADER_COLOR = '#1B2838'
BPAD_TOP = ((20,20), (20, 10))
BPAD_LEFT = ((20,10), (0, 10))
BPAD_LEFT_INSIDE = (0, 5)
BPAD_RIGHT = ((10,20), (10, 20))


date_banner = [
  [
    sg.Text(
      datetime.today().strftime('%A, %B %d %Y'),
      font='Any 20',
      text_color='yellow',
      # size=50, 
      # pad=(20,20),
      justification='center',
      background_color=DARK_HEADER_COLOR
    )
  ]
]

time_block = [
  [
    sg.Text(
      '20:20', 
      font='Digital-7',
      size=48,
      # justification='center',
      text_color='yellow',
      background_color=DARK_HEADER_COLOR
    ),
  ],
]

am_block = [
  [
    sg.Text(
      'AM',
      font='Any 20',
      # justification='center',
      text_color='yellow',
    )
  ],
]

pm_block = [
  [
    sg.Text(
      'PM',
      font='Any 20',
      text_color='yellow',
    )
  ],
]

current_temp_block = [
  [
    sg.Text(
      '103º',
      font='Any 20'
    )
  ],
]

low_temp_block = [
  [
    sg.Text(
      '101º',
      font='Any 20'
    )
  ],
]

high_temp_block = [
  [
    sg.Text(
      '109º',
      font='Any 20'
    )
  ],
]

exit_block = [
  [
    sg.Button('Exit')
  ]
]

row1=  [
    sg.Text(
      datetime.today().strftime('%A, %B %d %Y'),
      font='Any 20',
      text_color='yellow',
      size=50, 
      pad=(20,20),
      justification='center',
      background_color=DARK_HEADER_COLOR
    ),
  ]

row2 = [
    [      
      sg.Column(
        time_block,
        size=(350, 200),
        pad=(20,0),
        
        background_color=DARK_HEADER_COLOR
      ),
      sg.Column(
          am_block,
          size=(100, 100),
          pad=(0,0),
      ),
    ],
      sg.Column(
        current_temp_block,
        size=(250, 100),
        pad=(0,0),
      ),
    sg.Column(
      pm_block,
      size=(100, 100),
      pad=(0,0),
    ),
]
row3 = [
  sg.Column(
    exit_block,
    size=(50, 35),
    pad=(20,0),
  )    
]

layout = [
  row1,
  row2,
  row3
]

window = sg.Window(
  'Dashboard PySimpleGUI-Style', 
  layout, 
  # auto_size_text = True,
  # auto_size_buttons = True,
  location = (0,0),
  size = (800,480),
  margins=(0,0), 
  background_color=BORDER_COLOR, 
  no_titlebar=False, 
  grab_anywhere=True
)

while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()