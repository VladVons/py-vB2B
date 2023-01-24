# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Price import TPrice
from ..Common import TPluginBase


class In_Price_pl01_xlsx(TPluginBase):
    async def Run(self):
        Price = TPrice(self)
        await Price.Load()
        return {'TDbPrice': Price.Dbl}
