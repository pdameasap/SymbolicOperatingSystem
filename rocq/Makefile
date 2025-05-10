# Makefile for compiling ROCQ-based SHF Coq modules

COQC=coqc
COQFLAGS=-Q . rocq

FILES=\
  versare_syntax.v \
  versare_semantics.v \
  versare_properties.v \
  versare_tensor.v

all: $(FILES:.v=.vo)

clean:
	rm -f *.vo *.glob
