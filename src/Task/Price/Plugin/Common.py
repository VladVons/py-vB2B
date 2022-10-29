# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.DB.DbList import TDbList
from Inc.Util.Obj import DeepGet, GetClassPath
from Inc.UtilP.Time import TASleep
from IncP.Download import TDownload
from IncP.Log import Log
from .CommonDb import TDbPrice, TDbCategory


class TFileBase():
    def __init__(self, aParent):
        self.Parent = aParent
        self.Sleep = TASleep(self.Parent.Conf.get('SleepLoop', 0), 500)

    def GetFile(self) -> str:
        TopClass = GetClassPath(self).split('/')[-1]
        Res = self.Parent.Parent.Conf.GetKey('DirData') + '/' + self.Parent.Name + '/' + TopClass + '.dat'
        return Res


class TFileDbl(TFileBase):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Dbl = TDbList()

    async def _Load(self):
        raise NotImplementedError()

    async def Load(self):
        File = self.GetFile()
        Log.Print(1, 'i', f'Load {File}')
        if (os.path.exists(File)):
            self.Dbl.Load(File)
        else:
            ClassPath = GetClassPath(self)
            if (any(x in ClassPath for x in ['_xls', '_csv', '_ods'])):
                SrcFile = self.Parent.GetFile()
                if (not os.path.exists(SrcFile)):
                    Log.Print(1, 'e', f'File not found {SrcFile}. Skip')
                    return

            await self._Load()
            if (self.Parent.Conf.get('SaveCache')):
                os.makedirs(os.path.dirname(File), exist_ok=True)
                self.Dbl.Save(File)
        Log.Print(1, 'i', f'Done {File}. Records {self.Dbl.GetSize()}')


class TPriceBase(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Dbl = TDbPrice()
        self.DelMpn = ''.maketrans('', '', ' -/_.&@()#+')

    async def _Load(self):
        raise NotImplementedError()

    def GetMpn(self, aVal) -> str:
        return aVal.translate(self.DelMpn).upper().strip()


class TCategoryBase(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Dbl = TDbCategory()

    async def _Load(self):
        raise NotImplementedError()

    def _GetTree(self) -> dict:
        Res = {}
        for Rec in self.Dbl:
            ParentId = Rec.GetField('ParentId')
            Data = Res.get(ParentId, [])
            Data.append([Rec.GetField('CategoryId'), 0])
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
        Root = [[Id, 0]for Id, _Cnt in CategoryTree[1]]
        TreeDepth = ToChildRecurs(Root, 0)

        Res = []
        self.Dbl.SearchAdd('CategoryId')
        for Id, Depth in TreeDepth:
            RecNo = self.Dbl.Search('CategoryId', Id)
            Text = '  ' * Depth + '%s, %s' % (Id, self.Dbl.RecGo(RecNo).GetField('Name'))
            Res.append(Text)
        return '\n'.join(Res)

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

        ConfMargin = self.Parent.Conf.get('Margin', {})
        if (ConfMargin):
            Margins = ConfMargin.get('Id', {})
            CategoryTree = self._GetTree()
            Root = [[Id, 0] for Id, _Cnt in CategoryTree[1]]
            Res = ToChildRecurs(Root, ConfMargin.get('Default', 1.0))
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
            CategoryId = Rec.GetField('CategoryId')
            ProductsInCategory[CategoryId] = ProductsInCategory.get(CategoryId, 0) + 1

        _CategoryTree, CategoryCount, _Res = self.SubCount(ProductsInCategory)
        return CategoryCount

    def GetIdByName(self, aNames: list[str]) -> list[int]:
        Res = []
        for Rec in self.Dbl:
            Name = Rec.GetField('Name').lower()
            if (any(x in Name for x in aNames)):
                Res.append(Rec.GetField('CategoryId'))
        return Res

class TApiBase():
    def __init__(self):
        self.Download = TDownload()

    @staticmethod
    def GetModName(aPath: str) -> str:
        return os.path.basename(os.path.dirname(aPath))


class TPluginBase():
    def __init__(self):
        # assigned from TPlugins class creator
        self.Parent = None
        self.Depends = None
        self.Name = None
        self.Conf = None
        self.Depth = 0

    def GetParam(self, aName: str, aDef = None) -> object:
        return DeepGet(self.Parent.Data, aName, aDef)

    def GetParamDepends(self, aName: str = '') -> dict:
        Res = {}
        for Depend in self.Depends:
            Path = f'{Depend}.{aName}' if (aName) else Depend
            Param = self.GetParam(Path)
            if (Param):
                Res[Depend] = Param
        return Res

    def GetParamDependsIdx(self, aName: str, aIdx: int = 0) -> object:
        Param = self.GetParamDepends(aName)
        Param = list(Param.values())
        if (aIdx < len(Param)):
            return Param[aIdx]
        return None

    def GetFile(self) -> str:
        Res = self.Conf.GetKey('File')
        if (not Res):
            Split = self.Name.split('_')
            File = '/'.join(Split[:-1]) + '.' + Split[-1]
            Res = self.Parent.Conf.GetKey('DirData') + '/' + File
        return Res


def ToFloat(aVal: str) -> float:
    if (not aVal):
        aVal = 0
    elif (isinstance(aVal, str)):
        aVal = aVal.replace(',', '.').replace(' ', '')

    try:
        aVal = float(aVal)
    except ValueError:
        aVal = 0.0
    return aVal
