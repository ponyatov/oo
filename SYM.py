
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

