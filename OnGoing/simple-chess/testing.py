import copy

class Test:
    def __init__(self):
        self.score = 100
        self.name = "Test"


test1 = Test()

test2 = copy.deepcopy(test1)

if test1 == test2:
    print("True")
else:
    print("False")
