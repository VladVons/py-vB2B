# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import gspread
#
from Inc.ParserX.Common import TPluginBase
from .Price import TPricePC, TPriceMonit


class TIn_Price_pl01_xlsx(TPluginBase):
    def Download(self, aUrl: str, aFile: str) -> bool:
        # need auth file: '~/.config/gspread/service_account.json'
        GSA = gspread.service_account()
        SH = GSA.open_by_url(aUrl)
        Data = SH.export(format = gspread.utils.ExportFormat.EXCEL)
        with open(aFile, 'wb') as F:
            F.write(Data)
            return True

    async def Run(self):
        Url = self.Conf.GetKey('url_gspread')
        if (Url):
            File = self.GetFile()
            if (not os.path.isfile(File)):
                self.Download(Url, File)

        Res = {}

        # --- Computer
        Price = TPricePC(self)
        Engine = Price.InitEngine()
        Price.SetSheet('COMPUTERS')
        await Price.Load()

        FieldAvg = 'price'
        Fields =  Price.Dbl.GetFields()
        Fields.remove(FieldAvg)
        Dbl = Price.Dbl.Group(Fields, [FieldAvg])
        for Rec in Dbl:
            Avg = Rec.GetField(FieldAvg) / Rec.count
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()
        Dbl.Sort(['model', 'cpu', 'ram_size'])
        Res['TDbCompPC'] = Dbl

        # --- Monitor
        Price = TPriceMonit(self)
        Price.InitEngine(Engine)
        Price.SetSheet('MONITORS')
        await Price.Load()

        FieldAvg = 'price'
        Fields =  Price.Dbl.GetFields()
        Fields.remove(FieldAvg)
        Dbl = Price.Dbl.Group(Fields, [FieldAvg])
        for Rec in Dbl:
            Avg = Rec.GetField(FieldAvg) / Rec.count
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()
        Dbl.Sort(['model', 'screen'])
        Res['TDbCompMonit'] = Dbl

        return Res
