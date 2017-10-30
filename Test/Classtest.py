class People(object):
    """docstring for People."""

    def __init__(self, name):
        self.name = name

    def print_name(self):
        print('My name is: %s' % (self.name))


class Student(People):
    def __init__(self, name, score):
        self.name = name
        self.__score = score

    def print_score(self):
        print('My score is: %s' % (self.__score))


bart = Student('zhangsan', 88)
bart.name = "zhangsan"
bart.__score = 77
bart.print_name()
bart.print_score()
