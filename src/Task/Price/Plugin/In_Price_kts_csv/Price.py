# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat, TTranslate
from ..CommonDb import TDbPrice
from ..Parser_csv import TParser_csv


class TPrice(TParser_csv):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.USD = aParent.Conf.get('USD', 0)
        self.Trans = TTranslate()

    def _Fill(self, aRow: dict):
        if (aRow.get('Price') or aRow.get('PriceUSD')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(aRow.get('Mpn', ''))
            Rec.SetField('Mpn', Val)

            self.Copy('Code', aRow, Rec)
            self.Copy('Name', aRow, Rec)

            Price = aRow.get('Price')
            PriceUSD = aRow.get('PriceUSD')
            if (Price):
                Rec.SetField('Price', ToFloat(Val))
            else:
                Val = round(ToFloat(PriceUSD) * self.USD, 2)
                Rec.SetField('Price', Val)

            Rec.Flush()
