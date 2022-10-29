# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.DB.DbList import TDbList
from Inc.Util.Obj import GetNotNone, DeepGet
from IncP.Download import TRecSes, TDownload
from IncP.Log import Log
from .Images import TImages
from .Category import TCategory


class TProducts():
    def __init__(self, aParent):
        self.Parent = aParent
        self._Count = 0
        self._Images = TImages(aParent)
        self.Dbl = TDbList([
            ('CategoryId', int),
            ('ParentId', int),
            ('Id', int),
            ('Code', str),
            ('Mpn', str),
            ('Ean', str),
            ('Name', str),
            ('Price', float),
            ('Image', str)
        ])

        self._CategoryId = None

    def _GetUrls(self, aCategoryId: int, aStart: int, aCount: int, aLimit: int) -> list[str]:
        return [self.Parent.Api.GetUrlProducts(aCategoryId, i, aLimit) for i in range(aStart, aCount, aLimit)]

    def _Fill(self, aRow: dict):
        Rec = self.Dbl.RecAdd([
            int(GetNotNone(aRow, 'categoryID', 0)),
            0,
            int(GetNotNone(aRow, 'productID', 0)),
            GetNotNone(aRow, 'product_code', ''),
            GetNotNone(aRow, 'articul', ''),
            GetNotNone(aRow, 'EAN', ''),
            GetNotNone(aRow, 'name', ''),
            float(GetNotNone(aRow, 'price_uah', 0)),
            GetNotNone(aRow, 'large_image', '')
        ])
        Rec.Flush()

    async def _OnSend(self, aRecSes: TRecSes, aRes: dict):
        if (aRes['Status'] != 200):
            Log.Print(1, 'e', 'ErrA. Url: %s, Status: %s' % (aRecSes.Url, aRes['Status']))
            return

        if (DeepGet(aRes, 'Data.status') != 1):
            Log.Print(1, 'e', 'ErrB %s' % (aRecSes.Url))
            return

        Products = DeepGet(aRes, 'Data.result.list')
        if (Products):
            for Row in Products:
                self._Fill(Row)
                if (self.Dbl.GetSize() % 100 == 0):
                    print('Records: %s/%s' % (self.Dbl.GetSize(), self._Count))

    async def LoadImages(self, aData: dict):
        Data = [
            Val
            for Key, Val in aData.items()
            if not os.path.exists(self._Images.GetFilePath(Key))
        ]
        await self._Images.LoadUrls(Data, 5)

    async def Load(self, aFile: str, aCategory: TCategory) -> list:
        Res = []
        for Rec in aCategory.Dbl:
            if (Rec.GetField('ParentId') <= 1):
                continue

            CategoryId = Rec.GetField('CategoryId')
            File = f'{aFile}_{CategoryId}.dat'
            print(f'Load {File} {Rec.GetField("Name")}')
            if (os.path.exists(File)):
                Dbl = TDbList().Load(File)
                #print('---x1', File, Dbl.GetSize())
                #print(Dbl)
            else:
                Products = TProducts(self.Parent)
                await Products.Run(CategoryId, 3)
                Dbl = Products.Dbl
                Dbl.Tag = Rec.GetField('Name')
                if (Dbl.GetSize() > 0):
                    Dbl.Sort(['Name'])
                    Dbl.Save(File)

            if (self.Parent.Conf.get('Images')):
                await self.LoadImages(Dbl.ExportPair('Code', 'Image'))
            Res.append(Dbl)
        return Res

    async def Run(self, aCategoryId: int, aTasks: int = 3) -> TDbList:
        Data = await self.Parent.Api.GetProducts(aCategoryId, 0)
        if (not Data):
            Log.Print(1, 'e', 'Cant get products from category %s' % (aCategoryId))
            return

        self._Count = Data['count']
        #self._Count = 19400
        self._CategoryId = aCategoryId
        #self._CategoryId = 1331
        Start = 0
        #Start = 19370
        Limit = 100
        #Limit = 1
        Urls = self._GetUrls(self._CategoryId, Start, self._Count, Limit)

        Data = [TRecSes(x) for x in Urls]
        Download = TDownload(self._OnSend)
        await Download.SendMany(Data, aTasks)
