# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Str import ToFloat
from ..Common import TTranslate
from ..CommonDb import TDbPrice
from ..Parser_csv import TParser_csv


class TPrice(TParser_csv):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.USD = aParent.Conf.get('usd', 0)
        self.Trans = TTranslate()

    def _Fill(self, aRow: dict):
        if (aRow.get('price') or aRow.get('price_usd')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(aRow.get('mpn', ''))
            Rec.SetField('mpn', Val)

            self.Copy('code', aRow, Rec)
            self.Copy('name', aRow, Rec)

            Price = aRow.get('price')
            PriceUSD = aRow.get('price_usd')
            if (Price):
                Rec.SetField('price', ToFloat(Val))
            else:
                Val = round(ToFloat(PriceUSD) * self.USD, 2)
                Rec.SetField('price', Val)

            Rec.Flush()
