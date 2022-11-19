# Created: 2022.10.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import json
import time
#
from Inc.Util.Arr import Parts
from Inc.Log import TLog, TEchoFile
from ..Common import TFileBase

def DSplit(aFunc: callable):
    def Wrapper(aData: list, aMax: int) -> list[str]:
        Res = []
        for Part in Parts(aData, aMax):
            Data = aFunc(Part, aMax)
            Res.append(re.sub(r'\s+', ' ', Data).strip())
        return Res
    return Wrapper


class TLogEx(TLog):
    def Write(self, aData):
        self._Write({'aM': aData}, [])

class TSql():
    def __init__(self):
        self.Prefix = 'oc_'
        self.Parts = 100
        self.Now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.Escape = ''.maketrans({
            '<': '&lt;',
            '>': '&gt;',
            '&': '&amp;',
            "'": '&apos;',
            '"': '&quot;'
            })


    def Product_Clear(self):
        Res = []
        Res.append('# Product_Clear')
        Res.append(f'DELETE FROM {self.Prefix}product;')
        Res.append(f'DELETE FROM {self.Prefix}product_to_category;')
        Res.append(f'DELETE FROM {self.Prefix}product_to_store;')
        Res.append(f'DELETE FROM {self.Prefix}module WHERE code = "featured";')
        return '\n'.join(Res)

    def Category_Clear(self) -> str:
        Res = []
        Res.append('# Category_Clear')
        Res.append(f'DELETE FROM {self.Prefix}category;')
        Res.append(f'DELETE FROM {self.Prefix}category_description;')
        Res.append(f'DELETE FROM {self.Prefix}category_to_store;')
        return '\n'.join(Res)

    def Category_Create(self, aData: list) -> str:
        @DSplit
        def Category(aData: list, _aMax: int) -> str:
            Values = []
            for Row in aData:
                ParentId = Row['ParentId']
                Top = 0
                Status = 1
                if (ParentId == 1):
                    ParentId = 0
                    Top = 1
                Values.append(f'({Row["Id"]}, {ParentId}, {Status}, {Top}, "{self.Now}", "{self.Now}")')

            return f'''
                INSERT IGNORE INTO {self.Prefix}category (category_id, parent_id, status, top, date_added, date_modified)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                    date_modified = VALUES(date_modified);
            '''

        @DSplit
        def Category_Descr(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 1, "{Row["Name"].translate(self.Escape)}")'
                for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Prefix}category_description (category_id, language_id, name)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name);
            '''

        @DSplit
        def Category_ToStore(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 0)'
                for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Prefix}category_to_store (category_id, store_id)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        store_id = VALUES(store_id);
            '''

        Res = []
        Res.append('# Category')
        Res.append(f'UPDATE {self.Prefix}category SET status = 0;')
        Res += Category(aData, self.Parts)

        Res.append('# Category_Descr')
        Res += Category_Descr(aData, self.Parts)
        Res.append('# Category_ToStore')
        Res += Category_ToStore(aData, self.Parts)
        return '\n'.join(Res)

    def Product_Create(self, aData: list) -> str:
        @DSplit
        def Product(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 1, 1, {Row["PriceOut"]}, "{Row["Mpn"]}", "{Row["Code"]}", "{self.Now}", "{self.Now}")'
                for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Prefix}product (product_id, status, quantity, price, mpn, sku, date_added, date_modified)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        price = VALUES(price),
                        date_modified = VALUES(date_modified);
            '''

        @DSplit
        def Product_Descr(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 1, "{Row["Name"].translate(self.Escape)}")'
                    for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Prefix}product_description (product_id, language_id, name)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        name = VALUES(name);
            '''

        @DSplit
        def Product_ToCategory(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, {Row["CategoryId"]})'
                for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Prefix}product_to_category (product_id, category_id)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        category_id = VALUES(category_id);
            '''

        @DSplit
        def Product_ToStore(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 0)'
                for Row in aData
            ]
            return  f'''
                INSERT IGNORE INTO {self.Prefix}product_to_store (product_id, store_id)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        store_id = VALUES(store_id);
            '''

        Res = []
        Res.append('# Product')
        Res.append(f'UPDATE {self.Prefix}product SET status = 0;')
        Res += Product(aData, self.Parts)

        Res.append('# Product_Descr')
        Res += Product_Descr(aData, self.Parts)
        Res.append('# Product_ToCategory')
        Res += Product_ToCategory(aData, self.Parts)
        Res.append('# Product_ToStore')
        Res += Product_ToStore(aData, self.Parts)
        return '\n'.join(Res)

class TMain(TFileBase):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.InitLog()
        self.Sql = TSql()

    def InitLog(self):
        ConfFile = self.Parent.GetFile()
        if (os.path.exists(ConfFile)):
            os.remove(ConfFile)
        else:
            os.makedirs(os.path.dirname(ConfFile), exist_ok=True)

        EchoFile = TEchoFile(ConfFile)
        EchoFile.Fmt = ['aM']
        self.Log = TLogEx([EchoFile])

    async def Run(self):
        FileIn = self.Parent.Conf.GetKey('FileIn')
        with open(FileIn, 'r', encoding='utf-8') as File:
            Data = json.load(File)

        self.Log.Write(self.Sql.Category_Clear())
        self.Log.Write(self.Sql.Product_Clear())
        self.Log.Write(self.Sql.Category_Create(Data['Categories']))
        self.Log.Write(self.Sql.Product_Create(Data['Products']))
