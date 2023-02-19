# Created: 2023.02.13
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import json
#
from Inc.DbList  import TDbList, TDbRec
from Inc.DataClass import DataClass
from Inc.ParserX.Common import TFileBase
from Inc.ParserX.CommonSql import TSqlBase, DSplit, TLogEx, StripQuery
from ..CommonDb import TDbCategory, TDbProductEx
from ..In_Price_brain_net.Api import TApi


@DataClass
class TSqlConf():
    LangId: int
    TenantId: int
    PriceId: int
    Parts: int = 100
    DirImage: str = 'catalog/products'


class TCatalogToDb():
    def __init__(self, aDbl: TDbList):
        self.Dbl = aDbl
        self.BTree = self.Dbl.SearchAdd('id')

    def GetTree(self) -> dict:
        Res = {}
        for Rec in self.Dbl:
            ParentId = Rec.GetField('parent_id')
            Data = Res.get(ParentId, [])
            Data.append(Rec.GetField('id'))
            Res[ParentId] = Data
        return Res

    def GetSequence(self, aTree: dict) -> list:
        def Recurs(aTree: dict, aParentId: int) -> list:
            ResR = []
            for x in aTree.get(aParentId, {}):
                RecNo = self.BTree.Search(x)
                Rec = self.Dbl.RecGo(RecNo)
                ResR.append({'id': x, 'parent_id': aParentId, 'name': Rec.GetField('name')})
                if (x in aTree):
                    ResR += Recurs(aTree, x)
            return ResR
        return Recurs(aTree, 0)

    def Get(self) -> list:
        Tree = self.GetTree()
        Res = self.GetSequence(Tree)
        return Res


class TSql(TSqlBase):
    def __init__(self, aSqlConf: TSqlConf):
        super().__init__()
        self.Conf = aSqlConf

    def Product_Clear(self):
        Res = []
        Res.append('\n-- Product_Clear')

        Query = f'''
            delete from ref_product_image
            where product_id in (
                select id
                from ref_product
                where tenant_id = {self.Conf.TenantId}
            )
            ;
        '''
        Res.append(StripQuery(Query))

        Query = f'''
            delete from ref_product_to_category
            where product_id in (
                select id
                from ref_product
                where tenant_id = {self.Conf.TenantId}
            )
            ;
        '''
        Res.append(StripQuery(Query))

        return '\n'.join(Res)

    def Category_Create(self, aData: list) -> str:
        @DSplit
        def Category(aData: list, _aMax: int) -> str:
            Values = [f"({Row['id']}, {Row['parent_id']}, {self.Conf.TenantId})" for Row in aData]
            Res = f'''
                insert into ref_product_category (id, parent_id, tenant_id)
                values {', '.join(Values)}
                on conflict (id) do nothing
                ;
            '''
            return Res

        @DSplit
        def Category_Lang(aData: list, _aMax: int) -> str:
            Values = [
                f"({Row['id']}, {self.Conf.LangId}, '{Row['name'].translate(self.Escape)}')"
                for Row in aData
            ]
            Res = f'''
                insert into ref_product_category_lang (category_id, lang_id, title)
                values {', '.join(Values)}
                on conflict (category_id, lang_id) do update
                set title = excluded.title
                ;
            '''
            return Res

        Res = []
        Res.append('\n-- Category')
        Res += Category(aData, self.Conf.Parts)

        Res.append('\n-- Category_Lang')
        Res += Category_Lang(aData, self.Conf.Parts)

        return '\n'.join(Res)

    def Product_Create(self, aDbl: TDbProductEx) -> str:
        def GetImage(aCode: str) -> str:
            return self.Conf.DirImage + '/' + TApi.GetImageBase(aCode) + '.jpg'

        @DSplit
        def Product(aData: list, _aMax: int) -> str:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Value = f'({DbRec.GetField("id")}, {self.Conf.TenantId}, {bool(DbRec.GetField("available"))})'
                Values.append(Value)

            return f'''
                insert into ref_product (id, tenant_id, enabled)
                values {', '.join(Values)}
                on conflict (id) do update
                set enabled = excluded.enabled
                ;
            '''

        @DSplit
        def Product_Lang(aData: list, _aMax: int) -> str:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Name = DbRec.GetField('name').translate(self.Escape)
                Descr = DbRec.GetField('descr', '').translate(self.Escape)
                Feature = DbRec.GetField('feature', '')
                Feature = json.dumps(Feature, ensure_ascii=False).replace("'", '`')
                Value = f"({DbRec.GetField('id')}, {self.Conf.LangId}, '{Name}', '{Descr}', '{Feature}')"
                Values.append(Value)

            Res = f'''
                insert into ref_product_lang (product_id, lang_id, title, descr, feature)
                values {', '.join(Values)}
                on conflict (product_id, lang_id) do update
                set title = excluded.title, feature = excluded.feature, descr = excluded.descr
                ;
            '''
            return Res

        @DSplit
        def Product_Image(aData: list, _aMax: int) -> str:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                ProductId = DbRec.GetField('id')
                for Image in DbRec.GetField('image', []):
                    Value = f"({ProductId}, '{Image}')"
                    Values.append(Value)

            Res = f'''
                insert into ref_product_image (product_id, image)
                values {', '.join(Values)}
                ;
            '''
            return Res

        @DSplit
        def Product_ToCategory(aData: list, _aMax: int) -> str:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Values.append(f"({DbRec.GetField('id')}, {DbRec.GetField('category_id')})")

            Res = f'''
                insert into ref_product_to_category (product_id, category_id)
                values {', '.join(Values)}
                ;
            '''
            return Res

        @DSplit
        def Product_Price(aData: list, _aMax: int) -> str:
            nonlocal DbRec

            Values = []
            for Row in aData:
                DbRec.Data = Row
                Value = f"({DbRec.GetField('id')}, {self.Conf.PriceId}, {DbRec.GetField('price')})"
                Values.append(Value)

            Res = f'''
                insert into ref_product_price (product_id, price_id, price)
                values {', '.join(Values)}
                on conflict (product_id, price_id, qty) do update
                set price = excluded.price
                ;
            '''
            return Res


        DbRec = TDbRec()
        DbRec.Fields = aDbl.Rec.Fields

        Res = []
        Res.append('\n-- Product')
        Res += Product(aDbl.Data, self.Conf.Parts)
        Res.append('\n-- Product_Lang')
        Res += Product_Lang(aDbl.Data, self.Conf.Parts)
        Res.append('\n-- Product_Image')
        Res += Product_Image(aDbl.Data, self.Conf.Parts)
        Res.append('\n-- Product_ToCategory')
        Res += Product_ToCategory(aDbl.Data, self.Conf.Parts)
        Res.append('\n-- Product_Price')
        Res += Product_Price(aDbl.Data, self.Conf.Parts)
        return '\n'.join(Res)


class TMain(TFileBase):
    def __init__(self, aParent):
        super().__init__(aParent)

        ConfFile = self.Parent.GetFile()
        self.LogEx = TLogEx()
        self.LogEx = self.LogEx.Init(ConfFile)

        SqlDef = self.Parent.Conf.GetKey('sql', {})
        SqlConf = TSqlConf(
            DirImage = self.Parent.Conf.GetKey('site_image'),
            TenantId = SqlDef.get('tenant_id'),
            LangId = SqlDef.get('lang_id'),
            PriceId = SqlDef.get('price_id'),
            Parts = SqlDef.get('parts', 25)
        )
        self.Sql = TSql(SqlConf)

    def Save(self, aDbCategory: TDbCategory, aDbProductEx: TDbProductEx):
        self.LogEx.Write('-- Generated by TOut_vShop_sql plugin')

        Data = TCatalogToDb(aDbCategory).Get()
        self.LogEx.Write(self.Sql.Category_Create(Data))

        self.LogEx.Write(self.Sql.Product_Clear())
        self.LogEx.Write(self.Sql.Product_Create(aDbProductEx))
