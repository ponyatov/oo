#ifndef _H_HPP
#define _H_HPP

#include <iostream>
using namespace std;

struct Sym {			// base object class
	Sym(string V);
	string dump();
};

						// = lexer interface
extern int yylex();		// get next token
extern int yylineno;	// current line no
extern char* yytext;	// lexed text string
						// == parser interface
extern int yyparse();	// parser entry
extern void yyerror(string);// error callback
#include "ypp.tab.hpp"	// token definitions

#endif // _H_HPP
