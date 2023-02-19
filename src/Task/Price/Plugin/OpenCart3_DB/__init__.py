# Created: 2022.11.18
# # Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TOpenCart3_DB(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Run()
