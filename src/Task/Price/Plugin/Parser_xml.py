# Created: 2023.02.08
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

import xml.dom.minidom as dom
#
from .Common import TEngine


class TParser_xml(TEngine):
    def _InitEngine(self, aFile: str):
        return dom.parse(aFile)

    async def _Load(self):
        Nodes = self._Engine.getElementsByTagName(self._Sheet)
        for Row in Nodes:
            self._Fill(Row)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
