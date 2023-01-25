# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.Db.DbList import TDbList


class TDbProduct(TDbList):
    def __init__(self):
        super().__init__([
            ('CategoryId', int),
            ('Id', int),
            ('Code', str),
            ('Mpn', str),
            ('Name', str),
            ('Price', float),
            ('Image', str)
        ])

class TDbPrice(TDbList):
    def __init__(self):
        super().__init__([
            ('CategoryId', int),
            ('Id', int),
            ('Code', str),
            ('Mpn', str),
            ('Name', str),
            ('Price', float),
            ('Available', int),
            ('Image', str)
        ])

class TDbCategory(TDbList):
    def __init__(self):
        super().__init__([
            ('CategoryId', int),
            ('ParentId', int),
            ('Name', str),
            ('Descr', str)
        ])

class TDbPriceJoin(TDbList):
    def __init__(self):
        super().__init__([
            ('Id', int),
            ('Code', str),
            ('Mpn', str),
            ('Name', str),
            ('Match', int),
            ('Price', float)
        ])

class TDbCompPC(TDbList):
    def __init__(self):
        super().__init__([
            ('Model', str),
            ('Case', str),
            ('CPU', str),
            ('DiskSize', int),
            ('Disk', str),
            ('RamSize', int),
            ('OS', str),
            ('VGA', str),
            ('DVD', str),
            ('Price', float)
        ])

class TDbCompPricePl(TDbList):
    def __init__(self):
        super().__init__([
            ('Model', str)
        ])
