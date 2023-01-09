import json


def Test1():
    File = 'fo_last_web_export_22_12_24_12_28.json'
    with open(File) as F:
        Data = json.load(F)
    print(Data)

Test1()


