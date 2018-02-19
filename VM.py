################################################## object/stack virtual machine

################################################################### base Object

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V
    def __repr__(self):
        return '<%s:%s>'%(self.type,self.value)
    
def test_Object(): # run tests using py.test -v VM.py
    assert '%s' % Object('test') == '<object:test>'
    
#################################################################### Primitives
       
class Primitive(Object): pass

def test_Primiteve(): assert \
    str( Primitive('atom') ) == '<primitive:atom>'
    
########################################################## Symbol ( generic ID)

class Symbol(Primitive): pass

def test_Symbol(): assert \
    '%s'%Symbol('Pi') == '<symbol:Pi>'
