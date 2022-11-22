# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from IncP.Download import TRecSes, TDownload
from IncP.Log import Log


class TImages():
    def __init__(self, aParent, aDir: str = None):
        self.Parent = aParent
        self.Suffix = '_big.jpg'

        if (aDir):
            self.Dir = aDir
        else:
            self.Dir = '%s/%s/Image' % (aParent.Parent.Conf.get('DirData'), self.Parent.Api.GetModName(__file__))

    def GetDirPath(self, aProductCode: str) -> str:
        return f'{self.Dir}/{aProductCode[-2]}/{aProductCode[-1]}'

    def GetFilePath(self, aProductCode: str) -> str:
        return '%s/%s.jpg' % (self.GetDirPath(aProductCode), aProductCode)

    def _GetUrls(self, aProductCodes: list[str]) -> list[str]:
        return [self.Parent.Api.GetUrlImage(x) for x in aProductCodes]

    async def _OnSend(self, aRecSes: TRecSes, aRes: dict):
        if (aRes['Status'] == 200):
            Code = os.path.basename(aRecSes.Url).replace(self.Suffix, '')
            File = self.GetFilePath(Code)
            if (not os.path.exists(File)):
                if (__debug__):
                    Log.Print(1, 'i', 'Task: %4s, Url: %s -> %s' % (aRecSes.TaskNo, aRecSes.Url, File))
                Dir = self.GetDirPath(Code)
                os.makedirs(Dir, exist_ok=True)
                with open(File, 'wb') as F:
                    F.write(aRes['Data'])
        else:
            Log.Print(1, 'e', 'Err %s' % (aRecSes.Url))

    async def LoadUrls(self, aUrls: list[str], aTasks: int = 3):
        Download = TDownload(self._OnSend)
        RecSes = [TRecSes(x) for x in aUrls]
        await Download.SendMany(RecSes, aTasks)

    async def LoadCodes(self, aProductCodes: list[str], aTasks: int = 3):
        Download = TDownload(self._OnSend)
        RecSes = [TRecSes(x) for x in self._GetUrls(aProductCodes)]
        await Download.SendMany(RecSes, aTasks)
