# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
#
from Inc.Db.DbList import TDbRecSafe
from ..Common import TFileDbl
from ..CommonDb import TDbPriceJoin


class TMain(TFileDbl):
    def __init__(self, aParent, aPrices: dict):
        super().__init__(aParent, TDbPriceJoin())
        self.Prices = aPrices

    def MinPrice(self, aMpn: str, aRec: TDbRecSafe):
        Match = 0
        MinPrice = sys.maxsize
        for Name, DbPrice in self.Prices.items():
            RecNo = DbPrice.Search('mpn', aMpn)
            if (RecNo >= 0):
                Price = DbPrice.RecGo(RecNo).GetField('price')
                if (Price > 0):
                    Match += 1
                    MinPrice = min(MinPrice, Price)
                    aRec.SetField(Name, Price)
        aRec.SetField('price', MinPrice)
        aRec.SetField('match', Match)

    async def _Load(self):
        for Name, DbPrice in self.Prices.items():
            self.Dbl.Fields.Add(Name, float)
            DbPrice.SearchAdd('mpn')

        ConfMain = self.Parent.Conf.get('main')
        DblMain = self.Prices[ConfMain]
        for RecNo, Rec in enumerate(DblMain):
            RecNew = self.Dbl.RecAdd()
            RecNew.SetAsRec(Rec, ['id', 'code', 'mpn', 'name'])
            Mpn = Rec.GetField('mpn')
            if (Mpn):
                self.MinPrice(Rec.GetField('mpn'), RecNew)
                DblMain.RecNo = RecNo
            RecNew.Flush()
            await self.Sleep.Update()
