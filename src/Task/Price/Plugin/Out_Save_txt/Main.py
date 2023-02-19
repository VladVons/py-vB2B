# Created: 2022.10.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import json
#
from Inc.Util.Obj import GetClassPath
from Inc.ParserX.Common import TFileBase
from IncP.Log import Log


class TMain(TFileBase):
    async def Save(self, aParam: dict):
        ConfFile = self.Parent.GetFile()
        Dir = ConfFile.replace('.txt', '')
        os.makedirs(Dir, exist_ok=True)

        for PluginKey, PluginVal in aParam.items():
            for ParamKey, ParamVal in PluginVal.items():
                Data = ''
                ClassPath = GetClassPath(ParamVal)
                if ('/TDbList' in ClassPath):
                    ParamVal.OptReprLen = 40
                    Data = str(ParamVal)
                elif (type(ParamVal) in [dict, list]):
                    Data = json.dumps(ParamVal, indent=2)

                if (Data):
                    File = f'{Dir}/{PluginKey}_{ParamKey}.txt'
                    Log.Print(1, 'i', 'Save %s' % (File))
                    with open(File, 'w', encoding='utf-8') as F:
                        F.write(Data)
                await self.Sleep.Update()
