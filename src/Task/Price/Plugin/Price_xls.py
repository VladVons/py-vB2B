# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from xlrd import open_workbook
#
from .Common import TPriceBase


class TPrice_xls(TPriceBase):
    async def _Load(self):
        ConfFile = self.Parent.GetFile()
        WB = open_workbook(ConfFile)

        Sheet = self.Parent.Conf.get('Sheet')
        if (Sheet):
            WS = WB.sheet_by_name(Sheet)
        else:
            WS = WB.sheet_by_index(0)

        ConfFields = self.Parent.Conf.get('Fields')
        ConfSkip = self.Parent.Conf.get('Skip', 0)
        for i in range(ConfSkip, WS.nrows):
            Data = {'No': i}
            for Field, FieldIdx in ConfFields.items():
                Val = WS.cell(i, FieldIdx - 1).value
                Data[Field] = Val
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
