# Created: 2022.09.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import csv
#
from .Common import TFileDbl


class TParser_csv(TFileDbl):
    async def _Load(self):
        ConfFile = self.Parent.GetFile()
        ConfEncoding = self.Parent.Conf.get('Encoding', 'cp1251')
        with open(ConfFile, 'r',  encoding=ConfEncoding, errors='ignore') as File:
            Rows = csv.reader(File, delimiter = ',')

            ConfSkip = self.Parent.Conf.get('Skip', 0)
            for _i in range(ConfSkip):
                next(Rows)

            ConfFields = self.Parent.Conf.get('Fields')
            for RowNo, Row in enumerate(Rows, ConfSkip):
                Data = {'No': RowNo}
                for Field, FieldIdx in ConfFields.items():
                    Val = Row[FieldIdx - 1]
                    Data[Field] = Val
                self._Fill(Data)
                await self.Sleep.Update()

    def _Fill(self, aRow: dict):
        raise NotImplementedError()
