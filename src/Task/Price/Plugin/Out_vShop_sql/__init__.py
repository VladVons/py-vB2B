# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.ParserX.Common import TPluginBase
from .Main import TMain


class TOut_vShop_sql(TPluginBase):
    async def Run(self):
        DbCategory = self.GetParamDependsIdx('TDbCategory')
        DbProductEx = self.GetParamDependsIdx('TDbProductEx')

        Main = TMain(self)
        Main.Save(DbCategory, DbProductEx)
