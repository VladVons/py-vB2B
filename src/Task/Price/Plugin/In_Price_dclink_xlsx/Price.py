# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import ToFloat, TTranslate
from ..CommonDb import TDbPrice
from ..Parser_xlsx import TParser_xlsx


class TPrice(TParser_xlsx):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.Trans = TTranslate()

    def _Fill(self, aRow: dict):
        if (aRow.get('Price')):
            Rec = self.Dbl.RecAdd()

            Val = self.Trans.GetMpn(str(aRow.get('Mpn', '')))
            Rec.SetField('Mpn', Val)

            self.Copy('Code', aRow, Rec)
            self.Copy('Name', aRow, Rec)

            Val = ToFloat(aRow.get('Price'))
            Rec.SetField('Price', Val)

            Rec.Flush()
