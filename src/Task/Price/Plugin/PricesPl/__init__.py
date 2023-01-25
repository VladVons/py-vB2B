# Created: 2023.01.23
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TMain
from ..Common import TPluginBase


class TPricesPl(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Load()

        return {}
