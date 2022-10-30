# Created: 2022.02.14
# Author:  Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import aiohttp
from .FormBase import TFormBase


class TForm(TFormBase):
    Title = 'About'

    async def _Render(self):
        Info = self.Info
        Info['aiohttp'] = aiohttp.__version__
        Info['ip'] = self.Request.remote

        Arr = ['%s: %s' % (Key, Val) for Key, Val in sorted(self.Info.items())]
        self.Data.Info = '<br>\n'.join(Arr)
