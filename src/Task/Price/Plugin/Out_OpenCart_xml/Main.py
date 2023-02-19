# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
#
from Inc.ParserX.Common import TFileBase
from ..CommonDb import TDbPrice, TDbCategory


class TMain(TFileBase):
    @staticmethod
    def Prettify(aElem) -> str:
        Rough = ET.tostring(aElem, 'utf-8')
        Reparsed = minidom.parseString(Rough)
        return Reparsed.toprettyxml(indent = '\t')

    async def Save(self, aDbPrice: TDbPrice, aDbPriceJoin: TDbPrice, aDbCategory: TDbCategory, aCategoryMargins: dict):
        Root = ET.Element('price')
        Element = ET.SubElement(Root, 'catalog')

        TableEscape = ''.maketrans({
            #'<': '&lt;',
            #'>': '&gt;',
            #'&': '&amp;',
            #"'": '&apos;',
            #'"': '&quot;'
            '<': '|',
            '>': '|',
            '&': '_',
            "'": '`',
            '"': '`'
            })

        # OpenCart root categories must be 0, not 1
        TableId = {1: 0}

        for Rec in aDbCategory:
            ParentId = Rec.GetField('parent_id')
            ItemA = ET.SubElement(Element, 'category', ID = str(Rec.GetField('id')), ParentID = str(TableId.get(ParentId, ParentId)))
            ItemA.text = Rec.GetField('name').translate(TableEscape)

            await self.Sleep.Update()

        TransField = {
            'mpn': 'articul',
            'id': 'code',
            'name': 'name',
            'category_id': 'category_id',
            'image': 'image'
        }

        BT = aDbPriceJoin.BeeTree.get('mpn')
        if (not BT):
            BT = aDbPriceJoin.SearchAdd('mpn')

        Element = ET.SubElement(Root, 'items')
        for Rec in aDbPrice:
            ItemA = ET.SubElement(Element, 'item')
            for Key, Val in TransField.items():
                ItemB = ET.SubElement(ItemA, Val)
                ItemB.text = str(Rec.GetField(Key)).translate(TableEscape)

            Mpn = Rec.GetField('mpn')
            RecNo = BT.Search(Mpn)
            if (RecNo >= 0):
                PriceMin = aDbPriceJoin.RecGo(RecNo).GetField('price')
            else:
                PriceMin = Rec.GetField('price')
            CategoryId = Rec.GetField('category_id')
            Price = PriceMin * aCategoryMargins.get(CategoryId, 1)

            ItemB = ET.SubElement(ItemA, 'price_in')
            ItemB.text = str(PriceMin)

            ItemB = ET.SubElement(ItemA, 'price_out')
            ItemB.text = '%0.2f' % (Price)

            ItemB = ET.SubElement(ItemA, 'quantity')
            ItemB.text = '1'

            await self.Sleep.Update()


        #Tree = ET.ElementTree(Root)
        #Tree.write(ConfFile, 'utf-8')
        Data = self.Prettify(Root)

        ConfFile = self.Parent.GetFile()
        os.makedirs(os.path.dirname(ConfFile), exist_ok=True)
        with open(ConfFile, 'w', encoding='utf-8') as File:
            File.write(Data)
