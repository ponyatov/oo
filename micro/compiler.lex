%{
#include "h.h"
#include <iostream>
#include <map>
using namespace std;

#define YYERR "\n\n"<<yylineno<<":"<<msg<<"["<<yytext<<"]\n\n"
void yyerror(string msg) { cout<<YYERR; cerr<<YYERR; abort(); }
%}
%option noyywrap
%%
\\[^\n]*		{}		// line comments
\([^\)]*\)		{}		// ( coment in commas )

\:				{yylex(); cout << yytext << endl;
				LFA(); NFA(yytext); AFA(0); CFA();	// compile word header
				return 0; }
				
\;				{ B(RET); return 0; }

nop				{ B(NOP); return 0; }				// predefined commands
bye				{ B(BYE); return 0; }

[a-zA-Z0-9_]+	{return 0;}

[ \t\r\n]+		{}		// drop spaces
.				{yyerror("lexer");}

<<EOF>>			{ return EOF; }

%%

int main(int argc, char *argv[]) {
	assert(argc==2);
								// compile bytecode image header:
	B(JMP); W(0);				// ENTRY: jmp _entry
	W(0);						// HEAP: Cp register must be HERE
	W(0);						// first LFA marks begin of vocabulary
	
	while (yylex() != EOF);		// run compiler
	set(HEAP,Cp);				// save Cp
	SAVE(argv[1]); DUMP();		// save/dump resulting bytecode image
}
