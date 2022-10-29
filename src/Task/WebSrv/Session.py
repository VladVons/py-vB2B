# Created: 2022.10.19
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import re
from aiohttp import web
import aiohttp_session
#
from IncP.Log import Log


class TSession():
    def __init__(self):
        self.Data = {}

    async def Update(self, aRequest: web.Request):
        self.Data = await aiohttp_session.get_session(aRequest)

    @staticmethod
    def _CheckUserAccess(aUrl: str, aUrls: list):
        if (aUrls):
            for x in aUrls:
                try:
                    if (x.strip()) and (not x.startswith('-')) and (re.match(x, aUrl)):
                        return True
                except Exception as E:
                    Log.Print(1, 'e', 'CheckUserAccess()', aE = E)
                    return False
        return False

    def CheckUserAccess(self, aUrl: str):
        #Allow = ['/$', '/form/login', '/form/about']
        Allow = ['.*']
        return (self._CheckUserAccess(aUrl, Allow))


Session = TSession()
