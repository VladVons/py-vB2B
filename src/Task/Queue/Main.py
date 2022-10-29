# Created: 2020.10.20
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import asyncio
#
from Inc.DataClass import DataClass


@DataClass
class TCall():
    Func: callable
    Args: list = []


class TQueue():
    def __init__(self):
        self._Queue: list[TCall] = []

    async def _DoPost(self, _aOwner, aMsg: dict):
        if (aMsg.get('To') == self.__class__.__name__):
            if (aMsg.get('Type') == 'Add'):
                self.Add(aMsg.get('Call'))

    def Add(self, aCall: TCall):
        self._Queue.append(aCall)

    async def Run(self, aSleep: int = 1):
        while True:
            if (len(self._Queue) > 0):
                Call = self._Queue.pop()
                if (Call.Args):
                    await Call.Func(*Call.Args)
                else:
                    await Call.Func()
            await asyncio.sleep(aSleep)
