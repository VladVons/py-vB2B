# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Price import TPrice
from ..Common import TPluginBase


class TIn_Price_tdb_xlsx(TPluginBase):
    async def Run(self):
        Price = TPrice(self)
        await Price.Load()
        return {'TDbPrice': Price.Dbl}
