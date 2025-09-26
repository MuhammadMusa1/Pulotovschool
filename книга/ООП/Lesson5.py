class HomeTech:
    def __init__(self, name):
        self.__name = name
        

    def work (self):
        print('Я работаю')

class Blender(HomeTech):
    def work(self):
        print('dd')
    def work(self, prod):
        print('Я смешиваю')
    


blender = Blender('Блендер')
blender.work()
