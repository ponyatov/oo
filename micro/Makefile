Msz = 0x10000
CFLAGS += -DMsz=$(Msz) 

exec: FORTH.bc ./micro.exe
	./micro.exe $< >> FORTH.log && tail $(TAIL) FORTH.log
FORTH.bc: FORTH.uF ./micro.exe ./compiler.exe
	./compiler.exe FORTH.bc < $< > FORTH.log && tail $(TAIL) FORTH.log

# virtual machine / emulator
# strict old C compiling: for portability and strange C compilers
VM_CFLAGS += -std=c89 -Wall -Wextra
./micro.exe: micro.c c.c h.h
	$(CC) $(VM_CFLAGS) -DEMULATOR -o $@ micro.c c.c
	
# byte-code compiler (bison/flex powered)
# uses some rich C++ features, so not very portable
./compiler.exe: lexer.cpp c.c h.h
	$(CXX) $(CFLAGS) -DEMULATOR -o $@ lexer.cpp c.c
lexer.cpp: compiler.lex
	flex -o $@ $< 