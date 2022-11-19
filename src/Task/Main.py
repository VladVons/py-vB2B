# Created: 2021.02.26
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


import os
import sys
import time
import argparse
#
from Task import ConfTask
from Inc.PluginTask import Plugin
from Inc.UtilP.Log import TEchoConsoleEx, TEchoFileEx
from IncP import GetInfo
from IncP.Log import Log


class TTask():
    def __init__(self):
        self.Info = GetInfo()

    def InitLog(self):
        AppName = self.Info['app_name']
        FileLog = f'/var/log/{AppName}/{AppName}.log'
        if (not os.path.exists(FileLog)) or (not os.access(FileLog, os.W_OK)):
            FileLog = sys.argv[0].removesuffix('.py') + '.log'
        Log.AddEcho(TEchoFileEx(FileLog))
        print(f'Log file {FileLog}')

        Log.AddEcho(TEchoConsoleEx())

    def InitOptions(self):
        Usage = f'usage: {self.Info["app_name"]} [options] arg'
        Parser = argparse.ArgumentParser(usage = Usage)
        Parser.add_argument('-s', '--Service', help = 'run as service', action = 'store_true')
        Parser.add_argument('-i', '--Info', help = 'information', action = 'store_true')
        return Parser.parse_args()

    async def Run(self):
        self.InitLog()

        Options = self.InitOptions()
        if (Options.Info):
            List = [f'{Key:10} {Val}' for Key, Val in self.Info.items()]
            print('\n'.join(List))
            return

        Log.Print(1, 'i', f'Run() {self.Info["app_name"]}')

        TimeStart = time.time()
        if (Options.Service):
            Name = 'PluginsSrv'
        else:
            Name = 'PluginsApp'
        Plugins = ConfTask.get(Name, '')
        Plugin.LoadList(Plugins)

        try:
            await Plugin.Run()
        except KeyboardInterrupt as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
        except Exception as E:
            Log.Print(1, 'x', 'TTask.Run()', aE = E)
            raise E
        finally:
            await Plugin.StopAll()
        Log.Print(1, 'i', 'End. Time %0.2f' % (time.time() - TimeStart))
