# Created: 2023.01.24
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Price import TPrice
from ..Common import TPluginBase


class TIn_Price_pl01_xlsx(TPluginBase):
    async def Run(self):
        Price = TPrice(self)
        await Price.Load()

        FieldAvg = 'Price'
        Fields =  Price.Dbl.Fields.GetList()
        Fields.remove(FieldAvg)
        Dbl = Price.Dbl.Group(Fields, [FieldAvg])
        for Rec in Dbl:
            Avg = Rec.GetField(FieldAvg) / Rec.GetField('Count')
            Rec.SetField(FieldAvg, Avg)
            Rec.Flush()

        Dbl.Sort(['Model', 'CPU', 'RamSize'])
        return {'TDbCompPC': Dbl}
