## @file
## @brief object/stack oFORTH Virtual Machine (Python implementation)

## @defgroup core Core

import os,sys,math

## @defgroup object Object system
## @ingroup core

## @defgroup base Object
## base class
## @ingroup object

## base Object
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
    
## @defgroup prim Primitive
## Primitive types maps to machine-level (key feature: **evaluates to itself**)
## @ingroup object
       
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
    def execute(self):
        for op in self.nest: op.execute()

def test_Vector(): assert \
    ( Vector('ordered') << 1 << 2 << 3 ).nest == [1,2,3]
    
def test_Vector_execute():
    D << Vector('empty')
    assert str(D) == '\n<stack:DATA>\n\t<vector:empty>'
    EXECUTE() ; assert D.nest == []

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
    def execute(self): self.fn()

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
    def __init__(self,V,FN):
        Syntax.__init__(self, V)
        self['filename'] = FN

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

## @defgroup FVM oFORTH Virtual Machine
## @ingroup core

## @defgroup voc Vocabulary
## holds global definitios
## @ingroup FVM

## Vocabulary register
## @ingroup voc
W = Map('FORTH')

## @ingroup voc
def test_FVM_W(): assert W.head() == '<map:FORTH>'

## @defgroup stack Global data stack
## all computations in FORTH use only stack (no registers or variables)
## @ingroup FVM
## @{

## global data stack register
D = Stack('DATA')

## @test empty stack dump
def test_FVM_D(): assert '%s' % D == '\n<stack:DATA>'

## `DUP ( o - o o )` duplicate top stack element
def DUP(): D.dup()
W << DUP

## `DROP ( o1 o2 -- o1 )` drop top element
def DROP(): D.drop()
W << DROP

## `SWAP ( o1 o2 -- o2 o1 )` swap 2 top elements
def SWAP(): D.swap()
W << SWAP

## @test stack operations
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

## @}

def test_Active():
    D.flush()
    assert '%s' % Active('life').execute() == '\n<active:life>'
    assert '%s' % D == '\n<stack:DATA>'
    
def test_Object_callable():
    D.flush()
    T = Object('callable')
    T.execute() ; assert D.top() == T
    D.flush()

## @defgroup debug Debug
## words and commands can be used for debug
## @ingroup FVM
## @{

## `? ( -- )` dump stack
def q(): print D
W['?'] = Fn(q)
## `?? ( -- )` dump vocabulary, stack, end exit from system (end of script)
def qq(): print W ; print D ; BYE()
W['??'] = Fn(qq)

## @}

########################################################################## misc

## `. ( ... -- ) flush data stack
def dot(): D.flush()
W['.'] = Fn(dot)

## `BYE ( -- )` stop system
def BYE(): sys.exit(0)
W << BYE

## `NOP ( -- )` do nothing
def NOP(): pass
W << NOP

## @defgroup interp Interpreter/Compiler
## @ingroup FVM

## @defgroup lexer Lexer
## @brief regexp-based (lex) made with PLY parser generator library
## @ingroup interp
## @{

import ply.lex as lex

## lexer error callback
def t_error(t): raise SyntaxError('%s in %s'%(t.lexer.filename,t))

## ignored chars: spaces
t_ignore = ' \t\r\n'

## single line `#comment`
def t_COMMENT_hash(t):   r'\#.+'
## single line `\comment`
def t_COMMENT_slash(t):  r'\\.+'
## block `(comment)`
def t_COMMENT_parens(t): r'\(.*?\)'

## list of used token (literal) types
tokens = ['token','integer','number','hex','bin','inc']

## float in exponential form
def t_NUMBER_exp(t):
    r'[\+\-]?[0-9]+(\.[0-9]*)?[eE][\+\-]?[0-9]+'
    return Number(t.value)

## float with point
def t_NUMBER_point(t):
    r'[\+\-]?[0-9]+\.[0-9]*'
    return Number(t.value)

## machine number in hex
def t_HEX(t):
    r'0x[0-9a-fA-F]+'
    return Hex(t.value)

## binary bit string
def t_BIN(t):
    r'0b[01]+'
    return Bin(t.value)

## generic integer
def t_INTEGER(t):
    r'[\+\-]?[0-9]+'
    return Integer(t.value)

## word name token made from any non-space chars
def t_WORD(t):
    r'[a-zA-Z0-9_\?\.\[\]\:\;]+'
    return Token(t.value,t.lexer.filename)

## EOF handling must pop top lexer from .include stack
def t_eof(t):
    lexer.pop()                 # drop top lexer
    try:
        return lexer[-1].token()# must return next token as `has data` marker
    except IndexError:
        return None             # mark end data

## create system-wide lexers stack (used for .inc)
lexer = []

## `.inc <filename>` include file
def include():
    WORD() ; WN = D.pop().value
    lexer.append(lex.lex())
    try:
        F = open(WN)
        lexer[-1].filename = WN
    except IOError:
        F = open(WN+'.src')
        lexer[-1].filename = WN+'.src'
    lexer[-1].input(F.read()) 
W['.inc'] = Fn(include) ; W['.inc']['IMMED'] = T

## @}

## @defgroup interp Interpreter
## @ingroup interp
## @{

## `EXECUTE ( callable:xt -- ... )`
## run executable definition via its execution token in stack
## @ingroup interp
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

## `WORD ( -- token:wordname )`
## parse next word name from source code stream
## @ingroup lexer
def WORD():
    D << lex.token() # get object right from lexer
    if not D.top(): D.pop() ; raise EOFError
W << WORD

## @test check comments and primitive literals
test_STRING_4Interpreter = '''
# line comment
\ slash line comment
( block comment )
ThisMustBeFirst
-01 002.3 +04e-05 0xDeadBeef 0b1101 ( lot of numbers )
#this tightly inputted code can't be parsed by classical FORTH, lexer only
(And)Some\Symbols
    '''

def test_WORD():
    lexer[-1].input(test_STRING_4Interpreter)
    WORD() ; assert D.pop().head() == '<token:ThisMustBeFirst>'
    WORD() ; assert D.pop().head() == '<integer:-1>'
    WORD() ; assert D.pop().head() == '<number:2.3>'
    WORD() ; assert D.pop().head() == '<number:4e-05>'
    WORD() ; assert D.pop().head() == '<hex:0xDeadBeef>'
    WORD() ; assert D.pop().head() == '<bin:0b1101>'
    WORD() ; assert D.pop().head() == '<token:Some>'
    try: WORD() ; assert False
    except EOFError: assert True # test ok

## `FIND ( wordname -- callable:xt )`
## lookup execatable definition in vocabulary
def FIND():
    WN = D.pop()            # get word name to be found
    try: D << W[WN.value]   # push result from vocabulary
    except KeyError:
        try: D << W[WN.value.upper()]
        except KeyError:    # not found
            raise SyntaxError('%s in %s'%(WN.value,WN['filename']))

def test_FIND():
    D << String('FIND') ; FIND()
    assert D.pop().head() == '<fn:FIND>'
    D << String('NOTFOUND')
    try: FIND() ;       assert False
    except SyntaxError: assert True
W << FIND

## `INTERPRET ( -- )`
## [R]ead [E]val [P]rint [L]oop
## @param[in] SRC source file should be interpreted
def INTERPRET(SRC):
    global lexer ; lexer += [lex.lex()] # push new lexer
    lexer[-1].filename = SRC            # set input filename
    lexer[-1].input(open(SRC).read())   # feed source code
    while True:                         # interpreter loop                     
        try: WORD()
        except EOFError: break
        if D.top().type in ['token','symbol']:    # need lookup
            FIND()
            if D.top().attr.has_key('IMMED'):
                EXECUTE() ; continue
        if COMPILE: COMPILE << D.pop()  # compile from stack
        else:       EXECUTE()           # or execute in place
W << INTERPRET

## @test empty source code
def test_INTERPRET_null():
    D.flush() ; INTERPRET('')
    assert D.nest == []

## @test using @ref test_STRING_4Interpreter
def test_INTERPRET():
    def ThisMustBeFirst(): pass
    def Some(): pass
    W << ThisMustBeFirst << Some ; 
    D.flush() ; INTERPRET(test_STRING_4Interpreter)
    assert D.pop().head() == '<bin:0b1101>'
    assert D.pop().head() == '<hex:0xDeadBeef>'
    assert D.pop().head() == '<number:4e-05>'
    assert D.pop().head() == '<number:2.3>'
    assert D.pop().head() == '<integer:-1>'
    assert D.nest == []
    
## @}

## @defgroup compiler Compiler
## compile definitions <b>into Active objects</b>
## @ingroup interp
## @{

COMPILE = None

## reset COMPILEr
def COMPILE_RST(): global COMPILE ; COMPILE = None

## `[` begin block
def QL(): global COMPILE ; COMPILE = Vector('')
W['['] = Fn(QL)
## `]` end block 
def QR(): D << COMPILE ; COMPILE_RST()
W[']'] = Fn(QR) ; W[']']['IMMED'] = T   # set immediate flag

## @test empty `[ block ]`
def test_QLQR():
    COMPILE_RST();
    QL(); assert     COMPILE
    QR(); assert not COMPILE
    
## @test empty block compilation
def test_COMPILE_emptyblock():
    D.flush() ; COMPILE_RST()   # cleaup
    # check bad syntax (must have spaces)
    try: INTERPRET('[]') ; assert False
    except SyntaxError: assert True
    # check right syntax
    INTERPRET('[ ]')
    assert D.top().head() == '<vector:>'
    # check execution of empty block
    EXECUTE()
    assert D.nest == []
## @test compile empty `[]` block via INTERPRET()
def test_INTERPRET_state_transitions():
    D.flush() ; COMPILE_RST()   # cleanup
    INTERPRET('[')              # start compilation
    assert COMPILE.head() == '<vector:>'
    INTERPRET(']')              # stop
    assert COMPILE == None
## @test compile vector with number literals via INTERPRET()
def test_vector_compile():
    D.flush(); COMPILE_RST()
    INTERPRET('[ 1 2 3 ]')
    assert str(D.top()) == \
        '\n<vector:>\n\t<integer:1>\n\t<integer:2>\n\t<integer:3>'
    # don't cleanup data stack
## @test execute compiled block in test_vector_compile()
def test_vector_exec():
    test_vector_compile() ; EXECUTE()
    assert str(D) == \
    '\n<stack:DATA>\n\t<integer:1>\n\t<integer:2>\n\t<integer:3>'
    
## `: ( -- )` Start : colon definition ;
##
## We'll compile colon definitions into vectors,
## but not memory image like classical FORTH systems does.
## So ::Vector must has callable nature by defining special 
## `__call__(self)` method
def colon():
    WORD() ; WN = D.pop().value # fetch new word name
    # push just created word into vocabulary:
    # it let as to use self word name for recursion
    global COMPILE ; W[WN] = COMPILE = Vector(WN)
W[':'] = Fn(colon)

## `; ( -- )` Finish : colon definition ;
def semicolon():
    global COMPILE ; COMPILE = []
W[';'] = Fn(semicolon) ; W[';']['IMMED'] = T

## @test colon definition: ` : init ( -- ) nop bye ; `
def test_colon_def():
    D.flush()
    INTERPRET(''' : init ( -- ) nop bye ; ''')
    assert W['init'].dump() == '\n<vector:init>\n\t<fn:NOP>\n\t<fn:BYE>'
    
## `CONST ( n -- )` define named constant
def CONST():
    WORD() ; WN = D.pop()
    W[WN.value] = D.pop()
W << CONST

## `WORDS ( -- )` list vocabulary
def WORDS(): print W
W << WORDS

if __name__ == "__main__":              # VM startup
    try:
        SRC = sys.argv[1]               # feed file from command line
    except IndexError:
        SRC = 'src.src'                 # feed src.src
    INTERPRET(SRC)

## @}
