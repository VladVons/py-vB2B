# Created: 2022.10.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TOut_PricesJoin_xlsx(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Save(
            self.GetParamDependsIdx('TDbPriceJoin'),
            self.GetParamDependsIdx('Prices')
        )
