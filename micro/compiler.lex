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

\:				{yylex(); cout << yytext << endl;
				//LFA(0);
				return 0;}
				
\;				{ B(RET); return 0; }

[a-zA-Z0-9_]+	{return 0;}

[ \t\r\n]+		{}		// drop spaces
.				{yyerror("lexer");}

<<EOF>>			{ return EOF; }

%%

int main(int argc, char *argv[]) {
	assert(argc==2);
	LFA(0x12345678);
	LFA(0);
	while (yylex() != EOF);
	SAVE(argv[1]);
}