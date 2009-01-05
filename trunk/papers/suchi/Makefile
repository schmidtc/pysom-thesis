all: paper.pdf

view: paper.pdf
	open paper.pdf

paper.pdf: ../../bib/*.bib *.tex
	( pdflatex paper || rm -f paper.pdf ) && \
	bibtex paper && \
	( pdflatex paper || rm -f paper.pdf ) && \
	( pdflatex paper ) && \
	( pdflatex paper )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof paper.ps paper.pdf
