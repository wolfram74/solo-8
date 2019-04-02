def flashy(flash_to_be):
    def routified(self):
        self.count +=1
        flash_to_be(self)
    return routified

class Tally():
    def __init__(self):
        self.count=0

    def shout0(self):
        print(self.count)

    @flashy
    def shout1(self):
        print(self.count)

t = Tally()

t.shout0()
t.shout1()
t.shout1()
t.shout0()
