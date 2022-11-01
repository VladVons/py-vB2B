# Created: 2022.04.14
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details

from Inc.UtilP.WebSrv.WebSrv import TWebSrvConf
from .Main import TWebSrv


def Main(aConf) -> tuple:
    SrvConf = aConf.get('SrvConf', {})
    SrvConf = TWebSrvConf(**SrvConf)
    Obj = TWebSrv(SrvConf, aConf)
    return (Obj, Obj.RunApp())
