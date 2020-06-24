#!Venv/bin python3
# -*- coding: utf-8 -*-
import sqlite3
from urllib.request import urlopen

import numpy as np
import pandas as pd
from bs4 import BeautifulSoup

with sqlite3.connect('test.db') as conn:
    c = conn.cursor()
    # Draw,Date,X1,X2,X3,X4,X5,Joker
    c.execute('''CREATE TABLE IF NOT EXISTS some_table
              (id INTEGER PRIMARY KEY AUTOINCREMENT, ...);''')
    conn.commit()

# This needs to change to greek version of
# the site which also has the correct order
# https://tzoker.opap.gr/#/

html = urlopen('https://www.opap.org.cy/el/page/joker-results').read()
html = html.decode('utf-8')

soup = BeautifulSoup(html, features='html.parser')
column2 = soup.find(id='column2')
competition_title = column2.find(id='competition_title')
table = column2.findAll('table')[0].findAll('tr')[1]
tableParts = list(filter(None, table.text.split('\n')))
parts = competition_title.div.text.split('η')

newItem = {
    'X1': int(tableParts[0]),
    'X2': int(tableParts[1]),
    'X3': int(tableParts[2]),
    'X4': int(tableParts[3]),
    'X5': int(tableParts[4]),
    'Joker': int(tableParts[6]),
    'Draw': int(parts[0]),
    'Date': pd.to_datetime(parts[2]),
}

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

# drawData = drawData[drawData['Date'] >= pd.to_datetime('2015-01-01')]

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
