COQC=coqc
COQFLAGS=-Q . rocq

FILES=\
  versare_syntax.v \
  versare_semantics.v \
  versare_properties.v \
  versare_tensor.v

all: $(FILES:.v=.vo)

docs: $(FILES:.v=.html)

%.vo: %.v
	$(COQC) $(COQFLAGS) $<

%.html: %.v
	coqdoc --html $<

clean:
	rm -f *.vo *.glob *.html *.aux
