#!Venv/bin python3
# -*- coding: utf-8 -*-

import sqlite3
from urllib.request import urlopen

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

# missing = 2432
# while missing < 2543:
#     missing += 1
#     html = urlopen('https://www.opap.org.cy/el/joker?gameid={}'.format(missing)).read()
html = urlopen('https://www.opap.org.cy/el/joker').read()
html = html.decode('utf-8')

soup = BeautifulSoup(html, features='html.parser')
winnerNumbers = soup.find(id='winnerNumbers')
draw = soup.find_all(class_='draw-number-warning')
table = winnerNumbers.find_all('li')
print(table)
newItem = {
    'X1': int(table[0].get_text()),
    'X2': int(table[1].get_text()),
    'X3': int(table[2].get_text()),
    'X4': int(table[3].get_text()),
    'X5': int(table[4].get_text()),
    'Joker': int(table[5].get_text()),
    'Draw': draw[1].get_text(),
    'Date': pd.to_datetime(draw[0].get_text(), dayfirst=True),
}  # format

filePath = 'joker.csv'

drawData = pd.read_csv(filePath)
drawData['Date'] = pd.to_datetime(drawData['Date'])

if newItem['Draw'] not in drawData['Draw'].values:
    drawData = drawData.append(newItem, ignore_index=True)

drawData.to_csv(filePath, index=False)


def JoinNumbers(x):
    return '%s%s%s%s%s' % (x['X1'], x['X2'], x['X3'], x['X4'], x['X5'])


drawData['ResultString'] = drawData.apply(JoinNumbers, axis=1)
drawData['ResultLength'] = drawData['ResultString'].map(lambda x: len(x))

ಠ_ಠ = drawData['ResultLength'].mean()
print(ಠ_ಠ)

numberData = pd.DataFrame()
numberData['Number'] = np.arange(0, 46, 1)
numberData['Count'] = drawData['X1'].value_counts().sort_index()
numberData['Count'] += drawData['X2'].value_counts().sort_index()
numberData['Count'] += drawData['X3'].value_counts().sort_index()
numberData['Count'] += drawData['X4'].value_counts().sort_index()
numberData['Count'] += drawData['X5'].value_counts().sort_index()
numberData = numberData.drop(numberData.index[0])
numberData = numberData.sort_values(by='Count', ascending=False)
print(numberData.head(15))

jokerData = pd.DataFrame()
jokerData['Number'] = np.arange(0, 21, 1)
jokerData['Count'] = drawData['Joker'].value_counts().sort_index()
jokerData = jokerData.drop(jokerData.index[0])
jokerData = jokerData.sort_values(by='Count', ascending=False)
print(jokerData.head())