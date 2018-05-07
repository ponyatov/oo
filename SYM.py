    def __lshift__(self,object): return self.push(object)
    def dup(self): self.nest.append(self.top()) ; return self
    def drop(self): del self.nest[-1] ; return self
    def swap(self):
        B = self.pop() ; A = self.pop()
        self.push(B) ; self.push(A)
        return self
    ## execute object in context of D stack
    ## @pram[in] D context data stack
    def execute(self,D): D << self ; return self
    
######################################################### Symbol ( generic ID )

    
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

## @defgroup cont Container
## data containers
## @ingroup object
## @{

class Container(Object): pass

def test_Container():
    C = Container('with data')
    assert C.head() == '<container:with data>'

## LIFO Stack
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

## unordered key:value storage
class Map(Container):
    def __lshift__(self,F): # operator<<
        try: self[F.value] = F # push object
        except AttributeError: # fallback for
            self[F.__name__] = Fn(F) # VM command
        return self # return modified Map

def test_Map(): assert Map('map').attr == {}

def test_Map_LL(): assert '%s' % \
    ( Map('LL') << test_Map_LL ) == \
        '\n<map:LL>\n\ttest_Map_LL = <fn:test_Map_LL>'
        
def test_Map_GetSet():
    M = Map('get/set') ; M['X'] = 'Y'
    assert M.attr == {'X':'Y'}  # check set
    assert M['X'] == 'Y'        # check get

## ordered vector
class Vector(Container):
    def execute(self,D):
        for op in self.nest: op.execute(D)

def test_Vector(): assert \
    ( Vector('ordered') << 1 << 2 << 3 ).nest == [1,2,3]
    
## FIFO queue
class Queue(Vector):
    def pop(self): return self.nest[0]

def test_Queue(): assert Queue('queue').nest == []

def test_Queue_pushpop():
    Q = Queue('queue') << 1 << 2 << 3
    assert Q.pop() == 1

## @}

## @defgroup active Active
## items has only executional semantics
## @ingroup object
## @{

class Active(Object):
    def execute(self): return self
    
## function compiled into VM
class Fn(Active):
    def __init__(self,F):
        Active.__init__(self, F.__name__)   # get name
        self.fn = F                 # special function pointer
    def execute(self,D): self.fn()

def test_Fn(): assert Fn(test_Fn).head() == '<fn:test_Fn>'

## @}

## @defgroup special Specials
## @ingroup object

## @defgroup bool Boolean
## bool values
## @ingroup special

class Bool(Object): pass
class true(Bool): pass
class false(Bool): pass

T = true('T') ; F = false('F')

def test_Bool():
    assert T.head() == '<true:T>'
    assert F.head() == '<false:F>'
    
## @defgroup err Error
## exception and error processing
## @ingroup special

## @defgroup grammar Grammar
## elements specially for syntax parsing
## @ingroup object
## @{

## Syntax elements
class Syntax(Object):
    pass

## lexeme (token) = word name
class Token(Syntax):
    def __init__(self,V):
        Syntax.__init__(self, V)

## Language grammar
class Grammar(Syntax):
    pass

## @test token
def test_token():
    assert Token('wordname').head() == '<token:wordname>'

## sungle BNF grammar rule
class BNF(Grammar):
    pass

## @}

