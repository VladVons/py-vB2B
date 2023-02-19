# Created: 2022.10.11
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
#
from Inc.Misc.Zip import PackFiles
from Inc.Misc.FS import GetFiles
from Inc.ParserX.Common import TFileBase
from IncP.Log import Log


class TMain(TFileBase):
    async def Load(self):
        ConfFiles = self.Parent.Conf.get('files')
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
