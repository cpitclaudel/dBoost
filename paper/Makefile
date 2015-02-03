
FIGDIR = ../graphics/plots
TEXFILES=$(wildcard *.tex)
PLOTS = sensors_gm sensors_mm
PDFFIGS := $(PLOTS:%=$(FIGDIR)/%.pdf)

print-%:
	@echo $* = $($*)

all: paper.pdf

$(FIGDIR)/%.pdf:
	cd $(FIGDIR) && python3 plots.py
	pdfcrop $@ $@

paper.pdf: $(TEXFILES) $(PDFFIGS)
	pdflatex -shell-escape paper.tex
	bibtex paper.aux
	pdflatex -shell-escape paper.tex
	pdflatex -shell-escape paper.tex

view: paper.pdf
	open paper.pdf

clean:
	rm -fv *.pdf *.aux *.bbl *.blg *.log *.out $(CROP_FILES) $(PDFFIGS)
