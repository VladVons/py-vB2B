# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from aiohttp import web
#
from Inc.UtilP.WebSrv.WebSrv import TWebSrvBase
from IncP.Log import Log
from .form.info import TForm
from .Session import Session

class TWebSrv(TWebSrvBase):
    async def _FormCreateUser(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('Name')

        Public = ['grafana']
        await Session.Update(aRequest)
        if (not Session.Data.get('UserId')) and (Name != 'login') and (not Name in Public):
            Redirect = 'login?url=%s' % (Name)
            raise web.HTTPFound(location = Redirect)

        return await self._FormCreate(aRequest, Name)

    @staticmethod
    async def _Err_404(aRequest: web.Request):
        #https://docs.aiohttp.org/en/stable/web_advanced.html
        #Routes = web.RouteTableDef()

        Form = TForm(aRequest, 'info.tpl.html')
        Form.Data['Info'] = 'Page not found'
        Res = await Form.Render()
        Res.set_status(404, Form.Data['Info'])
        return Res

    async def RunApp(self):
        Log.Print(1, 'i', f'WebSrv.RunApp() on port {self._SrvConf.Port}')

        App = self.CreateApp(aErroMiddleware = {404: self._Err_404})
        await self.Run(App)
