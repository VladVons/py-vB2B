# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.UtilP.Zip import PackFiles
from Inc.UtilP.FS import GetFiles
from IncP.Log import Log
from ..Common import TFileBase


class TMain(TFileBase):
    async def Load(self):
        ConfFiles = self.Parent.Conf.get('Files')
        Files = []
        for File in ConfFiles:
            if (os.path.exists(File)):
                if (os.path.isdir(File)):
                    Files += list(GetFiles(File))
                else:
                    Files.append(File)
            else:
                Log.Print(1, 'e', f'File not found {File}')

        ConfFile = self.Parent.GetFile()
        PackFiles(ConfFile, Files, False)
