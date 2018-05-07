
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

