class Person:
    def __init__(self, name, specs):
        self.name = name
        self.specs = specs

    def say_hi(self):
        print('Hello, my name is', self.name)

p1 = Person(name='Shivanee', specs=True)	# create object 1
p1.say_hi()                                 # object 1 uses method say_hi

p2 = Person(name='Rishik',  specs=True)		# create object 2
p2.say_hi()                                 # object 2 uses method say_hi

p3 = Person(name='Amulya',  specs=False) 	# create object 3
p3.say_hi()                                 # object 3 uses method say_hi
