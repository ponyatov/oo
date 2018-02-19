log.log: src.src VM.py
	python VM.py < $< > $@ && tail $(TAIL) $@