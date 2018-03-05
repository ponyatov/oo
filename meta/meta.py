# meta/macro compiler in Python into embedded C(++)

import os,sys,re

class Object():
    def __init__(self,V): self.value = V ; self.attr={} ; self.nest = []
    def __lshift__(self,V): return self.push(V)
    def push(self,o): self.nest.append(o) ; return self
    def __setitem__(self,K,V): self.attr[K] = V ; return self
    def __getitem__(self,K): return self.attr[K]
    def __repr__(self): return self.dump()
    def head(self,prefix=''):
        return '%s<%s:%s>'%(prefix,self.__class__.__name__.lower(),self.value)
    def pad(self,N): return '\n'+'\t'*N
    def dump(self,depth=0):
        S = self.pad(depth)+ self.head()
        for i in self.attr:
            S += self.pad(depth+1) + self.attr[i].head(prefix='%s = '%i)
        for j in self.nest:
            S += j.dump(depth+1)
        return S
    
class Symbol(Object): pass
    
class File(Object):
    def __init__(self,V):
        Object.__init__(self, V)
        self.fh = open(V,"w")
    def write(self,o): return self.fh.write(o)
        
class Dir(Object):
    def __init__(self,V):
        Object.__init__(self, V)
        try: os.mkdir(V)
        except OSError: pass # exists
    def __add__(self,o):
        if type(o) == str: return File('%s/%s'%(self.value,o))
        else: raise TypeError(str(type(o)))

class Module(Object):
    def __init__(self,V):
        Object.__init__(self, V)
        self['dir'] = Dir(V)
        self['mk'] = self['dir']+'Makefile'
        self['cpp'] = self['dir']+(V+'.c')
        print >>self['mk'],\
            '# %s\n./%s$(EXE): ./%s.c Makefile\n\t$(CC) $(CFLAGS) -o $@ $<' \
                % (self.head(),self.value,self.value)
    def build(self):
        for i in self.nest: print >> self['cpp'] , i.cpp()
#         os.system('make -C %s' % self.value) ;
        return self
    
class Type(Object): pass

void = Type('void')
int  = Type('int')

class Function(Object):
    def __init__(self,V,type=void):
        Object.__init__(self, V)
        self['type'] = type
    def cpp(self): return '%s %s() {}' % (self['type'].cpp(),self.value)

hello = Module('hello')

hello << Function('main',type=int)

print hello.build()
