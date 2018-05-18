## @file
## @brief `oFORTH/py` object metasystem /Python implementation/

import os,sys,time

# wxPython
import wx,wx.stc

# we'll use threaded VM/GUI/HTTP to avoid lockups and system falls
import threading
import Queue as pyQueue

## @defgroup sym Symbolic object system
## was first conceived for knowledge representation and symbolic computation

## @defgroup object Universal base object
## @brief can hold single data element or work as data container
## @ingroup sym
## @{

## unversal base object can hold single data element or work as data container
class Object:
    ## construct symbol
    ## @param[in] V single primitive object value
    def __init__(self,V):
        ## type/class tag
        self.tag = self.__class__.__name__.lower()
        ## single object value
        self.val = V
        ## `attr{}`ibutes
        ## @ingroup attr
        self.attr = {}
        ## store `nest[]`ed elements (ordered) / stack
        self.nest = []
        ## create nested/stack
        self.flush()
        ## immediate flag
        self.immed = False
    ## clear stack
    def flush(self):
        ## @ingroup nest
        self.nest = [] ; return self
        
    ## @defgroup dump Dump
    ## @brief dump object in human-readable form for debugging
    ## @ingroup object
    ## @{
    
    ## `print sym` in readable form
    def __repr__(self): return self.dump()
    
    ## dump object in full tree form
    ## @param[in] depth tree depth for recursive dump
    ## @param[in] prefix optional prefix before <b>dump</b> header
    def dump(self,depth=0,prefix=''):
        ## list of dumped objects, block infty recursion
        global dumped
        if depth==0: dumped = []
        S = '\n'+self.pad(depth)+self.head(prefix)      # dump header
        if self in dumped: return S                     # break recursion
        else: dumped.append(self) 
        for i in self.attr:
            S += '\n' + self.pad(depth+1) + \
                self.attr[i].dump(depth+1,prefix='%s = '%i)
        return S + self.dumpnest(depth)
    ## dump `nest[]`ed only
    def dumpnest(self,depth=0):
        S = ''
        for j in self.nest: S += j.dump(depth+1)
        return S
    ## dump object in short header-only `<T:V>` form
    ## @param[in] prefix optional string will be put before `<T:V>`
    def head(self,prefix=''): return '%s<%s:%s>'%(prefix,self.tag,self.val)
    ## pad with N tabs in tree output
    ## @param[in] N left padding
    def pad(self,N): return '\t'*N
    ## @}
    
    ## @defgroup attr Attributes = object slots
    ## @ingroup object
    ## <b>any object</b> can be used as associative array,
    ## or can have slots to implement OOP mechanics
    ## @{
    
    ## `sym[key]=o` operator: store attributes in form of key/value
    def __setitem__(self,key,o):
        if type(o) == type(''): self.attr[key] = String(o)  # wrap string 
        else: self.attr[key] = o
        return self
    ## `sym[key]` operator: fetch object by its name
    def __getitem__(self,key): return self.attr[key]
    ## @}    
    
    ## @defgroup nest Nested elements = vector = stack
    ## @ingroup object
    ## @brief <b>any object</b> can hold nested elements (AST tree),
    ## data in order, and use it in a stack-like way (push/pop/...)
    ## @{
    
    ## `obeject << any` operator adds object to `nest[]`ed
    def __lshift__(self,o): return self.push(o)
    ## push element stack-like
    def push(self,o): self.nest.append(o) ; return self
    ## pop top (end) value
    def pop(self): return self.nest.pop()
    ## @return top element without invasive pop
    def top(self): return self.nest[-1]
    ## duplicate top element
    def dup(self): self.nest.append(self.top()) ; return self
    ## remove top element
    def drop(self): del self.nest[-1] ; return self
    ## swap topmost two elements
    def swap(self):
        B = self.pop() ; A = self.pop()
        self.push(B) ; self.push(A)
        return self
    ## primitive objects executes into itself
    def __call__(self): D << self
    
## @defgroup symtests Tests
## run tests using `py.test -v oFORTH.py`
## @{

## @test symbol creation
def test_Object():      assert Object('test').head() == '<object:test>'
## @test `attr{}`ibutes empty creation
def test_Object_attr(): assert Object('attr{}').attr == {}
## @test `nest[]`ed list empty creation
def test_Object_nest(): assert Object('nest[]').nest == []

## @}

## @}

## @defgroup prim Primitive types
## @brief key feature: **evaluates to itself**
## @ingroup sym
## @{
       
class Primitive(Object): pass

## @test primitive
def test_Primiteve():
    assert Primitive('atom').dump() == '\n<primitive:atom>'

## @}

## @defgroup symbol Symbol
## @brief generic identifier targets to name any entity
## @ingroup prim
## @{

## Symbol targets to name any entity
class Symbol(Primitive): pass

## @test symbol for Pi number
def test_Symbol():
    assert Symbol('Pi').head() == '<symbol:Pi>'

## @}

## @defgroup string String
## @brief text string
## @ingroup prim
## @{

## string
class String(Primitive):
    ## dump string in line form
    ## @param[in] prefix optional string will be put before ``string``
    def head(self,prefix=''):
        H = "%s'" % prefix
        for c in self.val:
            if c == '\t': H += '\\t'
            elif c == '\r': H += '\\r'
            elif c == '\n': H += '\\n'
            else: H += c
        return H+"'"

## @test hello world
def test_String():
    assert String('world').head(prefix='hello ') == 'hello <string:world>'

## @}
        
## @defgroup number Numbers
## @brief floating point, integers, hex/binary, complex,...
## @ingroup prim
## @{

## floating point number
class Number(Primitive):
    ## construct floating point number 
    def __init__(self,V):
        Primitive.__init__(self, V)
        ## wrap python float
        self.val = float(V)

## @test type/value for wrapped dotted number
def test_Number_point(): assert \
    type(Number('-0123.45').val) == type(-123.45) and \
    abs( Number('-0123.45').val - (-123.45) ) < 1e-6

## @test type/value for wrapped exponential number
def test_Number_exp(): assert \
    type(Number('-01.23e+45').val) == type(-123.45) and \
    abs( Number('-01.23E+45').val - (-1.23e45) ) < 1e-6
        
## integer
class Integer(Number):
    ## construct with optional base
    def __init__(self,V,base=10):
        Primitive.__init__(self, V)
        ## wrap python integer
        self.val = int(V,base)

## @test type and value for wrapped integer 
def test_Integer(): assert \
    type(Integer('-012345').val) == type(-12345) and \
         Integer('-012345').val  == -12345        

## hexadecimal (machine) number         
class Hex(Integer):
    ## inherit integer with base=16
    def __init__(self,V): Integer.__init__(self, V[2:], 0x10)
    ## dump in hex
    def head(self,prefix=''): return '%s<%s:0x%X>'%(prefix,self.tag,self.val)
    
## @test hex number reading
def test_Hex(): assert Hex('0x1234').val == 0x1234
    
## binary (machine) number
class Bin(Integer):
    ## inherit integer with base=2
    def __init__(self,V): Integer.__init__(self, V[2:], 0x02)
    
## @test binary number reading
def test_Bin(): assert Bin('0b1101').val == 0b1101

## @}

## @defgroup cont Containers
## data containers
## @ingroup sym
## @{

## any data container
class Container(Object): pass

## @test generic container
def test_Container():
    assert Container('with some data').head() == '<container:with some data>'

## @}

## @defgroup stack Stack
## Stack supports push/pop operations and Last In First Out discipline
## @ingroup cont
## @{

## LIFO Stack
class Stack(Container): pass

## @test empty stack
def test_Stack(): assert Stack('stack').nest == []

## @test flush
def test_Stack_flush(): assert Stack('flush test').flush().nest == []

## @test push
def test_Stack_push(): assert \
    ( Stack('push test') << 1 << 2 << 3 ).nest == [1,2,3]

## @test pop
def test_Stack_pop():
    S = Stack('pop test') << 1 << 2
    assert S.pop() == 2 ; assert S.nest == [1]

## @test top
def test_Stack_top():
    assert ( Stack('top test') << 1 << 2 ).top() == 2

## @test drop
def test_Stack_drop():
    S = Stack('drop test') << 1 << 2 ; S.drop() ; assert len(S.nest) == 1

## @test dup
def test_Stack_dup():
    assert ( Stack('dup test') << 1 ).dup().nest == [1,1]

## @test swap
def test_Stack_swap():
    assert ( Stack('swap test') << 1 << 2 ).swap().nest == [2,1]

## @}

## @defgroup map Map
## container holds elements indexed by string key /unordered associative array/
## @ingroup cont
## @{

## unordered key:value storage should be used as FORTH vocabulary 
class Map(Container):
    ## `map << object` operator stores object using its name as key
    def __lshift__(self,o):
        # treat as symbolic object
        try: self[o.val] = o
        # fallback in case of map << python function
        except AttributeError: self[o.__name__] = Fn(o)
        return self

## @test empty map
def test_Map(): assert Map('map').attr == {}

## @test pushing to map with `<<` operator
def test_Map_lshift():
    M = Map('set') << test_Map_lshift ; print M
    assert M.dump() == '\n<map:set>\n\ttest_Map_lshift = <fn:test_Map_lshift>'
    
## @test fetch and store using string keys
def test_Map_getset():
    M = Map('get/set') ; M['X'] = 'Y'
    assert M['X'].tag == 'string' and M['X'].val == 'Y'

## @}

## @defgroup vector Vector
## ordered container with integer index
## /<b>has executable semantics</b> for oFORTH callable code blocks/
## @ingroup cont
## @{

## ordered vector
class Vector(Container):
    ## vector is callable as it used for sequential code blocks in oFORTH
    def __call__(self):
        for i in self.nest: i()

## @test vector creation        
def test_Vector():
    assert ( Vector('ordered') << 1 << 2 << 3 ).nest == [1,2,3]
    
## @test vector execute
def test_Vector_execute():
    V = Vector('empty')
    assert V.dump() == '\n<vector:empty>'
    V()
    assert V.dump() == '\n<vector:empty>'

## @}

## @defgroup queue Queue
## LIFO ordered container friendly with Python threading
## @ingroup cont
## @{

## queue wraps threading-friendly Queue
class Queue(Container):
    ## construct wrapped Queue 
    def __init__(self,V):
        Container.__init__(self, V)
        ## wrap Python Queue
        self.nest = pyQueue.Queue()
    ## dump queue as size:n
    def dumpnest(self, depth=0):
        return '\n'+self.pad(depth+1)+'size:%s'%self.nest.qsize()
    ## put element
    def push(self,o): self.nest.put(o) ; return self
    ## pop element
    ## @param[in] timeout optional timeout, seconds
    def pop(self,timeout=None):
        if timeout: return self.nest.get(timeout=timeout)
        else: return self.nest.get()

## @test empty queue creation
def test_Queue():
    assert Queue('SRC').dump() == '\n<queue:SRC>\n\tsize:0'

## @test queue push/pop    
def test_Queue_pushpop():
    Q = Queue('queue') << 1 << 2 << 3
    assert Q.pop() == 1

## @}

## @defgroup active Active
## executable objects wrapped from Python VM and modules
## @ingroup sym
## @{

## active callable object
class Active(Object): pass

## function wrapper
class Fn(Active):
    ## wrap function
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        ## wrapped function pointer
        self.fn = F
    ## implement execution semantics (callable object)
    def __call__(self): return self.fn()

## @test function without call        
def test_Fn(): assert Fn(test_Fn).head() == '<fn:test_Fn>'

## @test function with call
def test_Fn_call(): assert Fn(lambda:True) () == True

## @}

## @defgroup FVM oFORTH Virtual Machine

## @defgroup voc Vocabulary
## holds global definitios
## @ingroup FVM
## @{

## global vocabulary register
W = Map('FORTH')

## @test global vocabulary
def test_FVM_W(): assert W.head() == '<map:FORTH>'

## @}

## @defgroup fvmstack Global data stack
## all computations in FORTH use only stack (no registers or variables)
## @ingroup FVM
## @{

## global data stack register
D = Stack('DATA')

## @test empty stack dump
def test_FVM_D(): assert D.dump() == '\n<stack:DATA>'

## `DUP ( o - o o )` duplicate top stack element
def DUP(): D.dup()
W << DUP

## `DROP ( o1 o2 -- o1 )` drop top element
def DROP(): D.drop()
W << DROP

## `SWAP ( o1 o2 -- o2 o1 )` swap 2 top elements
def SWAP(): D.swap()
W << SWAP

## @}

## @defgroup interp Interpreter/Compiler
## @ingroup FVM
## @{

## @defgroup ply Syntax parser /lexer only/
## made with PLY parser generator library
## @{

import ply.lex as lex

## list of supported token types
tokens = ['SYM','NUM','HEX','STR']

## multiple lexing states: string parsing with `\escapes`
states = (('string','exclusive'),)

## ignored chars: spaces
t_ignore = ' \t\r\n'

## line comments can start with `#` and `\` , and ( block comments ) in parens
t_ignore_COMMENT = r'[\#\\].*|\(.*?\)'

## count line numbers
def t_newline(t):
    r'\n'
    t.lexer.lineno += 1

## hex number
def t_HEX(t):
    r'0x[0-9a-fA-F]+'
    t.value = Hex(t.value) ; return t
    
## float numbers
def t_NUM(t):
    r'[\+\-]?[0-9]+(\.[0-9]*)?([eE][\+\-]?[0-9]+)?'
    t.value = Number(t.value) ; return t
    
## symbol lexer rule
def t_SYM(t):
    r'[a-zA-Z0-9_\?\:\;\.\+\-]+'
    t.value = Symbol(t.value) ; return t

## ignore chars in string mode 
t_string_ignore = ''
## move to `string` state on `'`
def t_begin_string(t):
    r'\''
    t.lexer.push_state('string')
    t.lexer.string=''
## return from `string` state on `'`
## @returns string token
def t_string_STR(t):
    r'\''
    t.lexer.pop_state()
    t.value = String(t.lexer.string) ; return t
## tab
def t_string_tab(t):
    r'\\t'
    t.lexer.string += '\t'
## cr
def t_string_cr(t):
    r'\\r'
    t.lexer.string += '\r'
## lf
def t_string_lf(t):
    r'\\n'
    t.lexer.string += '\n'
## any char in `string` mode    
def t_string_char(t):
    r'.'
    t.lexer.string += t.value
    
## lexer error callabck
def t_ANY_error(t): raise SyntaxError(t)

## end of file must reset FVM
def t_eof(t): global COMPILE ; COMPILE = [] 

## global lexer
lexer = lex.lex()

## @}

## `WORD ( -- symbol:wordname )`
## parse next word name from source code stream
## @returns token will be empty on EOF
## @ingroup lexer
def WORD():
    token = lexer.token()                   # call syntax parser /lexer/
    if token: D << token.value              # push parsed object to data stack
    return token                            # PLY token will be empty on EOL
W << WORD

## `FIND ( wordname -- callable:xt )`
## lookup execatable definition in vocabulary
def FIND():
    o = D.pop() ; WN = o.val                # pop name to be found
    try: D.push(W[WN])                      # lookup in vocabulary
    except KeyError: raise SyntaxError(o)
    
## `EXECUTE ( xt -- )` run object with executable semantics
def EXECUTE(): D.pop()()
W << EXECUTE    

## `INTERPRET ( -- )`
## [R]ead [E]val [P]rint [L]oop
## @param[in] SRC source code should be interpreted
def INTERPRET(SRC=''):
    lexer.input(SRC)                        # feed lexer
    while True:
        if not WORD(): break                # parse and exit on EOF
        if D.top().tag in ['symbol']:
            FIND()                          # look up in vocabulary
        if not COMPILE or D.top().immed:
            EXECUTE()                       # run found callable object
        else:
            COMPILE << D.pop()              # compile
    gui_thread.onDump(None)

## @test empty script
def test_INTERPRET_empty():
    assert D.nest == [] ; INTERPRET('') ; assert D.nest == []
    
## @test numbers
def test_INTERPRET_comments():
    assert D.nest == []
    INTERPRET('# line comment \n ( block comment )')
    assert D.nest == []

## @test numbers
def test_INTERPRET_numbers():
    assert D.nest == []
    INTERPRET('( numbers ) +01 -002.3 -4e+05')
    assert D.pop().val == -4e+05
    assert D.pop().val == -2.3
    assert D.pop().val == +1
    assert D.nest == []
    
## compilation register = interpret/compile state flag
COMPILE = None

## `: ( -- )` start colon definition
def colon():
    WORD() ; WN = D.pop().val                       # lex forward new word name
    global COMPILE ; W[WN] = COMPILE = Vector(WN)   # can use name for recurse
W[':'] = Fn(colon)

## `; ( -- )` stop colon definition
def semicolon():
    global COMPILE ; print COMPILE ; COMPILE = None
W[';'] = Fn(semicolon) ; W[';'].immed = True

## @}

## @defgroup debug Debug
## @ingroup FVM
## @{

## `? ( -- )` dump data stack
def DumpStack(): print D
W['?'] = Fn(DumpStack)

## `?? ( -- )` dump full FVM state
def DumpFVM(): print W ; print D
W['??'] = Fn(DumpFVM)

## '. ( ... -- )` clear system state (data stack)
def DropAll(): D.flush()
W['.'] = Fn(DropAll) 

## `?dis <wordname> ( -- )` disassemble `<wordname>`
def dis(): WORD() ; FIND() ; print D.pop()
W['?dis'] = Fn(dis)

## @}

## @defgroup gui GUI engine
## `wxPython`
## @{

## command processing queue
CMD = Queue('CMD')

## interpreter will run in background
class CMD_thread(threading.Thread):
    ## stop thread flag
    stop = False
    ## infty loop on command queue processing
    def run(self):
        while not self.stop:
            try: INTERPRET(CMD.pop(timeout=1))  # process next command
            except pyQueue.Empty: pass          # required for self.stop flag
            except:                             # don't stop thread on errors
                COMPILE = []                    # drop compilation mode
                print sys.exc_info()            # print error frame
## command processing singleton thread
cmd_thread = CMD_thread()

## GUI processing in separate thread
class GUI_thread(threading.Thread):
    ## run GUI in background
    def __init__(self):
        threading.Thread.__init__(self)
        ## wx application
        self.app = wx.App()
        ## main window
        self.main = wx.Frame(None,wx.ID_ANY,str(sys.argv))
        ## vocabulary/stack dump windows
        self.SetupDumpers()
        ## menu
        self.SetupMenu()
        ## editor area
        self.SetupEditor()
    ## condifure menu
    def SetupMenu(self):
        ## menu bar
        self.menubar = wx.MenuBar() ; self.main.SetMenuBar(self.menubar)
        ## file menu
        self.file = wx.Menu() ; self.menubar.Append(self.file,'&File')
        ## file/save
        self.save = self.file.Append(wx.ID_SAVE,'&Save')
        self.main.Bind(wx.EVT_MENU, self.onSave, self.save)
        ## file/export
        self.export = self.file.Append(wx.ID_CONVERT,'Ex&port') 
        self.file.AppendSeparator()
        ## file/exit
        self.exit = self.file.Append(wx.ID_EXIT,'E&xit')
        self.main.Bind(wx.EVT_MENU, lambda e:self.main.Close(), self.exit)
        ## debug demu
        self.debug = wx.Menu() ; self.menubar.Append(self.debug,'&Debug')
        ## debug/dump
        self.dump = self.debug.Append(wx.ID_EXECUTE,'DUMP\tF12')
        self.main.Bind(wx.EVT_MENU, self.onDump, self.dump)
        ## debug/vocabulary
        self.vocabulary = self.debug.Append(wx.ID_ANY,'&Vocabulary',kind=wx.ITEM_CHECK)
        self.menubar.Check(self.vocabulary.GetId(),True) ; self.ToggleVocabulary(None)
        self.main.Bind(wx.EVT_MENU,self.ToggleVocabulary,self.vocabulary)
        ## debug/stack
        self.stack = self.debug.Append(wx.ID_ANY,'&Stack',kind=wx.ITEM_CHECK)
        self.menubar.Check(self.stack.GetId(),True) ; self.ToggleStack(None)
        self.main.Bind(wx.EVT_MENU, self.ToggleStack, self.stack)
        ## help menu
        self.help = wx.Menu() ; self.menubar.Append(self.help,'&Help')
        ## help/about
        self.about = self.help.Append(wx.ID_ABOUT,'&About\tF1')
        self.main.Bind(wx.EVT_MENU, self.onAbout, self.about)
        
    ## configure editor
    def SetupEditor(self):
        ## editor: use StyledText widget with rich syntax coloring
        self.editor = self.main.control = wx.stc.StyledTextCtrl(self.main)
        self.ReOpen(None)
        ## configure font size
        W,H = self.main.GetClientSize()
        self.editor.StyleSetFont(wx.stc.STC_STYLE_DEFAULT, \
            wx.Font(H>>4, wx.FONTFAMILY_MODERN, wx.NORMAL, wx.NORMAL))
        
    ## reopen file in editor
    def ReOpen(self,e,filename='src.src'):
        ## save used file name
        self.filename = filename
        F = open(filename) ; self.editor.SetValue(F.read()) ; F.close()
        ## left margin with line numbers
        self.editor.SetMargins(5,0)
        self.editor.SetMarginType(1,wx.stc.STC_MARGIN_NUMBER)
        self.editor.SetMarginWidth(1,33)
        # bind keys
        ## font scaling Ctrl +/-
        self.editor.CmdKeyAssign(ord('='),wx.stc.STC_SCMOD_CTRL,wx.stc.STC_CMD_ZOOMIN )
        self.editor.CmdKeyAssign(ord('-'),wx.stc.STC_SCMOD_CTRL,wx.stc.STC_CMD_ZOOMOUT)
        ## run code on Ctrl-Enter
        self.editor.Bind(wx.EVT_CHAR,self.onChar)
    ## save handler
    def onSave(self,e):
        F = open(self.filename,'w') ; F.write( self.editor.GetValue() ) ; F.close()
    ## event handler: process keyboard events
    def onChar(self,e):
        key = e.GetKeyCode() ; ctrl = e.CmdDown() ; shift = e.ShiftDown()
        if key == 13 and ( ctrl or shift ): CMD.push(self.editor.GetSelectedText())
        else: e.Skip()
    ## about event handler
    def onAbout(self,e):
        F = open('README.md') ; wx.MessageBox(F.read(166)) ; F.close()
        
    ## activate GUI elements only on thread start
    ## (interpreter system can run in headless mode)
    def run(self):
        self.main.Show()
        self.app.MainLoop()
        
    ## configure dump windows
    def SetupDumpers(self):
        # vocabulary
        ## vocabulary dump window
        self.dumpvocab = wx.Frame(self.main,wx.ID_ANY,W.head())
        ## vocabulary widget (generic text editor)
        self.editvoc = self.dumpvocab.control = wx.stc.StyledTextCtrl(self.dumpvocab)
        # stack
        ## data stack dump window
        self.dumpstack = wx.Frame(self.main,wx.ID_ANY,D.head())
        ## stack widget (generic text editor)
        self.editstack = self.dumpstack.control = wx.stc.StyledTextCtrl(self.dumpstack)
    ## dump system state
    def onDump(self,e):
        self.onVocabularyUpdate(e)
        self.onStackUpdate(e)
    ## toggle vocabulary window
    def ToggleVocabulary(self,e):
        if self.dumpvocab.IsShown(): self.dumpvocab.Hide()
        else: self.dumpvocab.Show() ; self.onDump(e)
    ## toggle stack window
    def ToggleStack(self,e):
        if self.dumpstack.IsShown(): self.dumpstack.Hide()
        else: self.dumpstack.Show() ; self.onDump(e)
    ## update vocabulary window
    def onVocabularyUpdate(self,e):
        if self.dumpvocab.IsShown(): self.editvoc.SetValue(str(W))
    ## update stack window
    def onStackUpdate(self,e):
        if self.dumpstack.IsShown(): self.editstack.SetValue(str(D))
        
## GUI thread singleton
gui_thread = GUI_thread()

## @}

import pickle

if __name__ == '__main__':
    # pickle
    W = pickle.load(open(sys.argv[0]+'.image'))
    # start
    gui_thread.start()
    cmd_thread.start()
    gui_thread.join()
    ## stop command processing thread
    cmd_thread.stop = True
    ## and wait until cmd dispatch tick will be end
    cmd_thread.join()
    ## pickle
    pickle.dump(W,open(sys.argv[0]+'.image','w'))
