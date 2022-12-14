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
from Inc.DataClass import DataClass
from ..Common import TFileBase
from ..In_Price_brain_net.Api import TApi


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


@DataClass
class TSqlConf():
    Prefix: str = 'oc_'
    Parts: int = 100
    DirImage: str = 'catalog/products'


class TSql():
    def __init__(self, aSqlConf: TSqlConf):
        self.Conf = aSqlConf
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
        Res.append('\n# Product_Clear')
        Res.append(f'DELETE FROM {self.Conf.Prefix}product;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}product_to_category;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}product_to_store;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}seo_url WHERE query LIKE "product_%";')
        Res.append(f'DELETE FROM {self.Conf.Prefix}module WHERE code = "featured";')
        return '\n'.join(Res)

    def Category_Clear(self) -> str:
        Res = []
        Res.append('\n# Category_Clear')
        Res.append(f'DELETE FROM {self.Conf.Prefix}category;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}category_description;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}category_to_store;')
        Res.append(f'DELETE FROM {self.Conf.Prefix}seo_url WHERE query LIKE "category_%";')
        Res.append(f'DELETE FROM {self.Conf.Prefix}category_path;')
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
                INSERT IGNORE INTO {self.Conf.Prefix}category (category_id, parent_id, status, top, date_added, date_modified)
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
                INSERT IGNORE INTO {self.Conf.Prefix}category_description (category_id, language_id, name)
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
                INSERT IGNORE INTO {self.Conf.Prefix}category_to_store (category_id, store_id)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        store_id = VALUES(store_id);
            '''

        def Category_Path(aData: list) -> str:
            @DSplit
            def GetSQL(aData: list, _aMax: int) -> str:
                Values = [
                    f'({Row[0]}, {Row[1]}, {Row[2]})'
                    for Row in aData
                ]
                return f'''
                    INSERT INTO {self.Conf.Prefix}category_path (category_id, path_id, level)
                        VALUES {", ".join(Values)}
                '''

            def GetTree() -> dict:
                nonlocal aData

                Res = {}
                for x in aData:
                    ParentId = x['ParentId']
                    Data = Res.get(ParentId, [])
                    Data.append(x['Id'])
                    Res[ParentId] = Data
                return Res

            def Recurs(aIds: list[int], aPath: list[int]):
                nonlocal Tree

                Res = []
                for Id in aIds:
                    Items = Tree.get(Id)
                    if (Items):
                        Res += Recurs(Items, aPath + [Id])
                    else:
                        for Idx, Path in enumerate(aPath + [Id]):
                            Res.append([Id, Path, Idx])
                return Res

            Tree = GetTree()
            Data = Recurs(Tree[1], [])
            return GetSQL(Data, self.Conf.Parts)


        Res = []
        Res.append('\n# Category')
        Res.append(f'UPDATE {self.Conf.Prefix}category SET status = 0;')
        Res += Category(aData, self.Conf.Parts)

        Res.append('\n# Category_Descr')
        Res += Category_Descr(aData, self.Conf.Parts)
        Res.append('\n# Category_ToStore')
        Res += Category_ToStore(aData, self.Conf.Parts)
        Res.append('\n# Category_Path')

        Res += Category_Path(aData)
        return '\n'.join(Res)

    def Product_Create(self, aData: list) -> str:
        def GetImage(aCode: str) -> str:
            return self.Conf.DirImage + '/' + TApi.GetImageBase(aCode) + '.jpg'

        @DSplit
        def Product(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["Id"]}, 1, 1, {Row["PriceOut"]}, "{Row["Mpn"]}", "{Row["Code"]}", "{GetImage(Row["Code"])}", "{self.Now}", "{self.Now}")'
                for Row in aData
            ]
            return f'''
                INSERT IGNORE INTO {self.Conf.Prefix}product (product_id, status, quantity, price, mpn, sku, image, date_added, date_modified)
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
                INSERT IGNORE INTO {self.Conf.Prefix}product_description (product_id, language_id, name)
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
                INSERT IGNORE INTO {self.Conf.Prefix}product_to_category (product_id, category_id)
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
                INSERT IGNORE INTO {self.Conf.Prefix}product_to_store (product_id, store_id)
                    VALUES {", ".join(Values)}
                    ON DUPLICATE KEY UPDATE
                        store_id = VALUES(store_id);
            '''

        Res = []
        Res.append('\n# Product')
        Res.append(f'UPDATE {self.Conf.Prefix}product SET status = 0;')
        Res += Product(aData, self.Conf.Parts)

        Res.append('\n# Product_Descr')
        Res += Product_Descr(aData, self.Conf.Parts)
        Res.append('\n# Product_ToCategory')
        Res += Product_ToCategory(aData, self.Conf.Parts)
        Res.append('\n# Product_ToStore')
        Res += Product_ToStore(aData, self.Conf.Parts)
        return '\n'.join(Res)


class TMain(TFileBase):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.InitLog()

        SqlConf = TSqlConf(
            DirImage = self.Parent.Conf.GetKey('SiteImage')
        )
        self.Sql = TSql(SqlConf)

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

        self.Log.Write('# Generated by TOut_OpenCart3_sql plugin')
        self.Log.Write(self.Sql.Category_Clear())
        self.Log.Write(self.Sql.Product_Clear())
        self.Log.Write(self.Sql.Category_Create(Data['Categories']))
        self.Log.Write(self.Sql.Product_Create(Data['Products']))
