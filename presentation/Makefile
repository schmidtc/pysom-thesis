all: pres.pdf

view: pres.pdf
	open pres.pdf

pres.pdf: *.tex
	( otl2latex.py -p pres.otl pres.tex ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres || rm -f pres.pdf ) && \
	( pdflatex pres )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof pres.pdf *.nav *.out *.snm 

