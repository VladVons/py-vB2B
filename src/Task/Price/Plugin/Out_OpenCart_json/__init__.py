# Created: 2022.10.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TMain
from ..Common import TPluginBase


class TOut_OpenCart_json(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Save(
            self.GetParamDependsIdx('TDbPrice'),
            self.GetParamDependsIdx('TDbCategory'),
            self.GetParamDependsIdx('Margins')
        )
