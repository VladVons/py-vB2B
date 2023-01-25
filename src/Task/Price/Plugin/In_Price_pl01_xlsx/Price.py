# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
#
from ..Common import ToFloat
from ..CommonDb import TDbCompPC
from ..Parser_xlsx import TParser_xlsx


class TPrice(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPC())

        self.ReDisk = re.compile(r'(\d+)\s*(gb|tb)\s*(hdd|ssd)', re.IGNORECASE)
        self.ReRam = re.compile(r'(\d+)\s*(gb)', re.IGNORECASE)

    def _Fill(self, aRow: dict):
        if (aRow.get('Price')):
            Rec = self.Dbl.RecAdd()

            self.Copy('Model', aRow, Rec)
            self.Copy('CPU', aRow, Rec)
            self.Copy('Case', aRow, Rec)
            self.Copy('DVD', aRow, Rec)
            self.Copy('VGA', aRow, Rec)
            self.Copy('OS', aRow, Rec)

            Val = ToFloat(aRow.get('Price'))
            Rec.SetField('Price', Val)

            Val = aRow.get('Disk', '')
            Data = self.ReDisk.findall(Val)
            if (Data):
                Data = Data[0]
                Rec.SetField('DiskSize', int(Data[0]))
                Rec.SetField('Disk', Data[2])

            Val = aRow.get('RAM', '')
            Data = self.ReRam.findall(Val)
            if (Data):
                Data = Data[0]
                Rec.SetField('RamSize', int(Data[0]))

            Rec.Flush()
