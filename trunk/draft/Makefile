all: thesis.pdf

view: thesis.pdf
	open thesis.pdf

thesis.pdf: ../bib/*.bib *.tex *.cls
	( pdflatex thesis || rm -f thesis.pdf ) && \
	bibtex thesis && \
	( pdflatex thesis || rm -f thesis.pdf ) && \
	( pdflatex thesis ) && \
	( pdflatex thesis ) && \
	echo "\n\n\n\n\n\n DOUBLE CHECK THIS LINE IN YOUR .toc: \contentsline {schapter}{BIBLIOGRAPHY}{39} \n\n\n\n\n\n" && \
	echo "\n\n\n\n\n\n"

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof thesis.ps thesis.pdf
