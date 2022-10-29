# Created: 2022.03.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Session import Session
from .FormBase import TFormBase


class TForm(TFormBase):
    Title = 'Index'
    Pages = {
        '/form/price_list': 'sites list'
    }

    async def _Render(self):
        self.Data.Pages = {
            Key: Val
            for Key, Val in self.Pages.items()
            if (Session.CheckUserAccess(Key))
        }
