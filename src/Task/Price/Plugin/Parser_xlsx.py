# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from openpyxl import load_workbook
#
from .Common import TFileDbl


class TParser_xlsx(TFileDbl):
    async def _Load(self):
        ConfFile = self.Parent.GetFile()
        WB = load_workbook(ConfFile, read_only = True, data_only = True)

        ConfSheet = self.Parent.Conf.get('Sheet')
        if (ConfSheet):
            WS = WB[ConfSheet]
        else:
            WS = WB.active

        ConfFields = self.Parent.Conf.get('Fields')
        ConfSkip = self.Parent.Conf.get('Skip', 0)
        for RowNo, Row in enumerate(WS.rows):
            if (RowNo >= ConfSkip):
                Data = {'No': RowNo}
                for Field, FieldIdx in ConfFields.items():
                    Val = Row[FieldIdx - 1].value
                    Data[Field] = Val
                self._Fill(Data)
                await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
