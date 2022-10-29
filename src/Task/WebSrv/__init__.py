from Task import ConfTask
from .Main import TWebSrv


def Main(aConf) -> tuple:
    Obj = TWebSrv(aConf)
    return (Obj, Obj.Run())
