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
    ## execute object in context of D stack
    ## @pram[in] D context data stack
    def execute(self,D): D << self ; return self
    
def test_Object(): # run tests using py.test -v VM.py
    assert Object('test').head() == '<object:test>'
    
def test_Object_attr(): assert \
    Object('attr{} test').attr == {}
def test_Object_nest(): assert \
    Object('nest[] test').nest == []
    
