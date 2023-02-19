# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TPack_zip(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Load()
