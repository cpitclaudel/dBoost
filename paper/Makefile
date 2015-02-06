FIGDIR = ../graphics/plots
TEXFILES=$(wildcard *.tex)
#PLOTS = sensors_gm sensors_mm
PDFFIGS := $(PLOTS:%=$(FIGDIR)/%.pdf)

PYPLOTS=$(wildcard ../graphics/*.py)
PYPLOTS_PDFS=$(PYPLOTS:.py=.pdf)

print-%:
	@echo $* = $($*)

all: paper.pdf

$(FIGDIR)/%.pdf:
	cd $(FIGDIR) && python3 plots.py
	pdfcrop $@ $@

$(PYPLOTS_PDFS): %.pdf: %.py
	python3 $< $@
	pdfcrop $@ $@

paper.pdf: $(TEXFILES) $(PDFFIGS) $(PYPLOTS_PDFS)
	pdflatex -draftmode -shell-escape paper.tex
	bibtex paper.aux
	pdflatex -draftmode -shell-escape paper.tex
	pdflatex -shell-escape paper.tex

view: paper.pdf
	open paper.pdf

clean:
	rm -fv *.pdf *.aux *.bbl *.blg *.log *.out $(CROP_FILES) $(PDFFIGS) $(PYPLOTS_PDFS)
