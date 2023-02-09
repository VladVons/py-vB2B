# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TCategory, TProduct
from ..Common import TPluginBase


class TIn_Price_prom_xml(TPluginBase):
    async def Run(self):
        Category = TCategory(self)
        Engine = Category.InitEngine()
        Category.SetSheet('category')
        await Category.Load()

        Product = TProduct(self)
        Product.InitEngine(Engine)
        Product.SetSheet('item')
        await Product.Load()

        return {'TDbCategory': Category.Dbl, 'TDbProduct': Product.Dbl}
