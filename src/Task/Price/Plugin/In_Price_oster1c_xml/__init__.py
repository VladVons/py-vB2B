# Created: 2023.02.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.ParserX.Common import TPluginBase
from .Main import TCategory, TProduct


class TIn_Price_oster1c_xml(TPluginBase):
    async def Run(self):
        Engine = None

        Category = TCategory(self)
        if (not os.path.exists(Category.GetFile())):
            Engine = Category.InitEngine()
            Category.SetSheet('Category')
        await Category.Load()

        Product = TProduct(self)
        if (not os.path.exists(Product.GetFile())):
            Product.InitEngine(Engine)
            Product.SetSheet('Item')
        await Product.Load()

        return {'TDbCategory': Category.Dbl, 'TDbProductEx': Product.Dbl}
