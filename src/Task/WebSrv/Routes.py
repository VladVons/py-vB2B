# Created: 2021.02.26
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
#https://docs.aiohttp.org/en/stable/web_advanced.html
#https://docs.aiohttp.org/en/stable/web.html


from aiohttp import web
#
from .form.info import TForm


Routes = web.RouteTableDef()

async def rErr_404(aRequest: web.Request):
    Form = TForm(aRequest, 'info.tpl.html')
    Form.Data['Info'] = 'Page not found'
    Res = await Form.Render()
    Res.set_status(404, Form.Data['Info'])
    return Res

async def rErr_Def(aRequest: web.Request):
    return await rErr_404(aRequest)
