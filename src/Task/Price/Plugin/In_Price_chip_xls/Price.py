# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat
from ..Price_xls import TPrice_xls


class TPrice(TPrice_xls):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.USD = self.Parent.Conf.get('USD', 0)

    def _Fill(self, aRow: dict):
        if (aRow.get('Price') or aRow.get('PriceUSD')):
            Rec = self.Dbl.RecAdd()

            Val = self.GetMpn(str(aRow.get('Mpn', '')))
            Rec.SetField('Mpn', Val)

            Val = str(aRow.get('Code'))
            Rec.SetField('Code', Val)

            Val = str(aRow.get('Name'))
            Rec.SetField('Name', Val)

            Price = aRow.get('Price')
            PriceUSD = aRow.get('PriceUSD')
            if (Price):
                Rec.SetField('Price', ToFloat(Val))
            else:
                Val = round(ToFloat(PriceUSD) * self.USD, 2)
                Rec.SetField('Price', Val)

            Rec.Flush()
