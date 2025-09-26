class Sport:
    def __init__ (self, name):
        self.name = name

    def show(self):
        print(self.name)

class Football(Sport):
    def __init__(self, name, durT):
        #Sport.__init__(self, name)
        self.name = name
        self.durationTime = durT
    
class Boxing(Sport):
    def __init__(self, name, wC):
        Sport.__init__(self, name)
        self.weightCategory = wC

    


Fb = Football('Football', 45)
Bx = Boxing('Boxing', 'superheavy')

Bx.show()
Fb.show()
print(Bx.weightCategory)

