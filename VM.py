################################################## object/stack virtual machine

import os,sys,math

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
    
######################################################### Symbol ( generic ID )

class Symbol(Primitive): pass

def test_Symbol(): assert \
    '%s'%Symbol('Pi') == '<symbol:Pi>'
    
######################################################################## String

class String(Primitive): pass

def test_String(): assert '%s' % \
    String('hello') == '<string:hello>'

####################################################################### Numbers

######################################################################### Float

class Number(Primitive):
    def __init__(self,V):
        Primitive.__init__(self, V)
        self.value = float(V) # use python float

def test_Number_point(): assert \
    type(Number('-0123.45').value) == type(-123.45) and \
    abs( Number('-0123.45').value - (-123.45) ) < 1e-6

def test_Number_exp(): assert \
    type(Number('-01.23e+45').value) == type(-123.45) and \
    abs( Number('-01.23E+45').value - (-1.23e45) ) < 1e-6

####################################################################### Integer

class Integer(Number):
    def __init__(self,V):
        Number.__init__(self, V)
        self.value = int(V) # use python integer

def test_Integer(): assert \
    type(Integer('-012345').value) == type(-12345) and \
    Integer('-012345').value == -12345
