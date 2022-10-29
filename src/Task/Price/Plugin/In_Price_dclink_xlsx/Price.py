# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat
from ..Price_xlsx import TPrice_xlsx


class TPrice(TPrice_xlsx):
    def _Fill(self, aRow: dict):
        if (aRow.get('Price')):
            Rec = self.Dbl.RecAdd()

            Val = self.GetMpn(str(aRow.get('Mpn', '')))
            Rec.SetField('Mpn', Val)

            Val = str(aRow.get('Code'))
            Rec.SetField('Code', Val)

            Val = str(aRow.get('Name'))
            Rec.SetField('Name', Val)

            Val = ToFloat(aRow.get('Price'))
            Rec.SetField('Price', Val)

            Rec.Flush()
