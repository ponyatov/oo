log.log: src.src VM.py
	python VM.py < $< > $@ && tail $(TAIL) $@

TODAY = $(shell date +%d%m%y)
PDF = oFORTH_$(TODAY).pdf
.PHONY: doc pdf
doc: pdf
pdf: $(PDF)
$(PDF): doc/manual.pdf
	cp $< $@
doc/manual.pdf: doc/*.tex
	cd doc ; $(MAKE)
