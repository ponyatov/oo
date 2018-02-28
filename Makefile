default: doc/manual.pdf log.log micro/log.log

log.log: src.src VM.py
	python VM.py < $< > $@ && tail $(TAIL) $@

TODAY = $(shell date +%d%m%y)
PDF = oFORTH_$(TODAY).pdf
.PHONY: doc pdf
doc: pdf
pdf: $(PDF)
$(PDF): doc/manual.pdf
	cp $< $@
TEX = doc/*.tex doc/core/*.tex doc/oForth/*.tex doc/algo/*.tex doc/dyna/*.tex
TEX += doc/micro/*.tex
TEX += doc/img/*
doc/manual.pdf: $(TEX) doc/Makefile doc/*.sty
	cd doc ; $(MAKE)

micro/log.log: micro/*.c micro/*.lex micro/*.uF
	cd micro ; $(MAKE)