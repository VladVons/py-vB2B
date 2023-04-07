# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details



from Inc.Util.Str import ToFloat
from Inc.ParserX.Common import TTranslate
from Inc.ParserX.Parser_xlsx import TParser_xlsx
from ..CommonDb import TDbPrice


class TPrice(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.USD = aParent.Conf.get('usd', 0)
        self.Trans = TTranslate()


    def _Fill(self, aRow: dict):
        if (aRow.get('price_usd')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(str(aRow.get('mpn', '')))
            Rec.SetField('mpn', Val)

            self.CopySafe('name', aRow, Rec)

            Val = round(ToFloat(aRow.get('price_usd')) * self.USD, 2)
            Rec.SetField('price', Val)

            Rec.Flush()
