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
        self.Trans = TTranslate()

    def _Fill(self, aRow: dict):
        if (aRow.get('price')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(str(aRow.get('mpn', '')))
            Rec.SetField('mpn', Val)

            self.Copy('code', aRow, Rec)
            self.Copy('name', aRow, Rec)

            Val = ToFloat(aRow.get('price'))
            Rec.SetField('price', Val)

            Rec.Flush()
