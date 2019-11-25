class C:
    def __init__(self):
        print("C")


class B1(C):
    def b1_fun(self):
        print("B1")


class B2(C):
    def b2_fun(self):
        print("B2")


# A
class A(B1, B2):
    def a_fun(self):
        print("A")


a = A()
a.b1_fun()
a.b2_fun()
