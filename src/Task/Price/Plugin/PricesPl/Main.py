# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..Common import TFileDbl
from ..CommonDb import TDbCompPricePl


class TMain(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCompPricePl())

    async def _Load(self):
        pass
