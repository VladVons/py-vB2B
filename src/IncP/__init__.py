# Created: 2022.04.30
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details


__version__ = '1.0.11'
__date__ =  '2022.04.07'


def GetAppVer() -> dict:
    return {
        'app_name': 'vCrawler',
        'app_ver' : __version__,
        'app_date': __date__,
        'author':  'Vladimir Vons, VladVons@gmail.com',
        'home': 'http://oster.com.ua',
    }
