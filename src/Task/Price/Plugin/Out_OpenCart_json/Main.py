# Created: 2022.10.15
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from ..Category import TDbCategory
from ..Common import TFileBase
from ..CommonDb import TDbPrice


class TMain(TFileBase):
    async def Save(self, aDbPrice: TDbPrice, aDbCategory: TDbCategory, aCategoryMargins: dict):
        Category = []
        for Rec in aDbCategory:
            Data = {
                'id': Rec.GetField('id'),
                'parent_id': Rec.GetField('parent_id'),
                'name': Rec.GetField('name')
            }
            Category.append(Data)
            await self.Sleep.Update()

        # TransField =     {
        #     'mpn': 'articul',
        #     'id': 'code',
        #     'name': 'name',
        #     'category_id': 'category_id',
        #     'image': 'image',
        #     'price': 'priceIn'
        # }
        TransField =     {
            'mpn': 'mpn',
            'id': 'id',
            'code': 'code',
            'name': 'name',
            'category_id': 'category_id',
            'image': 'image',
            'price': 'price_in'
        }

        Products = []
        for Rec in aDbPrice:
            Data = {}
            for Key, Val in TransField.items():
                Data[Val] = Rec.GetField(Key)
            CategoryId = Rec.GetField('category_id')
            Data['price_out'] = round(Rec.GetField('price') * aCategoryMargins.get(CategoryId, 1), 1)
            Data['quantity'] = 1
            Products.append(Data)

            await self.Sleep.Update()

        Data = {'categories': Category, 'products': Products}

        ConfFile = self.Parent.GetFile()
        os.makedirs(os.path.dirname(ConfFile), exist_ok=True)
        with open(ConfFile, 'w', encoding='utf-8') as File:
            json.dump(Data, File, indent=2, ensure_ascii=False)
