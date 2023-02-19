# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.DbList import TDbListSafe
from Inc.Util.Obj import GetNotNone
from IncP.Download import TRecSes, TDownload
from IncP.Log import Log
from .Price import TPrice
from ..CommonDb import TDbProduct


class TProduct():
    def __init__(self, aParent):
        self.Parent = aParent
        self._Count = 0
        self.Dbl = TDbProduct()

    def _GetUrls(self, aProductId: list[int]) -> list[str]:
        return [self.Parent.Api.GetUrlProduct(x) for x in aProductId]

    def _Fill(self, aRow: dict):
        Rec = self.Dbl.RecAdd([
            int(GetNotNone(aRow, 'categoryID', 0)),
            int(GetNotNone(aRow, 'productID', 0)),
            GetNotNone(aRow, 'product_code', ''),
            GetNotNone(aRow, 'articul', ''),
            GetNotNone(aRow, 'name', ''),
            float(GetNotNone(aRow, 'price_uah', 0)),
            GetNotNone(aRow, 'large_image', '')
        ])
        Rec.Flush()

    async def _OnSend(self, _aRecSes: TRecSes, aRes: dict):
        Data = self.Parent.Api.GetResult(aRes)
        if (Data):
            self._Fill(Data)
            if (self.Dbl.GetSize() % 10 == 0):
                Log.Print(1, 'i', 'Records: %s/%s' % (self.Dbl.GetSize(), self._Count))

    async def Load(self, aFile: str, aPrice: TPrice):
        Log.Print(1, 'i', 'Get product %s' % (aFile))
        if (os.path.exists(aFile)):
            self.Dbl = TDbListSafe().Load(aFile)
        else:
            Products = aPrice.Dbl.ExportList('Id')
            await self.Run(Products)
            self.Dbl.Save(aFile)
        Log.Print(1, 'i', 'records %s' % self.Dbl.GetSize())

    async def Run(self, aProductCodes: list[str]):
        self._Count = len(aProductCodes)
        Download = TDownload(self._OnSend)
        RecSes = [TRecSes(x) for x in self._GetUrls(aProductCodes)]
        await Download.SendMany(RecSes, 5)
