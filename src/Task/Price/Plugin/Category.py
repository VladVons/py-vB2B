# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.ParserX.Common import TFileDbl
from IncP.Log import Log
from .CommonDb import TDbPrice, TDbCategory


class TCategoryBase(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent, TDbCategory())

    async def _Load(self):
        raise NotImplementedError()

    def _GetTree(self) -> dict:
        Res = {}
        for Rec in self.Dbl:
            ParentId = Rec.GetField('parent_id')
            Data = Res.get(ParentId, [])
            Data.append([Rec.GetField('id'), 0])
            Res[ParentId] = Data
        return Res

    def Visualize(self) -> str:
        def ToChildRecurs(aCategory: list[int, int], aDepth: int) -> list[int, int]:
            nonlocal CategoryTree

            Res = []
            for Id, _Cnt in aCategory:
                Res.append([Id, aDepth])
                Items = CategoryTree.get(Id, [])
                if (Items):
                    ResChild = ToChildRecurs(Items, aDepth + 1)
                    if (ResChild):
                        Res += ResChild
            return Res

        CategoryTree = self._GetTree()
        Root = [[Id, 0] for Id, _Cnt in CategoryTree[1]]
        TreeDepth = ToChildRecurs(Root, 0)

        Res = []
        self.Dbl.SearchAdd('id')
        for Id, Depth in TreeDepth:
            RecNo = self.Dbl.Search('id', Id)
            Text = '  ' * Depth + '%s, %s' % (Id, self.Dbl.RecGo(RecNo).GetField('name'))
            Res.append(Text)
        return '\n'.join(Res)

    def LoadFileMargin(self, aFile: str) -> dict:
        Res = {}
        with open(aFile, 'r', encoding='utf-8') as F:
            for Line in F.readlines():
                Arr = Line.split('-')
                if (len(Arr) == 2):
                    Val = Arr[1].strip()
                    if (Val.isdigit()):
                        Id = Arr[0].strip().split(',')[0]
                        Margin = int(Val) / 100 + 1
                        Res[Id] = Margin
        return Res
    def SubMargin(self) -> dict:
        def ToChildRecurs(aCategory: list[int, int], aMargin: float) -> dict:
            nonlocal CategoryTree, Margins

            Res = {}
            for Id, _Cnt in aCategory:
                Margin = Margins.get(str(Id), aMargin)
                Res[Id] = Margin
                Items = CategoryTree.get(Id, [])
                if (Items):
                    ResChild = ToChildRecurs(Items, Margin)
                    Res.update(ResChild)
            return Res

        ConfMargin = self.Parent.Conf.get('margin', {})
        if (ConfMargin):
            Margins = ConfMargin.get('id', {})
            MarginFile = ConfMargin.get('file')
            if (MarginFile):
                if (os.path.exists(MarginFile)):
                    MarginEx = self.LoadFileMargin(MarginFile)
                    Margins.update(MarginEx)
                else:
                    Log.Print(1, 'e', f'File not exists {MarginFile}')
            CategoryTree = self._GetTree()
            Root = [[Id, 0] for Id, _Cnt in CategoryTree[1]]
            Res = ToChildRecurs(Root, ConfMargin.get('default', 1.0))
            return Res

    def SubTreeId(self, aCategories: list[int]) -> dict:
        def ToChildRecurs(aCategoryId: int) -> list:
            nonlocal CategoryTree

            Res = []
            Items = CategoryTree.get(aCategoryId, [])
            for Id, _Cnt in Items:
                ResChild = ToChildRecurs(Id)
                if (ResChild):
                    Res += ResChild
                Res.append(Id)
            return Res

        CategoryTree = self._GetTree()
        Res = {x: ToChildRecurs(x) for x in aCategories}
        return Res

    def SubCount(self, aProductsInCategory: dict) -> dict:
        def ToChildRecurs(aCategory: list[int, int]) -> int:
            nonlocal CategoryTree

            Res = 0
            Items = CategoryTree.get(aCategory[0], [])
            for Idx, (Id, Cnt) in enumerate(Items):
                ResChild = ToChildRecurs([Id, Cnt])
                SKU = aProductsInCategory.get(Id, 0)
                Items[Idx][1] = ResChild + SKU
                Res += Items[Idx][1]
            return Res

        CategoryTree = self._GetTree()

        # parse from top root tree
        Res = CategoryTree[1]
        for Idx, x in enumerate(Res):
            Cnt = ToChildRecurs(x)
            Res[Idx][1] = Cnt

        CategoryCount = {}
        for Key, Val in CategoryTree.items():
            Sum = 0
            for Id, Cnt in Val:
                CategoryCount[Id] = Cnt
                Sum += Cnt
            CategoryCount[Key] = Sum

        return [CategoryTree, CategoryCount, Res]


    def ToPrice(self, aDbPrice: TDbPrice) -> dict:
        ProductsInCategory = {}
        for Rec in aDbPrice.Dbl:
            CategoryId = Rec.GetField('id')
            ProductsInCategory[CategoryId] = ProductsInCategory.get(CategoryId, 0) + 1

        _CategoryTree, CategoryCount, _Res = self.SubCount(ProductsInCategory)
        return CategoryCount

    def GetIdByName(self, aNames: list[str]) -> list[int]:
        Res = []
        for Rec in self.Dbl:
            Name = Rec.GetField('name').lower()
            if (any(x in Name for x in aNames)):
                Res.append(Rec.GetField('id'))
        return Res
