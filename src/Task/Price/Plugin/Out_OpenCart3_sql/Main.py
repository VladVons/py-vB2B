# Created: 2022.10.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DataClass import DDataClass
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DSplit, TLogEx
from ..In_Price_brain_net.Api import TApi


@DDataClass
class TSqlConf():
    Parts: int = 100
    DirImage: str = 'catalog/products'
    Prefix = 'oc_'


class TSql(TSqlBase):
    def __init__(self, aSqlConf: TSqlConf):
        super().__init__()
        self.Conf = aSqlConf

    def Product_Clear(self):
        Res = []
        Res.append('\n# Product_Clear')
        Res.append(f'delete from {self.Conf.Prefix}product;')
        Res.append(f'delete from {self.Conf.Prefix}product_to_category;')
        Res.append(f'delete from {self.Conf.Prefix}product_to_store;')
        Res.append(f'delete from {self.Conf.Prefix}seo_url WHERE query LIKE "product_%";')
        Res.append(f'delete from {self.Conf.Prefix}module WHERE code = "featured";')
        return '\n'.join(Res)

    def Category_Clear(self) -> str:
        Res = []
        Res.append('\n# Category_Clear')
        Res.append(f'delete from {self.Conf.Prefix}category;')
        Res.append(f'delete from {self.Conf.Prefix}category_description;')
        Res.append(f'delete from {self.Conf.Prefix}category_to_store;')
        Res.append(f'delete from {self.Conf.Prefix}seo_url WHERE query LIKE "category_%";')
        Res.append(f'delete from {self.Conf.Prefix}category_path;')
        return '\n'.join(Res)

    def Category_Create(self, aData: list) -> str:
        @DSplit
        def Category(aData: list, _aMax: int) -> str:
            Values = []
            for Row in aData:
                ParentId = Row['parent_id']
                Top = 0
                Status = 1
                if (ParentId == 1):
                    ParentId = 0
                    Top = 1
                Values.append(f'({Row["id"]}, {ParentId}, {Status}, {Top}, "{self.Now}", "{self.Now}")')

            return f'''
                insert ignore into {self.Conf.Prefix}category (category_id, parent_id, status, top, date_added, date_modified)
                values {", ".join(Values)}
                on duplicate key update
                date_modified = values(date_modified);
            '''

        @DSplit
        def Category_Descr(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["id"]}, 1, "{Row["name"].translate(self.Escape)}")'
                for Row in aData
            ]
            return f'''
                insert ignore into {self.Conf.Prefix}category_description (category_id, language_id, name)
                values {", ".join(Values)}
                on duplicate key update
                name = values(name);
            '''

        @DSplit
        def Category_ToStore(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["id"]}, 0)'
                for Row in aData
            ]
            return f'''
                insert ignore into {self.Conf.Prefix}category_to_store (category_id, store_id)
                values {", ".join(Values)}
                on duplicate key update
                store_id = values(store_id)
                ;
            '''

        def Category_Path(aData: list) -> str:
            @DSplit
            def GetSQL(aData: list, _aMax: int) -> str:
                Values = [
                    f'({Row[0]}, {Row[1]}, {Row[2]})'
                    for Row in aData
                ]
                return f'''
                    insert into {self.Conf.Prefix}category_path (category_id, path_id, level)
                    values {", ".join(Values)}
                '''

            def GetTree() -> dict:
                nonlocal aData

                Res = {}
                for x in aData:
                    ParentId = x['parent_id']
                    Data = Res.get(ParentId, [])
                    Data.append(x['id'])
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
        Res.append(f'update {self.Conf.Prefix}category SET status = 0;')
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
                f'({Row["id"]}, 1, 1, {Row["price_out"]}, "{Row["mpn"]}", "{Row["code"]}", "{GetImage(Row["code"])}", "{self.Now}", "{self.Now}")'
                for Row in aData
            ]
            return f'''
                insert ignore into {self.Conf.Prefix}product (product_id, status, quantity, price, mpn, sku, image, date_added, date_modified)
                values {", ".join(Values)}
                on duplicate key update
                price = values(price), date_modified = VALUES(date_modified)
                ;
            '''

        @DSplit
        def Product_Descr(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["id"]}, 1, "{Row["name"].translate(self.Escape)}")'
                    for Row in aData
            ]
            return f'''
                insert ignore into {self.Conf.Prefix}product_description (product_id, language_id, name)
                values {", ".join(Values)}
                on duplicate key update
                name = values(name)
                ;
            '''

        @DSplit
        def Product_ToCategory(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["id"]}, {Row["category_id"]})'
                for Row in aData
            ]
            return f'''
                insert ignore into {self.Conf.Prefix}product_to_category (product_id, category_id)
                values {", ".join(Values)}
                on duplicate key update
                category_id = values(category_id)
                ;
            '''

        @DSplit
        def Product_ToStore(aData: list, _aMax: int) -> str:
            Values = [
                f'({Row["id"]}, 0)'
                for Row in aData
            ]
            return  f'''
                insert ignore into {self.Conf.Prefix}product_to_store (product_id, store_id)
                values {", ".join(Values)}
                on duplicate key update
                store_id = values(store_id)
                ;
            '''

        Res = []
        Res.append('\n# Product')
        Res.append(f'update {self.Conf.Prefix}product SET status = 0;')
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

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlConf = TSqlConf(
            Prefix = 'oc_',
            DirImage = self.Parent.Conf.GetKey('site_image')
        )
        self.Sql = TSql(SqlConf)

    def Save(self):
        FileIn = self.Parent.Conf.GetKey('file_in')
        with open(FileIn, 'r', encoding='utf-8') as File:
            Data = json.load(File)

        self.LogEx.Write('# Generated by TOut_OpenCart3_sql plugin')
        self.LogEx.Write(self.Sql.Category_Clear())
        self.LogEx.Write(self.Sql.Product_Clear())
        self.LogEx.Write(self.Sql.Category_Create(Data['categories']))
        self.LogEx.Write(self.Sql.Product_Create(Data['products']))
