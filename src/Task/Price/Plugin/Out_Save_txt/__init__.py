# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TOut_Save_txt(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Save(
            self.GetParamDepends()
        )
