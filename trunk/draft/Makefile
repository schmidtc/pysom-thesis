all: thesis.pdf

view: thesis.ps
	gv thesis.ps

thesis.dvi: *.bib *.eps *.tex *.cls
	( latex thesis || rm -f thesis.dvi ) && \
	bibtex thesis && \
	( latex thesis || rm -f thesis.dvi ) && \
	( latex thesis || rm -f thesis.dvi )

thesis.ps: thesis.dvi
	dvips -t letter -o thesis.ps thesis

thesis.pdf: *.bib *.tex *.cls
	( pdflatex thesis || rm -f thesis.pdf ) && \
	bibtex thesis && \
	( pdflatex thesis || rm -f thesis.pdf ) && \
	( pdflatex thesis )

#thesis.pdf: thesis.ps
#	ps2pdf thesis.ps thesis.pdf

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof thesis.ps thesis.pdf
