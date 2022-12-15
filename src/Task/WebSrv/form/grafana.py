# Created: 2022.12.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .FormBase import TFormBase


class TForm(TFormBase):
    async def _Render(self):
        print('---grafana', self.Request.query_string)
