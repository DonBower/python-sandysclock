#!/usr/bin/python

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
      background_color=DARK_HEADER_COLOR
    )
  ]
]

time_block = [
  [
    sg.Text(
      '20:20', 
      font='Digital-7',
      text_color='yellow',
      auto_size_text=True
    )
  ],
]

am_block = [
  [
    sg.Text(
      'AM',
      font='Any 20'
    )
  ],
]

pm_block = [
  [
    sg.Text(
      'AM',
      font='Any 20'
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



layout = [
  [
    sg.Column(
      date_banner, 
      size=(700, 75), 
      pad=(0,0), 
      background_color=DARK_HEADER_COLOR
    )
  ],
  [
    sg.Column(
      [
        [
          sg.Column(
            time_block, 
            size=(350,200), 
            pad=BPAD_LEFT_INSIDE
          )
        ]
        # [
        #   [
        #     sg.Column(
        #       am_block, 
        #       size=(100,100),
        #       pad=BPAD_LEFT_INSIDE
        #     )
        #   ],
        #   [
        #     sg.Column(
        #       pm_block, 
        #       size=(100,100),
        #       pad=BPAD_LEFT_INSIDE
        #     )
        #   ]
        # ],
        # [
        #   [
        #     sg.Column(
        #       current_temp_block, 
        #       size=(250,100), 
        #       pad=BPAD_LEFT_INSIDE
        #     )
        #   ],
        #   [
        #     [
        #       sg.Column(
        #         low_temp_block, 
        #         size=(125,100),
        #         pad=BPAD_LEFT_INSIDE
        #       )
        #     ],
        #     [
        #       sg.Column(
        #         high_temp_block, 
        #         size=(125,100),
        #         pad=BPAD_LEFT_INSIDE
        #       )
        #     ]
        #   ]
        # ]
      ], 
      pad=BPAD_LEFT, 
      background_color=BORDER_COLOR
    ),
    sg.Column(
      exit_block,
      size=(50, 50),
      pad=BPAD_RIGHT
    )
  ]
]

window = sg.Window(
  'Dashboard PySimpleGUI-Style', 
  layout, 
  auto_size_text = True,
  auto_size_buttons = True,
  location = (0,0),
  size = (800,480),
  margins=(0,0), 
  background_color=BORDER_COLOR, 
  no_titlebar=True, 
  grab_anywhere=True
)

while True:             # Event Loop
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()