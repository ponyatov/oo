# object/stack virtual machine

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
    def __repr__(self):
        return '<%s:%s>'%(self.type,self.value)
       
class Primitive(Object): pass

print Object('test')
