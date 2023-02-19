# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Price import TPrice


class TIn_Price_erc_xlsx(TPluginBase):
    async def Run(self):
        Price = TPrice(self)
        Price.InitEngine()
        await Price.Load()
        return {'TDbPrice': Price.Dbl}
