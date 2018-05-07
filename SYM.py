
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

