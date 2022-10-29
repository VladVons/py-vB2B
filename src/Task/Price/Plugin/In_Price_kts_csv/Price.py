# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat
from ..Price_csv import TPrice_csv


class TPrice(TPrice_csv):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.USD = aParent.Conf.get('USD', 0)

    def _Fill(self, aRow: dict):
        if (aRow.get('Price') or aRow.get('PriceUSD')):
            Rec = self.Dbl.RecAdd()

            Val = self.GetMpn(aRow.get('Mpn', ''))
            Rec.SetField('Mpn', Val)

            Val = aRow.get('Code')
            Rec.SetField('Code', Val)

            Val = aRow.get('Name')
            Rec.SetField('Name', Val)

            Price = aRow.get('Price')
            PriceUSD = aRow.get('PriceUSD')
            if (Price):
                Rec.SetField('Price', ToFloat(Val))
            else:
                Val = round(ToFloat(PriceUSD) * self.USD, 2)
                Rec.SetField('Price', Val)

            Rec.Flush()
