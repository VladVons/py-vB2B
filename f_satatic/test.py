import sys

def Test3():
    w1 = 1/0
    print('hello3')

def Test2():
    e1 = 'hello'
    print('hello2')
    Test3()

a = 1
print(sys.version)
print(sys.version)
b = 2
Test2()
print(sys.version)
print(sys.version)

