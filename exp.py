class Test():
    def one(self, num):
        print("Num: " + str(num))
    def two(self, num):
        one(num + 1)

var = Test()

var.two(3)
