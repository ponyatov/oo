default: doc/manual.pdf log.log

log.log: src.src VM.py
	python VM.py < $< > $@ && tail $(TAIL) $@

TODAY = $(shell date +%d%m%y)
PDF = oFORTH_$(TODAY).pdf
.PHONY: doc pdf
doc: pdf
pdf: $(PDF)
$(PDF): doc/manual.pdf
	cp $< $@
doc/manual.pdf: doc/*.tex doc/Makefile doc/img/* doc/*.sty
	cd doc ; $(MAKE)
