default: doc/manual.pdf
# log.log
# micro
# log.log micro/log.log android

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
TEX += doc/micro/*.tex doc/meta/* doc/model/*.tex doc/plan/*.tex doc/web/*.tex
TEX += doc/img/*
doc/manual.pdf: $(TEX) doc/Makefile doc/*.sty
	cd doc ; $(MAKE)

micro: micro/log.log
micro/log.log: micro/*.c micro/*.h micro/*.lex micro/*.uF
	cd micro ; $(MAKE)
	
android: Android/app/src/main/res/mipmap-mdpi/ic_launcher.png
Android/app/src/main/res/mipmap-mdpi/ic_launcher.png: doc/img/hedgehog_black.png Makefile
	convert $< -resize 48x48\> $@
#	convert $< -resize 48x48^ -gravity center -extent 48x48 -background black $@ 
doc/img/hedgehog.png:
	wget -c -O $@ https://github.com/ponyatov/icons/raw/master/hedgehog.png
	
js: js/logo.png
js/logo.png: doc/img/hedgehog_black.png Makefile
	convert $< -scale 64x64 miff:- | convert - -extent 64x64 -background black -gravity center $@
#	   -gravity center  $@
