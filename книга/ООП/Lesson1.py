class Processor:
    name = ''
    frequency = 0
    numcore = 0
    def sum (a, b):
        return a + b
    def showname():
        print(Processor.name)


procIntel = Processor

procIntel.name = 'Intel Core i3'

print(procIntel.sum(9, 8))

procIntel.showname()
