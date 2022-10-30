# Created: 2022.04.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TWebSrv


def Main(aConf) -> tuple:
    Obj = TWebSrv(aConf)
    return (Obj, Obj.Run())
