all: aag2008.pdf g780_paper.pdf

aag2008.pdf: *.tex
	( pdflatex aag2008 || rm -f aag2008.pdf ) && \
	( pdflatex aag2008 || rm -f aag2008.pdf ) && \
	( pdflatex aag2008 )
g780_paper.pdf: *.tex
	( pdflatex g780_paper || rm -f g780_paper.pdf ) && \
	( pdflatex g780_paper || rm -f g780_paper.pdf ) && \
	( pdflatex g780_paper )

clean:
	rm -f *.aux *.bbl *.blg *.dvi *.log *.lot *.toc *.lof
