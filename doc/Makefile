IMG = img/compiler.png img/frontend.png img/forthend.png

LATEX = pdflatex -halt-on-error

manual.pdf: *.tex $(IMG) *.sty
	$(LATEX) manual && $(LATEX) manual
img/%.png: img/%.dot
	dot -T png -o $@ $< 
img/%.pdf: img/%.dot
	dot -T pdf -o $@ $< && \
	inkscape $@ --export-area-drawing --export-pdf=$@