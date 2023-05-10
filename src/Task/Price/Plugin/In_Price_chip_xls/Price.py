# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Str import ToFloat
from Inc.ParserX.Parser_xls import TParser_xls
from Inc.ParserX.Common import TTranslate
from ..CommonDb import TDbPrice


class TPrice(TParser_xls):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.USD = self.Parent.Conf.get('usd', 0)
        self.Trans = TTranslate()

    def _Fill(self, aRow: dict):
        if (aRow.get('price') or aRow.get('price_usd')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(str(aRow.get('mpn', '')))
            Rec.SetField('mpn', Val)

            self.CopySafe('code', aRow, Rec)
            self.CopySafe('name', aRow, Rec)

            Price = aRow.get('price')
            PriceUSD = aRow.get('price_usd')
            if (Price):
                Rec.SetField('price', ToFloat(Price))
            else:
                Val = round(ToFloat(PriceUSD) * self.USD, 2)
                Rec.SetField('price', Val)

            Rec.Flush()
