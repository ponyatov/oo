FORTH.bc: log.log
log.log: FORTH.uF ./micro.exe ./compiler.exe
	./compiler.exe < $< > $@ && tail $(TAIL) $@

# virtual machine / emulator
# strict old C compiling: for portability and strange C compilers
VM_CFLAGS += -std=c89 -Wall -Wextra -Werror
./micro.exe: ./micro.c
	$(CC) $(VM_CFLAGS) -DEMULATOR -o $@ $<
	
# byte-code compiler (bison/flex powered)
# uses some rich C++ features, so not very portable
./compiler.exe: lexer.cpp
	$(CXX) -o $@ $^
lexer.cpp: compiler.lex
	flex -o $@ $< 