" |O|bject system file types
" github: https://github.com/ponyatov/o

au BufNewFile,BufRead src.src set filetype=o
au BufNewFile,BufRead log.log set filetype=o
au BufNewFile,BufRead *.ypp set filetype=yacc
au BufNewFile,BufRead *.lpp set filetype=lex
au BufNewFile,BufRead *.hpp set filetype=cpp
au BufNewFile,BufRead *.cpp set filetype=cpp

au BufNewFile,BufRead *.log set autoread
au BufNewFile,BufRead *.py set expandtab

