%{
#include <iostream>
using namespace std;

#define YYERR "\n\n"<<yylineno<<":"<<msg<<"["<<yytext<<"]\n\n"
void yyerror(string msg) { cout<<YYERR; cerr<<YYERR; abort(); }
%}
%option main
%option noyywrap
%%
\\[^\n]*		{}		// line comments
[ \t\r\n]+		{}		// drop spaces
.				{yyerror("lexer");}
