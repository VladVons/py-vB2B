# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Db.DbList import TDbList
from Inc.Util.Obj import DeepGet, GetClassPath
from Inc.UtilP.Time import TASleep
from IncP.Download import TDownload
from IncP.Log import Log
from .CommonDb import TDbPrice


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
                self.Dbl.Save(File, True)
        Log.Print(1, 'i', f'Done {File}. Records {self.Dbl.GetSize()}')


class TPriceBase(TFileDbl):
    def __init__(self, aParent):
        super().__init__(aParent)
        self.Dbl = TDbPrice()
        self.DelMpn = ''.maketrans('', '', ' -/_.&@()#+"')

    async def _Load(self):
        raise NotImplementedError()

    def GetMpn(self, aVal) -> str:
        return aVal.translate(self.DelMpn).upper().strip()



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
