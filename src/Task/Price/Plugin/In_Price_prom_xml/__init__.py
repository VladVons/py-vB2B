# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from .Main import TCategory, TProduct
from ..Common import TPluginBase


class TIn_Price_prom_xml(TPluginBase):
    async def Run(self):
        Category = TCategory(self)
        if (not os.path.exists(Category.GetFile())):
            Engine = Category.InitEngine()
            Category.SetSheet('category')
        await Category.Load()

        Product = TProduct(self)
        if (not os.path.exists(Product.GetFile())):
            Product.InitEngine(Engine)
            Product.SetSheet('item')
        await Product.Load()

        return {'TDbCategory': Category.Dbl, 'TDbProductEx': Product.Dbl}
