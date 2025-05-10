# Makefile for ROCQ-based SHF Coq modules with HTML docs

COQC=coqc
COQDOC=coqdoc
COQFLAGS=-Q . rocq

FILES=\
  versare_syntax.v \
  versare_semantics.v \
  versare_properties.v \
  versare_tensor.v

all: $(FILES:.v=.vo)

docs: $(FILES:.v=.html)

%.html: %.v
	$(COQDOC) --html $<

clean:
	rm -f *.vo *.glob *.html *.aux
