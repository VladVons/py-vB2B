# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from Inc.Util.Str import ToFloat
from ..CommonDb import TDbCompPC
from ..Parser_xlsx import TParser_xlsx


class TPrice(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())

        self.ReDisk = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)

    def _Fill(self, aRow: dict):
        if (aRow.get('price')):
            Rec = self.Dbl.RecAdd()

            self.Copy('model', aRow, Rec)
            self.Copy('cpu', aRow, Rec)
            self.Copy('case', aRow, Rec)
            self.Copy('dvd', aRow, Rec)
            self.Copy('vga', aRow, Rec)
            self.Copy('os', aRow, Rec)

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

            Rec.Flush()
