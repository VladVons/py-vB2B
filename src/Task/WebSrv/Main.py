# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from Inc.WebSrv.WebSrv import TWebSrvBase
from IncP.Log import Log
from .Session import Session
from .Routes import rErr_404


class TWebSrv(TWebSrvBase):
    async def _FormCreateUser(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('Name')

        await Session.Update(aRequest)
        if (not Session.Data.get('UserId')) and (Name != 'login'):
            Redirect = 'login?url=%s' % (Name)
            raise web.HTTPFound(location = Redirect)

        return await self._FormCreate(aRequest, Name)

    async def RunApp(self):
        Log.Print(1, 'i', f'WebSrv.RunApp() on port {self.SrvConf.Port}')

        App = self.CreateApp()
        self.Conf.ErroMiddleware = {
            404: rErr_404
        }
        await self.Run(App)
