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