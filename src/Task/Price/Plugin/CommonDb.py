# Created: 2022.10.04
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from Inc.DB.DbList import TDbList


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
