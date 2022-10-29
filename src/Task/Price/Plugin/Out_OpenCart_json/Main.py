# Created: 2022.10.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from ..Common import TFileBase, TDbPrice, TDbCategory


class TMain(TFileBase):
    async def Save(self, aDbPrice: TDbPrice, aDbCategory: TDbCategory, aCategoryMargins: dict):
        Category = []
        for Rec in aDbCategory:
            Data = {
                'Id': Rec.GetField('CategoryId'),
                'ParentId': Rec.GetField('ParentId'),
                'Name': Rec.GetField('Name')
            }
            Category.append(Data)
            await self.Sleep.Update()

        # TransField =     {
        #     'Mpn': 'Articul',
        #     'Id': 'Code',
        #     'Name': 'Name',
        #     'CategoryId': 'CategoryID',
        #     'Image': 'Image',
        #     'Price': 'PriceIn'
        # }
        TransField =     {
            'Mpn': 'Mpn',
            'Id': 'Id',
            'Name': 'Name',
            'CategoryId': 'CategoryId',
            'Image': 'Image',
            'Price': 'PriceIn'
        }

        Products = []
        for Rec in aDbPrice:
            Data = {}
            for Key, Val in TransField.items():
                Data[Val] = Rec.GetField(Key)
            CategoryId = Rec.GetField('CategoryId')
            Data['PriceOut'] = round(Rec.GetField('Price') * aCategoryMargins.get(CategoryId, 1), 1)
            Data['Quantity'] = 1
            Products.append(Data)

            await self.Sleep.Update()

        Data = {'Categories': Category, 'Products': Products}

        ConfFile = self.Parent.GetFile()
        os.makedirs(os.path.dirname(ConfFile), exist_ok=True)
        with open(ConfFile, 'w', encoding='utf-8') as File:
            json.dump(Data, File, indent=2, ensure_ascii=False)
