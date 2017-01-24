include Makefile.local

ifndef PYDIR
$(error Fatal: Makefile.local must define PYDIR variable)
endif

PYFILES=ch_frb_rfi/__init__.py \
	ch_frb_rfi/acquisitions.py \
	ch_frb_rfi/chains.py \
	ch_frb_rfi/helper_transform.py \
	ch_frb_rfi/utils.py

install:
	mkdir -p $(PYDIR)/ch_frb_rfi
	for f in $(PYFILES); do cp $$f $(PYDIR)/$$f; done

uninstall:
	rm -rf $(PYDIR)/ch_frb_rfi/
