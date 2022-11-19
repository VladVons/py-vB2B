# Created: 2022.11.18
# # Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TMain
from ..Common import TPluginBase


class TOpenCart3_DB(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Run()
