################################################## object/stack virtual machine

import os,sys,math

################################################################### base Object

class Object:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.value = V  # single value for instance
        self.flush()
    # this convert function will be used by 'print'
    def __repr__(self): return self.dump()
    # return only <T:V> header string
    def head(self):
        return '<%s:%s>'%(self.type,self.value)
    # padding with N tabs for tree-like output
    def pad(self,N): return '\t'*N
    # recursive tree-like dump of any object
    def dump(self,depth=0,prefix=''):
        # tabbed head()er with optional prefix
        S = '\n'+self.pad(depth) + prefix + self.head()
        # attr{}ibutes subtree
        for i in self.attr:
            S += self.attr[i].dump(depth+1,'%s = ' % i)
        # nest[]ed elements subtree
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    def __setitem__(self,key,value): self.attr[key] = value ; return self
    def __getitem__(self,key): return self.attr[key]
    def flush(self):
        # store attributes in form of key/value
        self.attr = {}    # clean
        # store nested elements (ordered) / stack
        self.nest = []    # clean
        # return object itself for sequential operations
        return self
    def push(self,object):
        self.nest.append(object) ; return self
    def __lshift__(self,object): return self.push(object)
    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]
    def dup(self): self.nest.append(self.top()) ; return self
    def drop(self): del self.nest[-1] ; return self
    def swap(self):
        B = self.pop() ; A = self.pop()
        self.push(B) ; self.push(A)
        return self
    def execute(self): D << self ; return self
    
def test_Object(): # run tests using py.test -v VM.py
    assert Object('test').head() == '<object:test>'
    
def test_Object_attr(): assert \
    Object('attr{} test').attr == {}
def test_Object_nest(): assert \
    Object('nest[] test').nest == []
    
#################################################################### Primitives
       
class Primitive(Object): pass

def test_Primiteve(): assert \
    str( Primitive('atom') ) == '\n<primitive:atom>'
    
######################################################### Symbol ( generic ID )

class Symbol(Primitive): pass

def test_Symbol(): assert \
    Symbol('Pi').head() == '<symbol:Pi>'
    
######################################################################## String

class String(Primitive): pass

def test_String(): assert '%s' % \
    String('hello') == '\n<string:hello>'

####################################################################### Numbers

######################################################################### Float

class Number(Primitive):
    def __init__(self,V):
        Primitive.__init__(self, V)
        self.value = float(V)           # use python float

def test_Number_point(): assert \
    type(Number('-0123.45').value) == type(-123.45) and \
    abs( Number('-0123.45').value - (-123.45) ) < 1e-6

def test_Number_exp(): assert \
    type(Number('-01.23e+45').value) == type(-123.45) and \
    abs( Number('-01.23E+45').value - (-1.23e45) ) < 1e-6

####################################################################### Integer

class Integer(Number):
    def __init__(self,V,B=10):
        Number.__init__(self, '0')
        self.value = int(V)             # use python integer

def test_Integer(): assert \
    type(Integer('-012345').value) == type(-12345) and \
    Integer('-012345').value == -12345
    
class Hex(Integer):
    def __init__(self,V): Integer.__init__(self, '0') ; self.value = V
class Bin(Integer):
    def __init__(self,V): Integer.__init__(self, '0') ; self.value = V

#################################################################### Containers

class Container(Object): pass

def test_Container(): assert \
    Container('with data').head() == '<container:with data>'

######################################################################### Stack

class Stack(Container): pass

def test_Stack(): assert Stack('stack').nest == []

def test_Stack_flush(): assert \
    Stack('flush test').flush().nest == []

def test_Stack_push(): assert \
    ( Stack('push test') << 1 << 2 << 3 ).nest == [1,2,3]

def test_Stack_pop():
    S = Stack('pop test') << 1 << 2
    assert S.pop() == 2
    assert S.nest == [1]

def test_Stack_top(): assert \
    ( Stack('top test') << 1 << 2 ).top() == 2

def test_Stack_dup(): assert \
    ( Stack('dup test') << 1 ).dup().nest == [1,1]

def test_Stack_swap(): assert \
    ( Stack('swap test') << 1 << 2 ).swap().nest == [2,1]

########################################################################### Map

class Map(Container):
    def __lshift__(self,F): # operator<<
        try: self[F.value] = F # push object
        except AttributeError: # fallback for
            self[F.__name__] = VM(F) # VM command
        return self # return modified Map

def test_Map(): assert Map('map').attr == {}

def test_Map_LL(): assert '%s' % \
    ( Map('LL') << test_Map_LL ) == \
        '\n<map:LL>\n\ttest_Map_LL = <vm:test_Map_LL>'
        
def test_Map_GetSet():
    M = Map('get/set') ; M['X'] = 'Y'
    assert M.attr == {'X':'Y'}  # check set
    assert M['X'] == 'Y'        # check get

######################################################################### Queue

class Queue(Container):
    def pop(self): return self.nest[0]

def test_Queue(): assert Queue('queue').nest == []

def test_Queue_pushpop():
    Q = Queue('queue') << 1 << 2 << 3
    assert Q.pop() == 1

######################################################################## Active

class Active(Object):
    def execute(self): return self

############################################################################ VM

class VM(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)   # get name
        self.fn = F                 # special function pointer
    def execute(self): self.fn()

def test_VM(): assert VM(test_VM).head() == '<vm:test_VM>'

######################################################### FORTH Virtual Machine

###################################################### global context registers

#################################################################### Vocabulary

W = Map('FORTH')    # global vocabulary register

def test_FVM_W(): assert W.head() == '<map:FORTH>'

#################################################################### data stack

D = Stack('DATA')   # global data stack register

def test_FVM_D(): assert '%s' % D == '\n<stack:DATA>'

def DUP(): D.dup()
W << DUP

def DROP(): D.drop()
W << DROP

def SWAP(): D.swap()
W << SWAP

def test_D_dupswap():
    # check stack fluffing words in vocabulary
    assert W['DUP'].fn == DUP ; assert W['DROP'].fn == DROP
    # dup is callable and duplicates
    D.flush() << Integer(1) ; W['DUP'].execute()
    assert str(D) == '\n<stack:DATA>\n\t<integer:1>\n\t<integer:1>'
    # drop is callable and drops
    W['DROP'].execute()
    assert str(D) == '\n<stack:DATA>\n\t<integer:1>'
    # swap
    D << Integer(2) << W['SWAP'] ; W['EXECUTE'].execute()
    assert str(D) == '\n<stack:DATA>\n\t<integer:2>\n\t<integer:1>'

###################################################################### callable

def EXECUTE(): D.pop().execute()
W << EXECUTE

def test_callable_generic():
    D.flush() << Object('callable') ; W['EXECUTE'].execute()
    assert str(D) == '\n<stack:DATA>\n\t<object:callable>'

def test_callable_literals():
    D.flush()
    D << Integer(1234) ; W['EXECUTE'].execute()
    D << String('lit') ; W['EXECUTE'].execute()
    assert str(D) == \
        '\n<stack:DATA>\n\t<integer:1234>\n\t<string:lit>'

def test_Active():
    D.flush()
    assert '%s' % Active('life').execute() == '\n<active:life>'
    assert '%s' % D == '\n<stack:DATA>'
    
def test_Object_callable():
    D.flush()
    T = Object('callable')
    T.execute() ; assert D.top() == T

######################################################################### lexer

import ply.lex as lex

# lexer error callback
def t_error(t): raise SyntaxError(t)

# ignored chars: spaces
t_ignore = ' \t\r\n'

def t_COMMENT_hash(t):   r'\#.+'                # single line #comment
def t_COMMENT_slash(t):  r'\\.+'                # single line \comment
def t_COMMENT_parens(t): r'\(.*?\)'             # block (comment)

# list of used token (literal) types
tokens = ['symbol','integer','number','hex','bin']

def t_NUMBER_exp(t):                            # float in exponential form
    r'[\+\-]?[0-9]+(\.[0-9]*)?[eE][\+\-]?[0-9]+'
    return Number(t.value)

def t_NUMBER_point(t):                          # float with point
    r'[\+\-]?[0-9]+\.[0-9]*'
    return Number(t.value)

def t_HEX(t):                                   # machine number in hex
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)

def t_BIN(t):                                   # binary bit string
    r'0b[01]+'
    return Bin(t.value)

def t_INTEGER(t):                               # generic integer
    r'[\+\-]?[0-9]+'
    return Integer(t.value)

def t_WORD(t):
    r'[a-zA-Z0-9_\?\.]+'
    return Symbol(t.value)

def BYE(): sys.exit(0)          # stop system
W << BYE

lexer = lex.lex()               # create lexer
lexer.input(sys.stdin.read())   # feed stdin as source input stream
def WORD():
    token = lex.token()
    if not token: BYE()
    D << token
W << WORD

def INTERPRET():
    while True:                     # interpreter loop
        WORD() ; print D
W << INTERPRET
INTERPRET()
