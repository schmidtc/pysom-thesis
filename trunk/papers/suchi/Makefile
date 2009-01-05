all: geows09.pdf

view: geows09.pdf
	open geows09.pdf

geows09.pdf: ../bib/*.bib *.tex
	( pdflatex geows09 || rm -f geows09.pdf ) && \
	bibtex geows09 && \
	( pdflatex geows09 || rm -f geows09.pdf ) && \
	( pdflatex geows09 ) && \
	( pdflatex geows09 )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof geows09.ps geows09.pdf
