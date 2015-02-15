tests=$(shell ls *eg.py)

make=cd ..; $(MAKE) --no-print-directory

test:
	@$(MAKE) tests | awk -f ../etc/tests.awk

tests:
	@$(foreach f,$(tests), python $f;)

typo:    ; @$(make) typo
commit:  ; @$(make) commit
update:  ; @$(make) update
status:  ; @$(make) status
publish: ; @$(make) publish

a2ps: publish
	mkdir -p var
	git add var
	pandoc -s -N --template=template.tex   -V fontsize=7pt ../doc/cocomo.md -o var/$@.pdf 
	pdfnup var/$@.pdf --no-landscape  --frame true --nup 1x2 -o var/${@}2.pdf
	mv var/${@}2.pdf var/$@.pdf
	git add var/$@.pdf

eg1:; python libeg.py
eg2:; python countseg.py
eg3:; python cocomoeg.py
eg4:; python badSmellseg.py
