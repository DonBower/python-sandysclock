#!/usr/local/bin/python
import PySimpleGUI as sg
from datetime import datetime

from datetime import datetime as dt

def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

# print custom_strftime('%B {S}, %Y', dt.now())

"""
    Dashboard using blocks of information.

    Copyright 2020 PySimpleGUI.org
"""


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

rightNow = datetime.now()
currentDayString = custom_strftime('%A, %B {S}, %Y', rightNow)
currentDayString = "Wednesday, September 9th, 2023"
currentDay = [[sg.Text(currentDayString, font=('Helvetica', 42), justification='c', background_color='#FF7F7F')]]

currentTime  = [[sg.Text(rightNow.strftime('%I:%M'), justification='c', pad=BPAD_TOP, font=('Digital-7', 144))],]

currentTimeSet = rightNow.strftime('%p')
if currentTimeSet == "PM":
  amText="AM"
  pmText="PM"
else:
  amText="AM"
  pmText="PM"
    
exitButton = [[sg.Button('Exit')]]


temp = [
  [sg.Text('103º',    font=('Helvetica',54))],
  [sg.Text('Current', font=('Helvetica',18))],
]
lowTemp = [
  [sg.Text('100º',  font=('Helvetica',36))],
  [sg.Text('Low',   font=('Helvetica',12))],
]
highTemp = [
  [sg.Text('110º',  font=('Helvetica',36))],
  [sg.Text('high',  font=('Helvetica',12))],
]

am_pm = [
  [
    sg.Text(amText, font=('Helvetica',48))
  ],
  [
    sg.Text(pmText, font=('Helvetica',48))
  ]
]


layout = [
  [sg.Column(currentDay, size=(700, 75), pad=(0,0), background_color='#FF7F7F')],
  [sg.Column(currentTime, size=(350, 200), pad=(0,0)),sg.Column(am_pm, size=(100, 200), pad=(0,0)),sg.Column(temp, size=(250, 100), pad=(0,0)),],
  [sg.Column(lowTemp, size=(100, 100), pad=(0,0)),sg.Column(highTemp, size=(100, 100), pad=(0,0)),],
  [sg.Column([[sg.Column(exitButton, size=(75,25),  pad=(0,0))]], pad=(0,0), background_color=BORDER_COLOR),]
]

window = sg.Window('Dashboard PySimpleGUI-Style', layout, margins=(0,0), background_color=BORDER_COLOR, no_titlebar=True, grab_anywhere=True)

while True:             # Event Loop
    
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
window.close()