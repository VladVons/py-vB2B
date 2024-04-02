import json
import re
from Inc.Misc.Translit import TTranslit

def Main():
    Translit = TTranslit()
    Translit.Table.update({
        ' ': '_',
        '.': '_',
        '(': '',
        ')': '',
        "’": ''
    })

    ReSpaces = re.compile(r'\s+')

    File = 'kts.json'
    with open (File, 'r', encoding='utf8') as F:
        Data = json.load(F)

    for Idx, xData in enumerate(Data):
        Text = xData['name'].lower()
        #Text = ReSpaces.sub(' ', Text)
        Text = Translit.Xlat(Text)
        Text = f'https://ktc.ua/goods/{Text}.html'

        print(Idx, xData['code'], xData['name'])
        print(Idx, xData['code'], Text)
        print()
        if (Idx > 10):
            break

Main()
