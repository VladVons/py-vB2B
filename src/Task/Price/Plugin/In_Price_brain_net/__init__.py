# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
#
from Inc.ParserX.Common import TPluginBase
from Inc.Misc.FS import FilesExist
from IncP.Log import Log
from .Api import TApi
from .Price import TPrice
from .Category import TCategory


class TIn_Price_brain_net(TPluginBase):
    def __init__(self):
        super().__init__()
        self.Api = TApi()

    async def Run(self) -> dict:
        Category = TCategory(self)
        Price = TPrice(self)

        FilesCheck = [Category.GetFile(), Price.GetFile()]
        Files = FilesExist(FilesCheck)
        if (sum(Files) < len(FilesCheck)):
            User, Passw = self.Conf.get('auth')
            if (not await self.Api.Auth(User, Passw)):
                Log.Print(1, 'e', f'Auth error. Class {self.__class__.__name__}')
                assert(False), f'Auth error {User}, {Passw}'
                sys.exit()

        await Category.Load()
        Category.Filter_FromConfig()

        await Price.Load()
        Price.Filter_HasCategory(Category)

        ConfImagesCheck = self.Conf.GetKey('images.check')
        if (ConfImagesCheck):
            await Price.CheckImages()

        Category.Filter_HasProduct(Price)
        Margins = Category.SubMargin()

        #Text = Category.Visualize()
        #print(Text)


        #Product = TProduct(self)
        #await Product.Load(DirData + '/Product', Price)

        #Products = TProducts(self)
        #await Products.Load(DirData + '/Products', Categories)

        return {'TDbCategory': Category.Dbl, 'TDbPrice': Price.Dbl, 'Margins': Margins}
