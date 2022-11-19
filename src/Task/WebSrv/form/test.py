# Created: 2022.11.18
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
from .FormBase import TFormBase


class TForm(TFormBase):
    Title = 'Test'

    async def _Render(self):
        self.Data.Info = 'Passw: %s' % (os.getenv('Passw'))
