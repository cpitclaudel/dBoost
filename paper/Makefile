TEXFILES=$(wildcard *.tex)

all: paper.pdf

../graphics/models-plots.pdf:
	cd ../graphics/ && python3 models-plots.py

../graphics/models-plots-crop.pdf: ../graphics/models-plots.pdf
	cd ../graphics/ && pdfcrop models-plots.pdf

paper.pdf: $(TEXFILES) ../graphics/models-plots-crop.pdf
	pdflatex -shell-escape paper.tex
	bibtex paper.aux
	pdflatex -shell-escape paper.tex
	pdflatex -shell-escape paper.tex

clean:
	rm -fv *.pdf *.aux *.bbl *.blg *.log *.out
