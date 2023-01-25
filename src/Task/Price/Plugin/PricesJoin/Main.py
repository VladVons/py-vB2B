# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
#
from Inc.Db.DbList import TDbRec
from ..Common import TFileDbl
from ..CommonDb import TDbPriceJoin


class TMain(TFileDbl):
    def __init__(self, aParent, aPrices: dict):
        super().__init__(aParent, TDbPriceJoin())
        self.Prices = aPrices

    def MinPrice(self, aMpn: str, aRec: TDbRec):
        Match = 0
        MinPrice = sys.maxsize
        for Name, DbPrice in self.Prices.items():
            RecNo = DbPrice.Search('Mpn', aMpn)
            if (RecNo >= 0):
                Price = DbPrice.RecGo(RecNo).GetField('Price')
                if (Price > 0):
                    Match += 1
                    MinPrice = min(MinPrice, Price)
                    aRec.SetField(Name, Price)
        aRec.SetField('Price', MinPrice)
        aRec.SetField('Match', Match)

    async def _Load(self):
        for Name, DbPrice in self.Prices.items():
            self.Dbl.Fields.Add(Name, float)
            DbPrice.SearchAdd('Mpn')

        ConfMain = self.Parent.Conf.get('Main')
        DblMain = self.Prices[ConfMain]
        for RecNo, Rec in enumerate(DblMain):
            RecNew = self.Dbl.RecAdd()
            RecNew.SetAsRec(Rec, ['Id', 'Code', 'Mpn', 'Name'])
            Mpn = Rec.GetField('Mpn')
            if (Mpn):
                self.MinPrice(Rec.GetField('Mpn'), RecNew)
                DblMain.RecNo = RecNo
            RecNew.Flush()
            await self.Sleep.Update()
