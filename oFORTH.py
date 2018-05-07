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
        ## @ingroup nest
        self.nest = []
        
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
    def __setitem__(self,key,o): self.attr[key] = o ; return self
    ## `sym[key]` operator: fetch object by its name
    def __getitem__(self,key): return self.attr[key]
    ## @}    
    
    ## @defgroup nest Nested elements = vector = stack
    ## @ingroup object
    ## @brief <b>any object</b> can hold nested elements (AST tree),
    ## data in order, and use it in a stack-like way (push/pop/...)
    ## @{
    
    ## push element stack-like
    def push(self,o): self.nest.append(o) ; return self
    ## pop top (end) value
    def pop(self): return self.nest.pop()
    ## @return top element without pop
    def top(self): return self.nest[-1]    
    
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
        
## @defgroup FVM oFORTH Virtual Machine

## @defgroup gui GUI engine
## `wxPython`

if __name__ == '__main__':
    print Sym('test')