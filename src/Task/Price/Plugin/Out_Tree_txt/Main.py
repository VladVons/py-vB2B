# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import TFileBase, TCategoryBase
from ..CommonDb import TDbCategory


class TMain(TFileBase):
    async def Save(self, aParam: TDbCategory):
        ConfFile = self.Parent.GetFile()
        Category = TCategoryBase(self.Parent)
        Category.Dbl = aParam
        with open(ConfFile, 'w', encoding='utf-8') as F:
            F.write(Category.Visualize())
