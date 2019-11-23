all: pres

view: pres.pdf
	open pres.pdf

setup: pres.otl
	mkdir -p build/figures && \
	cp -r figures/ build/figures/ && \
	cp pres.otl build/pres.otl

fast: setup
	( otl2latex.py -p pres.otl pres.tex ) && \
	( pdflatex pres ) && \
	( open pres.pdf )

pres: setup
	cd build && \
	( otl2latex.py -p pres.otl pres.tex ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres )

clean:
	rm -rf build

