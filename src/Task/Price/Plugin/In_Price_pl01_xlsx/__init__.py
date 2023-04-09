# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import gspread
#
from Inc.ParserX.Common import TPluginBase
from .Price import TPricePC, TPriceMonit
from ..CommonDb import TDbCategory, TDbProductEx


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

        DbProductEx = TDbProductEx()

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
            Avg = round(Rec.GetField(FieldAvg) / Rec.count, 1)
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()

            DbProductEx.RecAdd().SetAsDict({
                'category_id': 1,
                'mpn': Rec.model,
                'name': Rec.title,
                'price': Avg,
                'available': Rec.count
                })
        #Dbl.Sort(['model', 'cpu', 'ram_size'])

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
            Avg = round(Rec.GetField(FieldAvg) / Rec.count, 1)
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()

            DbProductEx.RecAdd().SetAsDict({
                'category_id': 2,
                'mpn': Rec.model,
                'name': Rec.title,
                'price': Avg,
                'available': Rec.count
                })
        #Dbl.Sort(['model', 'screen'])

        DbCategory = TDbCategory()
        Rec = DbCategory.RecAdd().SetAsDict({'id': 1, 'parent_id': 0, 'name': 'Computer'})
        Rec = DbCategory.RecAdd().SetAsDict({'id': 2, 'parent_id': 0, 'name': 'Monitor'})
        return {'TDbCategory': DbCategory, 'TDbProductEx': DbProductEx}
