# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from ..Common import TFileBase, TCategoryBase
from ..CommonDb import TDbCategory


class TMain(TFileBase):
    async def Save(self, aParam: TDbCategory):
        ConfFile = self.Parent.GetFile()
        Dir = ConfFile.replace('.txt', '')
        os.makedirs(Dir, exist_ok=True)

        Category = TCategoryBase(self.Parent)
        Category.Dbl = aParam
        with open(ConfFile, 'w', encoding='utf-8') as F:
            F.write(Category.Visualize())
