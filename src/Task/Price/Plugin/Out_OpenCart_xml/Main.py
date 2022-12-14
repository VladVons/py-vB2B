# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
#
from ..Common import TFileBase
from ..CommonDb import TDbPrice, TDbCategory


class TMain(TFileBase):
    @staticmethod
    def Prettify(aElem) -> str:
        Rough = ET.tostring(aElem, 'utf-8')
        Reparsed = minidom.parseString(Rough)
        return Reparsed.toprettyxml(indent = '\t')

    async def Save(self, aDbPrice: TDbPrice, aDbPriceJoin: TDbPrice, aDbCategory: TDbCategory, aCategoryMargins: dict):
        Root = ET.Element('Price')
        Element = ET.SubElement(Root, 'Catalog')

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
            ParentId = Rec.GetField('ParentId')
            ItemA = ET.SubElement(Element, 'Category', ID = str(Rec.GetField('CategoryId')), ParentID = str(TableId.get(ParentId, ParentId)))
            ItemA.text = Rec.GetField('Name').translate(TableEscape)

            await self.Sleep.Update()

        TransField = {
            'Mpn': 'Articul',
            'Id': 'Code',
            'Name': 'Name',
            'CategoryId': 'CategoryID',
            'Image': 'Image'
        }

        BT = aDbPriceJoin.BeeTree.get('Mpn')
        if (not BT):
            BT = aDbPriceJoin.SearchAdd('Mpn')

        Element = ET.SubElement(Root, 'Items')
        for Rec in aDbPrice:
            ItemA = ET.SubElement(Element, 'Item')
            for Key, Val in TransField.items():
                ItemB = ET.SubElement(ItemA, Val)
                ItemB.text = str(Rec.GetField(Key)).translate(TableEscape)

            Mpn = Rec.GetField('Mpn')
            RecNo = BT.Search(Mpn)
            if (RecNo >= 0):
                PriceMin = aDbPriceJoin.RecGo(RecNo).GetField('Price')
            else:
                PriceMin = Rec.GetField('Price')
            CategoryId = Rec.GetField('CategoryId')
            Price = PriceMin * aCategoryMargins.get(CategoryId, 1)

            ItemB = ET.SubElement(ItemA, 'PriceIn')
            ItemB.text = str(PriceMin)

            ItemB = ET.SubElement(ItemA, 'PriceOut')
            ItemB.text = '%0.2f' % (Price)

            ItemB = ET.SubElement(ItemA, 'Quantity')
            ItemB.text = '1'

            await self.Sleep.Update()


        #Tree = ET.ElementTree(Root)
        #Tree.write(ConfFile, 'utf-8')
        Data = self.Prettify(Root)

        ConfFile = self.Parent.GetFile()
        os.makedirs(os.path.dirname(ConfFile), exist_ok=True)
        with open(ConfFile, 'w', encoding='utf-8') as File:
            File.write(Data)
