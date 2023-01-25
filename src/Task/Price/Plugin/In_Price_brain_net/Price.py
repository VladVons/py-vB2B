# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Util.Obj import GetNotNone
from IncP.Download import TCheckUrls
from ..Category import TDbCategory
from ..Common import TFileDbl, TTranslate
from ..CommonDb import TDbPrice


class TPrice(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent, TDbPrice())
        self.Trans = TTranslate()

    async def CheckImages(self):
        ProductCodes = self.Dbl.ExportList('Code')
        Urls = [self.Parent.Api.GetUrlImage(x) for x in ProductCodes]
        Res = await (TCheckUrls().Run(Urls, 5, 0.1))
        Images = {Code: Url for Code, Url, Ok in zip(ProductCodes, Urls, Res) if Ok}
        _ImagesErr = {Code: Url for Code, Url, Ok in zip(ProductCodes, Urls, Res) if not Ok}

        for Rec in self.Dbl:
            Code = Rec.GetField('Code')
            Url = Images.get(Code)
            if (Url):
                Rec.SetField('Image', Url)
                Rec.Flush()
            else:
                #Log.Print(1, 'e', 'Url error %s' % (ImagesErr.get(Code)))
                pass
            await self.Sleep.Update()

    def Filter_HasCategory(self, aDbCategory: TDbCategory):
        aDbCategory.Dbl.SearchAdd('CategoryId')

        Res = self.Dbl.New()
        for Rec in self.Dbl:
            CategoryId = Rec.GetField('CategoryId')
            RecNo = aDbCategory.Dbl.Search('CategoryId', CategoryId)
            if (RecNo >= 0):
                Res.RecAdd(Rec).Flush()
            else:
                #Log.Print(1, 'i', '%s, Cant find category %s %s for product %s' % (ErrCnt + 1, CategoryId, Rec.GetField('Name'), Rec.GetField('Id')))
                pass
        self.Dbl = Res

    def _Fill(self, aRow: dict):
        Code = GetNotNone(aRow, 'Code', '')
        Rec = self.Dbl.RecAdd([
            int(GetNotNone(aRow, 'CategoryID', 0)),
            int(GetNotNone(aRow, 'ProductID', 0)),
            Code,
            self.Trans.GetMpn(GetNotNone(aRow, 'Article', '')),
            GetNotNone(aRow, 'Name', ''),
            round(GetNotNone(aRow, 'PriceUSD', 0) * self.Parent.Conf.get('USD'), 2),
            GetNotNone(aRow, 'Available', 0),
            self.Parent.Api.GetUrlImage(Code)
        ])
        Rec.Flush()

    async def _Load(self):
        Data = await self.Parent.Api.GetPriceList(14)
        if (Data['Status'] == 200):
            for _Key, Row in Data['Data'].items():
                self._Fill(Row)
                await self.Sleep.Update()
