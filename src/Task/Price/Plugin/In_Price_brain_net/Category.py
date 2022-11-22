# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from ..CommonDb import TDbPrice
from ..Category import TCategoryBase


class TCategory(TCategoryBase):
    def _Filter_ById(self, aConfCategories: dict):
        def ToList(aId: list[int]) -> list[int]:
            Res = []
            if (aId):
                Items = self.SubTreeId(aId)
                for Key, Val in Items.items():
                    Res.append(Key)
                    Res += Val
            return Res

        Section = aConfCategories.get('IncludeId', [])
        IncludeId = ToList(Section)
        Section = aConfCategories.get('ExcludeId', [])
        ExcludeId = ToList(Section)

        Section = aConfCategories.get('Include', [])
        IncludeId += ToList(self.GetIdByName(Section))
        Section = aConfCategories.get('Exclude', [])
        ExcludeId += ToList(self.GetIdByName(Section))


        Res = self.Dbl.New()
        for Rec in self.Dbl:
            CategoryId = Rec.GetField('CategoryId')
            if (CategoryId in ExcludeId):
                continue

            if ((not IncludeId) or (CategoryId in IncludeId)):
                Res.RecAdd(Rec).Flush()
        self.Dbl = Res

    def Filter_FromConfig(self):
        ConfCategories = self.Parent.Conf.get('Categories')
        if (ConfCategories):
            self._Filter_ById(ConfCategories)

    def Filter_HasProduct(self, aDblPrice: TDbPrice):
        HashFinal = self.ToPrice(aDblPrice)

        Res = self.Dbl.New()
        for Rec in self.Dbl:
            Id = Rec.GetField('CategoryId')
            if (HashFinal.get(Id, 0) > 0):
                Res.RecAdd(Rec).Flush()
        self.Dbl = Res

    async def _Load(self):
        Data = await self.Parent.Api.GetCategories()
        if (Data):
            for Row in Data:
                if (Row['realcat'] == 0):
                    Rec = self.Dbl.RecAdd([Row['categoryID'], Row['parentID'], Row['name']])
                    Rec.Flush()
