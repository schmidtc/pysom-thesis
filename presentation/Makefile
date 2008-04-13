all: pres

view: pres.pdf
	open pres.pdf

pres: pres.otl
	( otl2latex.py -p pres.otl pres.tex ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof pres.pdf *.nav *.out *.snm 

