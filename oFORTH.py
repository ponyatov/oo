## @file
## @brief `oFORTH/py` object metasystem /Python implementation/

import os,sys

# wxPython
import wx,wx.stc

# we'll use threaded VM/GUI/HTTP to avoid lockups and system falls
import threading,Queue

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
    ## @param[in] onlystack flag used for stack dump (disable `attr{}` dump)
    def dump(self,depth=0,onlystack=False):
        S = '\n'+self.pad(depth)+self.head()
        if not onlystack:
            for i in self.attr:
                S += '\n' + self.pad(depth+1) + self.attr[i].head(prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
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
    
## @defgroup symtests Tests
## run tests using `py.test -v oFORTH.py`
## @ingroup object
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
class String(Primitive): pass

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
        self.value = float(V)

## @test type/value for wrapped dotted number
def test_Number_point(): assert \
    type(Number('-0123.45').value) == type(-123.45) and \
    abs( Number('-0123.45').value - (-123.45) ) < 1e-6

## @test type/value for wrapped exponential number
def test_Number_exp(): assert \
    type(Number('-01.23e+45').value) == type(-123.45) and \
    abs( Number('-01.23E+45').value - (-1.23e45) ) < 1e-6
        
## integer
class Integer(Number):
    ## construct with optional base
    def __init__(self,V,base=10):
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

## @defgroup active Active
## executable objects wrapped from Python VM and modules
## @ingroup sym
## @{

## active object
class Active(Object): pass

## function wrapper
class Fn(Active):
    ## wrap function
    def __init__(self,F):
        Active.__init__(self,F.__name__)
        ## wrapped function pointer
        self.fn = F

## @}

## @defgroup FVM oFORTH Virtual Machine

## @defgroup gui GUI engine
## `wxPython`

if __name__ == '__main__':
    print Sym('test')