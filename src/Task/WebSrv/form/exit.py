# Created: 2022.11.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import sys
import asyncio
#
from IncP.Log import Log
from Task.Queue.Main import TCall
from Task import Plugin
from .FormBase import TFormBase


class TForm(TFormBase):
    Title = 'Exit'

    async def Exit(self, aSleep: int):
        await asyncio.sleep(aSleep)
        Log.Print(1, 'i', 'Exit')
        sys.exit()

    async def _Render(self):
        Wait = 3
        await Plugin.Post(self, {
            'to': 'TQueue',
            'type': 'add',
            'call': TCall(self.Exit, [Wait])
        })

        self.Data.Info = f'Is about to exit() application in {Wait} sec'
        Log.Print(1, 'i', self.Data.Info)
