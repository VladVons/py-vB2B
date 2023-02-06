import re
from collections import defaultdict
from Inc.Db.DbList import TDbListSafe

def Test_1():
    eMail = 'this is my eMail vlad_vons1@gmaill.com I love it. Also davydvons@gmail.com is good'
    aMails = re.findall(r'([\w.]+\@[\w.]+)', eMail)
    if (aMails):
       for x in aMails:
           print(x)


def Test_2():
    MyList = [
        ['user1', 0, 1, 0],
        ['user2', 2, 2, 2],
        ['user3', 2, 2, 0],
        ['user3', 1, 1, 2],
        ['user1', 1, 0, 1],
    ]

    merged = defaultdict(lambda: [0, 0, 0])
    for user, *values in MyList:
        merged[user] = [sum(i) for i in zip(values, merged[user])]
    print(merged)

def Test_3():
    MyList = [
        ['user1', 0, 1, 0],
        ['user2', 2, 2, 2],
        ['user3', 2, 2, 0],
        ['user3', 1, 1, 2],
        ['user1', 1, 0, 1],
    ]

    Dict = {}
    for elem in MyList:
        if elem[0] not in Dict:
            Dict[elem[0]] = []
        Dict[elem[0]].append(elem[1:])

    for key in Dict:
        Dict[key] = [sum(i) for i in zip(*Dict[key])]
    print(Dict)

#Test_3()
