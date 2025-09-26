class Pet:
##    name = ''
##    animal = ''
##    breed = ''
##    age = 0
##    color = ''
##    size = ''

    def __init__(self, name, animal, breed, age, color, size):
        self.name = name
        self.animal = animal
        self.breed = breed
        self.age = age
        self.color = color
        self.size = size
    



##catTom = Pet
##catTom.name = 'Murzic'
##catTom.animal = 'cat'
##catTom.breed = 'British'
##catTom.age = 1
##catTom.color = 'grey'
##catTom.size = 'middle'
##
##dogRex = Pet
##dogRex.name = 'Rex'
##dogRex.animal = 'dog'
##dogRex.breed = 'Labrodor'
##dogRex.age = 3
##dogRex.color = 'black'
##dogRex.size = 'big'
##
##catBarsik = Pet
##catBarsik.name = 'Barsik'
##catBarsik.animal = 'cat'
##catBarsik.breed = 'Scotish'
##catBarsik.age = 0.5
##catBarsik.color = 'white'
##catBarsik.size = 'small'


catTom = Pet('Murzic', 'cat', 'British', 1, 'grey', 'middle')
print(catTom.name)
