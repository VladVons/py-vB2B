# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TMain
from ..Common import TPluginBase


class TSendMail(TPluginBase):
    async def Run(self):
        Main = TMain(self)
        await Main.Run()
