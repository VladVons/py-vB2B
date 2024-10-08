# Created: 2022.11.17
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import re
import aiomysql
#
from Inc.Sql.ADb import TADb, TDbExecPool
from Inc.ParserX.Common import TFileBase
from ..In_Price_brain_net import TIn_Price_brain_net
from ..In_Price_brain_net.Images import TImages


class TDbApp(TADb):
    async def Connect(self):
        await self.Close()
        self.Pool = await aiomysql.create_pool(**self.Auth)


class TSqlImage():
    def __init__(self, aDir: str):
        self.Missed = []
        self.Images = TImages(TIn_Price_brain_net(), aDir)
        self.RegEx = re.compile(r'\((.*?)\)')

    async def Save(self):
        await self.Images.LoadCodes(self.Missed)

    def ParseProduct(self, aLine: str):
        if (not aLine.startswith('INSERT IGNORE INTO oc_product ')):
            return

        Find = self.RegEx.findall(aLine)
        if (Find):
            Fields = [x.strip() for x in Find[0].split(',')]
            FieldNo = Fields.index('sku')
            for Row in Find[1:]:
                Values = Row.split(',')
                if (len(Values) >= FieldNo):
                    Code = Values[FieldNo].strip('" ')
                    Path = self.Images.GetFilePath(Code)
                    if (not os.path.exists(Path)):
                        self.Missed.append(Code)


class TMain(TFileBase):
    async def Run(self):
        Auth = self.Parent.Conf.GetKey('auth')
        DbApp = TDbApp(Auth)
        await DbApp.Connect()

        FileIn = self.Parent.Conf.GetKey('file_in')
        with open(FileIn, 'r', encoding='utf-8') as File:
            Lines = File.readlines()

        SqlImage = TSqlImage(self.Parent.Conf.GetKey('dir_image'))
        for Line in Lines:
            Line = Line.strip()
            if (Line) and (not Line.startswith('#')):
                await TDbExecPool(DbApp.Pool).Exec(Line)
                SqlImage.ParseProduct(Line)

        if (self.Parent.Conf.GetKey('load_image', True)):
            await SqlImage.Save()
