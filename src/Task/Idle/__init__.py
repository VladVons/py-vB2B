# Created: 2020.02.10
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


from .Main import TIdle


def Main(aConf) -> tuple:
    Obj = TIdle()
    return (Obj, Obj.Run(aConf.get('sleep', 1)))
