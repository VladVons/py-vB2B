# Created: 2022.10.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#--- xlsx
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Font
from openpyxl.comments import Comment
#
from IncP.Log import Log
from ..Common import TFileBase
from ..CommonDb import TDbPriceJoin, TDbPrice


class TMain(TFileBase):
    def Head(self, aDbl: TDbPrice, aWS, aHeadRow: dict):
        ConfFormat = self.Parent.Conf.GetKey('Format', '#,##0.00')
        ConfFieldWidth = self.Parent.Conf.GetKey('Field.Width', {})

        for Key, (No, Field, _) in aDbl.Fields.items():
            aWS.cell(aHeadRow['Title'], No + 1).value = Key
            CD = aWS.column_dimensions[get_column_letter(No + 1)]

            Width = ConfFieldWidth.get(Key)
            if (Width is not None):
                if (Width == 0):
                    CD.hidden= True
                else:
                    CD.width = Width

            if (Key.startswith('Price')):
                CD.number_format = ConfFormat

        Field = aDbl.Fields.get('Price')
        #aWS.column_dimensions[get_column_letter(Field[0] + 1)].font = Font(bold=True)
        aWS.freeze_panes = aWS.cell(aHeadRow['Data'], Field[0] + 2)

    async def Save(self, aDbPriceJoin: TDbPriceJoin, aPrices: list[TDbPrice]):
        WB = Workbook()
        WS = WB.active

        HeadRow = {'Title': 1, 'Data': 2}
        self.Head(aDbPriceJoin, WS, HeadRow)

        ConfRatio = self.Parent.Conf.GetKey('Ratio')
        for RowNo, Rec in enumerate(aDbPriceJoin, HeadRow['Data']):
            Price = Rec.GetField('Price')
            for FieldNo, Field in enumerate(aDbPriceJoin.Fields):
                Value = Rec[FieldNo]
                Cell = WS.cell(RowNo, FieldNo + 1)
                Cell.value = Value
                if (Field.startswith('In_Price_')):
                    if (Value == Price):
                        Cell.font = Font(bold = True)
                    elif (ConfRatio):
                        Text = '+%0.2f %0.2f%%' % (Value - Price, Value / Price * 100 - 100)
                        Cell.comment = Comment(Text, '', 20)
            await self.Sleep.Update()

        ConfPrices = self.Parent.Conf.GetKey('Prices', True)
        if (ConfPrices):
            aDbPriceJoin.SearchAdd('Mpn')
            for Plugin, Dbl in aPrices.items():
                WS = WB.create_sheet(title = Plugin)
                self.Head(Dbl, WS, HeadRow)
                for RowNo, Rec in enumerate(Dbl, HeadRow['Data']):
                    Mpn = Rec.GetField('Mpn')
                    for FieldNo, Field in enumerate(Dbl.Fields):
                        Cell = WS.cell(RowNo, FieldNo + 1)
                        Cell.value = Rec[FieldNo]
                        if (Field == 'Price') and (aDbPriceJoin.Search('Mpn', Mpn) >= 0):
                            Cell.font = Font(bold = True)
                    await self.Sleep.Update()

        ConfFile = self.Parent.GetFile()
        os.makedirs(os.path.dirname(ConfFile), exist_ok=True)
        Log.Print(1, 'i', 'Save %s'  % (ConfFile))
        WB.save(ConfFile)
