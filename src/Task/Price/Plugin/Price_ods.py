# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from pyexcel_ods import get_data
#
from .Common import TPriceBase


class TPrice_ods(TPriceBase):
    async def _Load(self):
        ConfFile = self.Parent.GetFile()
        Data = get_data(ConfFile)

        ConfSheet = self.Parent.Conf.get('Sheet')
        if (ConfSheet):
            Sheet = ConfSheet
        else:
            Sheet = list(Data.keys())[0]

        ConfSkip = self.Parent.Conf.get('Skip', 0)
        Rows = Data.get(Sheet)

        ConfFields = self.Parent.Conf.get('Fields')
        for i in range(ConfSkip, len(Rows)):
            Data = {'No': i}
            for Field, (FieldIdx, _) in ConfFields.items():
                Val = Rows[i][FieldIdx - 1]
                Data[Field] = Val
            self._Fill(Data)
            await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
