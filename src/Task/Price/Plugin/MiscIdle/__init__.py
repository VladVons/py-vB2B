# Created: 2022.10.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from ..Common import TPluginBase


class TMiscIdle(TPluginBase):
    async def Run(self):
        ConfSleep = self.Conf.GetKey('Sleep', 3)
        print('TMiscIdle.Run', ConfSleep)

        CntLoop = 0
        while True:
            print('TMiscIdle.Run.CntLoop', CntLoop)

            CntLoop += 1
            await asyncio.sleep(ConfSleep)
