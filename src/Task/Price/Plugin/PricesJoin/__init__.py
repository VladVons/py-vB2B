# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TPricesJoin(TPluginBase):
    async def Run(self):
        Prices = self.GetParamDepends('TDbPrice')
        Main = TMain(self, Prices)
        await Main.Load()

        return {'TDbPriceJoin': Main.Dbl, 'Prices': Prices}
