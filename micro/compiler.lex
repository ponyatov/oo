%{
#include "h.h"
#include <iostream>
#include <map>
using namespace std;

FILE *img=NULL;

#define YYERR "\n\n"<<yylineno<<":"<<msg<<"["<<yytext<<"]\n\n"
void yyerror(string msg) { cout<<YYERR; cerr<<YYERR; abort(); }
%}
%option noyywrap
%%
\\[^\n]*		{}		// line comments

\:				{yylex(); cout << yytext << endl; return 0;}
\;				{ B(RET); return 0; }

[a-zA-Z0-9_]+	{return 0;}

[ \t\r\n]+		{}		// drop spaces
.				{yyerror("lexer");}

<<EOF>>			{ assert( fwrite(M,Mp,1,img)==Mp ); fclose(img); exit(0); }

%%

int main(int argc, char *argv[]) {
	assert(argc==2);
	assert( img=fopen(argv[1],"wb") );
	for (;;) yylex();
}