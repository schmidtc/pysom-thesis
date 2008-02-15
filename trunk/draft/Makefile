all: thesis.pdf

view: thesis.pdf
	open thesis.pdf

thesis.pdf: ../bib/*.bib *.tex *.cls
	( pdflatex thesis || rm -f thesis.pdf ) && \
	bibtex thesis && \
	( pdflatex thesis || rm -f thesis.pdf ) && \
	( pdflatex thesis )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof thesis.ps thesis.pdf
