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

\:				{yylex();							// lex word name
				LFA();								// \ compile word header
				UCELL push_NFA = Cp;				// save NFA for debug/label
				NFA(yytext); AFA(0); CFA();
				B(LABEL); W(push_NFA);				// / mark label
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
	assert(argc==3);
								// compile bytecode image header:
	B(JMP); W(0);				// ENTRY: jmp _entry
	W(0);						// HEAP: Cp register must be HERE
	W(0);						// first LFA marks begin of vocabulary
	
	while (yylex() != EOF);		// run compiler
	set(HEAP,Cp);				// save Cp
	SAVE(argv[1]); DUMP();		// save/dump resulting bytecode image
	
	FILE *js = fopen(argv[2],"w"); assert(js);
	fprintf(js,"var M = new Uint8Array([\t\t\t// main memory\n");
	for (uint16_t addr = 0; addr < Cp; addr++) {
		if (addr % 8 ==0) fprintf(js,"\n\t/* %.4X */\t",addr);
		fprintf(js,"0x%.2X,",M[addr]);
	}
	fprintf(js,"\n0]);\n\n");
	fprintf(js,"var Cp = 0x%.4X;\t// instruction pointer\n\n",Cp);
	fprintf(js,"var Ip = 0x%.4X;\t// compiler (heap) pointer\n\n",get(1));
	fclose(js);
}
