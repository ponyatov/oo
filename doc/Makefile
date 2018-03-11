TEX = *.tex core/*.tex oForth/*.tex algo/*.tex dyna/*.tex micro/*.tex
TEX +=  meta/*.tex model/*.tex
IMG = img/compiler.png img/frontend.png img/forthend.png 
IMG += img/dynacomp.png img/circomp.png img/dynamodel.png

LATEX = pdflatex -halt-on-error

manual.pdf: $(TEX) $(IMG) *.sty
	$(LATEX) manual && $(LATEX) manual
img/%.png: img/%.dot
	dot -T png -o $@ $< 
img/%.pdf: img/%.dot
	dot -T pdf -o $@ $< && \
	inkscape $@ --export-area-drawing --export-pdf=$@