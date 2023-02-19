# Created: 2022.09.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

# http://api.brain.com.ua/help



import hashlib
import aiohttp
#
from Inc.ParserX.Common import TApiBase
from IncP.Download import TRecSes, TDownload


class TApi(TApiBase):
    def __init__(self):
        super().__init__()

        self.Url = 'http://api.brain.com.ua'
        self.Web = 'http://brain.com.ua'
        self.Lang = 'ua'
        self.Token = ''

    def GetUrlAuth(self) -> str:
        return f'{self.Url}/auth'

    def GetUrlCategories(self) -> str:
        return f'{self.Url}/categories/{self.Token}?lang={self.Lang}'

    def GetUrlProducts(self, aCategoryId: int, aOffset: int = 0, aLimit: int = 100) -> str:
        return f'{self.Url}/products/{aCategoryId}/{self.Token}?lang={self.Lang}&offset={aOffset}&limit={aLimit}'

    def GetUrlProduct(self, aProductId: int) -> str:
        return f'{self.Url}/product/{aProductId}/{self.Token}?lang={self.Lang}'

    @staticmethod
    def GetImageBase(aProductCode: str) -> str:
        return f'{aProductCode[-2]}/{aProductCode[-1]}/{aProductCode}'

    def GetUrlImage(self, aProductCode: str) -> str:
        return f'{self.Web}/static/images/prod_img/{self.GetImageBase(aProductCode)}_big.jpg'

    def GetUrlStocks(self) -> str:
        return f'{self.Url}/stocks/{self.Token}?lang={self.Lang}'

    def GetUrlTargets(self) -> str:
        return f'{self.Url}/targets/{self.Token}?lang={self.Lang}'

    def GetUrlPriceList(self, aTargetId: int) -> str:
        return f'{self.Url}/pricelists/{aTargetId}/json/{self.Token}?lang={self.Lang}&full=0'

    @staticmethod
    def GetResult(aRes: dict) -> object:
        if (aRes['status'] == 200):
            Data = aRes['data']
            if (Data.get('status', 0) == 1):
                for x in ['result', 'url']:
                    aRes = Data.get(x)
                    if (aRes):
                        return aRes
        return None

    async def Send(self, aRecSes: TRecSes) -> dict:
        Res = await self.Download.SendOne(aRecSes)
        return self.GetResult(Res)

    async def Auth(self, aLogin: str, aPassw: str) -> bool:
        Passw = hashlib.md5(aPassw.encode()).hexdigest()
        FormData = aiohttp.FormData({'login': aLogin, 'password': Passw})
        Url = self.GetUrlAuth()
        Data = await self.Send(TRecSes(Url, FormData))
        if (Data):
            self.Token = Data
            return True

    async def GetImage(self, aProductCode: str) -> bytes:
        Url = self.GetUrlImage(aProductCode)
        Res = await self.Download.SendOne(TRecSes(Url))
        if (Res['status'] == 200):
            return Res['data']

    async def GetCategories(self) -> list:
        Url = self.GetUrlCategories()
        return await self.Send(TRecSes(Url))

    async def GetProducts(self, aCategoryId: int, aOffset: int = 0, aLimit: int = 100) -> list:
        Url = self.GetUrlProducts(aCategoryId, aOffset, aLimit)
        return await self.Send(TRecSes(Url))

    async def GetProduct(self, aProductId: int) -> dict:
        Url = self.GetUrlProduct(aProductId)
        return await self.Send(TRecSes(Url))

    async def GetStocks(self) -> dict:
        Url = self.GetUrlStocks()
        return await self.Send(TRecSes(Url))

    async def GetTargets(self) -> dict:
        Url = self.GetUrlTargets()
        return await self.Send(TRecSes(Url))

    async def GetPriceList(self, aTargetId: int) -> dict:
        Url = self.GetUrlPriceList(aTargetId)
        Url = await self.Send(TRecSes(Url))
        Download = TDownload()
        return await Download.SendOne(TRecSes(Url))
