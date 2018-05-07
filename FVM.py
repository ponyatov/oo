
## @test stack operations
def test_D_dupswap():
    # check stack fluffing words in vocabulary
    assert W['DUP'].fn == DUP ; assert W['DROP'].fn == DROP
    # dup is callable and duplicates
    D.flush() << Integer(1) ; W['DUP'].execute(D)
    assert str(D) == '\n<stack:DATA>\n\t<integer:1>\n\t<integer:1>'
    # drop is callable and drops
    W['DROP'].execute(D)
    assert str(D) == '\n<stack:DATA>\n\t<integer:1>'
    # swap
    D << Integer(2) << W['SWAP'] ; W['EXECUTE'].execute(D)
    assert str(D) == '\n<stack:DATA>\n\t<integer:2>\n\t<integer:1>'

## @}

def test_Active():
    D.flush()
    assert '%s' % Active('life').execute() == '\n<active:life>'
    assert '%s' % D == '\n<stack:DATA>'

def test_Object_callable():
    D.flush()
    T = Object('callable')
    T.execute(D) ; assert D.top() == T
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

from GUI import *

## @defgroup lexer Lexer
## @brief regexp-based (lex) made with PLY parser generator library
## @ingroup interp
## @{

## lexer error callback
def t_error(t): raise SyntaxError(t)

## single line `#comment`
def t_COMMENT_hash(t):   r'\#.+'
## single line `\comment`
def t_COMMENT_slash(t):  r'\\.+'
## block `(comment)`
def t_COMMENT_parens(t): r'\(.*?\)'


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
    return Token(t.value)

## EOF handling must pop top lexer from .include stack
def t_eof(t):
    try:
        lexer.pop()                 # drop top lexer
        return lexer[-1].token()    # must return next token as `has data` marker
    except IndexError:
        return None                 # end of source marker

## system-wide lexer stack will be used for .inc
lexer = []

## `.inc <filename>` include file
def INC():
    WORD() ; WN = D.pop().value
    try: F = open(WN)
    except IOError: F = open(WN+'.src')
    global lexer
    lexer += [lex.lex()]        # new lexer
    lexer[-1].input(F.read())   # feed lexer
W['.inc'] = Fn(INC) ; W['.inc']['IMMED'] = T

## @}

## @defgroup interp Interpreter
## @ingroup interp
## @{



def test_callable_generic():
    D.flush() << Object('callable') ; W['EXECUTE'].execute(D)
    assert str(D) == '\n<stack:DATA>\n\t<object:callable>'

def test_callable_literals():
    D.flush()
    D << Integer(1234) ; W['EXECUTE'].execute(D)
    D << String('lit') ; W['EXECUTE'].execute(D)
    assert str(D) == \
        '\n<stack:DATA>\n\t<integer:1234>\n\t<string:lit>'

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
    global lexer ; lexer += [lex.lex()]
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


    WN = D.pop()            # get word name to be found
    try: D << W[WN.value]   # push result from vocabulary
    except KeyError:
        try: D << W[WN.value.upper()]
        except KeyError:    # not found
            raise SyntaxError(WN.value)

def test_FIND():
    D << String('FIND') ; FIND()
    assert D.pop().head() == '<fn:FIND>'
    D << String('NOTFOUND')
    try: FIND() ;       assert False
    except SyntaxError: assert True
W << FIND

    += [lex.lex()] # push new lexer
    lexer[-1].input(SRC)                # feed source input
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
    # it let us to use self word name for recursion
    # non-empty COMPILE points to compilation mode
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
    INTERPRET(open(SRC).read())

## @}
