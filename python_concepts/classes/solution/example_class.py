

class Number_Pair:
    def __init__(self,a,b):
        self.a = a # classes have attributes -we are making a and b attributes
        self.b = b
        self.order = None
        self.added = None
        self.subtracted = None
        self.multiplied = None
        self.add() # we can call some class functions from within the init function
        return None

    def update_ab(self,a,b):
        self.a = a
        self.b = b
        # update values if they have been calculated
        if self.added != None:
            self.add()
        if self.subtracted != None:
            self.subtract(order=self.order)

    def add(self):
        self.added = self.a + self.b

    # setting the order variable equal to 'a-b' makes 'a-b' the default value
    def subtract(self,order='a-b'):
        if order == 'a-b':
            self.subtracted = self.a - self.b
            self.order = order
        elif order == 'b-a':
            self.subtracted = self.b - self.a
            self.order = order
        else:
            raise ValueError('Invalid operation %s' % order)
        return self.subtracted

    def multiply(self,a,b):
        if a != self.a or b != self.b:
            self.update(a,b)
        self.multiplied = a * b
        return self.multiplied


