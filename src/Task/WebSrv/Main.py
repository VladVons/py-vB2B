# Created: 2022.10.19
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import asyncio
from aiohttp import web
from aiohttp_session.cookie_storage import EncryptedCookieStorage
import aiohttp_jinja2
import aiohttp_session
import jinja2
#
from IncP.Log import Log
from .Session import Session
from .Routes import rErr_404
from .Common import FileReader


def CreateErroMiddleware(aOverrides):
    @web.middleware
    async def ErroMiddleware(request: web.Request, handler):
        try:
            return await handler(request)
        except web.HTTPException as E:
            Override = aOverrides.get(E.status)
            if (Override):
                return await Override(request)
            raise E
        #except Exception as E:
        #    pass
    return ErroMiddleware

class TForm():
    def __init__(self, aParent: 'TWebSrv'):
        self.Parent = aParent

    async def Create(self, aRequest: web.Request, aName: str) -> web.Response:
        FormDir = '%s/%s' % (self.Parent.DirRoot, self.Parent.DirForm)
        if (not os.path.isfile('%s/%s%s' % (FormDir, aName, self.Parent.TplExt))):
            aName = 'err_code'

        for Module, Class in [(aName, 'TForm'), ('FormBase', 'TFormBase')]:
            try:
                Path = FormDir + '/' + Module
                Mod = __import__(Path.replace('/', '.'), None, None, [Class])
                TClass = getattr(Mod, Class)
                break
            except ModuleNotFoundError:
                pass
        Res = TClass(aRequest, aName + self.Parent.TplExt)
        Res.Parent = self
        return Res

    async def CreateAuth(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info.get('Name')

        await Session.Update(aRequest)
        if (not Session.Data.get('UserId')) and (Name != 'login'):
            Redirect = 'login?url=%s' % (Name)
            raise web.HTTPFound(location = Redirect)

        return await self.Create(aRequest, Name)


class TWebSrv():
    def __init__(self, aConf: dict):
        self.Conf = aConf

        self.DirRoot = 'Task/WebSrv'
        self.DirForm = 'form'
        self.DirDownload = 'download'
        self.Dir3w = 'www'
        self.TplExt = '.tpl.html'

        self.Form = TForm(self)

    async def _rDownload(self, aRequest: web.Request) -> web.Response:
        Name = aRequest.match_info['Name']
        File = '%s/%s/%s' % (self.DirRoot, self.DirDownload, Name)
        if (not os.path.exists(File)):
            return web.Response(body='File %s does not exist' % (Name), status=404)

        Headers = {'Content-disposition': 'attachment; filename=%s' % (Name)}
        # pylint: disable-next=no-value-for-parameter
        return web.Response(body=FileReader(aFile=File), headers=Headers)

    async def _rForm(self, aRequest: web.Request) -> web.Response:
        Form = await self.Form.CreateAuth(aRequest)
        return await Form.Render()

    async def _rIndex(self, aRequest: web.Request) -> web.Response:
        Form = await self.Form.Create(aRequest, 'index')
        return await Form.Render()

    async def _Run(self, aApp: web.Application):
        Port = self.Conf.get('Port', 8080)
        Log.Print(1, 'i', 'WebSrv on port %s' % (Port))

        ## pylint: disable-next=protected-access
        ##await web._run_app(App, host = '0.0.0.0', port = Port+1, shutdown_timeout = 60.0,  keepalive_timeout = 75.0)

        Runner = web.AppRunner(aApp)
        try:
            await Runner.setup()
            Site = web.TCPSite(Runner, host = '0.0.0.0', port = Port)
            await Site.start()
            while True:
                await asyncio.sleep(60)
        finally:
                await Runner.cleanup()

    async def Run(self):
        ConfClientMaxizeFile = self.Conf.get('ClientMaxizeFile', 1024**2)
        App = web.Application(client_max_size = ConfClientMaxizeFile)
        App.add_routes([
            web.get('/', self._rIndex),
            web.get('/form/{Name}', self._rForm),
            web.post('/form/{Name}', self._rForm),
            web.get('/download/{Name:.*}', self._rDownload)
        ])

        App.router.add_static('/', self.DirRoot + '/' + self.Dir3w, show_index=True, follow_symlinks=True)

        aiohttp_session.setup(App, EncryptedCookieStorage(b'my 32 bytes key. qwertyuiopasdfg'))

        Middleware = CreateErroMiddleware({
            404: rErr_404
        })
        App.middlewares.append(Middleware)

        aiohttp_jinja2.setup(App, loader=jinja2.FileSystemLoader(self.DirRoot + '/' + self.DirForm))
        await self._Run(App)

