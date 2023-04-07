# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Util.Str import ToFloat
from Inc.Util.Obj import GetNotNone
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbCompPC, TDbCompMonit


class TPricePC(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())

        self.ReDisk = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)
        self.ConfTitle = None

    def _OnLoad(self):
        Conf = self.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])

    def _Fill(self, aRow: dict):
        if (not aRow.get('price')):
            return

        Rec = self.Dbl.RecAdd()

        for x in ['model', 'cpu', 'case', 'dvd', 'vga', 'os']:
            self.Copy(x, aRow, Rec)

        Val = ToFloat(aRow.get('price'))
        Rec.SetField('price', Val)

        Val = aRow.get('disk', '')
        Data = self.ReDisk.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('disk_size', int(Data[0]))
            Rec.SetField('disk', Data[2])

        Val = aRow.get('ram', '')
        Data = self.ReRam.findall(Val)
        if (Data):
            Data = Data[0]
            Rec.SetField('ram_size', int(Data[0]))

        Title = [str(aRow[x]) for x in self.ConfTitle]
        Rec.SetField('title', '/'.join(Title))

        Rec.Flush()


class TPriceMonit(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompMonit())
        self.ConfTitle = None

    def _OnLoad(self):
        Conf = self.GetConfSheet()
        self.ConfTitle = Conf.get('title', [])

    def _Fill(self, aRow: dict):
        if (not aRow.get('price')) or (aRow.get('stand', '').lower() != 'yes'):
            return

        Rec = self.Dbl.RecAdd()

        for x in ['model', 'grade', 'color']:
            self.Copy(x, aRow, Rec)

        Val = GetNotNone(aRow, 'screen', '').replace('"', '')
        Rec.SetField('screen', Val)

        Val = ToFloat(aRow.get('price'))
        Rec.SetField('price', Val)

        Title = [str(aRow[x]) for x in self.ConfTitle]
        Rec.SetField('title', '/'.join(Title))

        Rec.Flush()
