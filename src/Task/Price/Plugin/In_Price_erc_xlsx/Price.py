# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat
from ..Price_xlsx import TPrice_xlsx


class TPrice(TPrice_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.USD = aParent.Conf.get('USD', 0)


    def _Fill(self, aRow: dict):
        if (aRow.get('Price')):
            Rec = self.Dbl.RecAdd()

            Val = self.GetMpn(str(aRow.get('Mpn', '')))
            Rec.SetField('Mpn', Val)

            Val = str(aRow.get('Name'))
            Rec.SetField('Name', Val)

            Val = ToFloat(aRow.get('Price'))
            if (aRow.get('Currency') == 'у.о.'):
                Val = round(Val * self.USD, 2)
            Rec.SetField('Price', Val)

            Rec.Flush()
