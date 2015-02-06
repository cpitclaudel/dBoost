FIGDIR = ../graphics/plots
TEXFILES=$(wildcard *.tex)
PLOTS = models-plots lof_2 lof_10 sensors_0-7_1_0-05_0_1 sensors_0-7_1_0-05_0_3 sensors_0_1_0-005_0_1 sensors_0_1_0-005_0_3 sensors_0-7_2_0-25_0_1 sensors_0-7_2_0-25_0_3
PDFFIGS := $(PLOTS:%=$(FIGDIR)/%.pdf)

PYPLOTS=$(wildcard ../graphics/*.py)
PYPLOTS_PDFS=$(PYPLOTS:.py=.pdf)

print-%:
	@echo $* = $($*)

all: paper.pdf

plots: $(PDFFIGS)

$(FIGDIR)/%.pdf: plots.py 
	pdfcrop $@ $@

plots.py:
	cd $(FIGDIR) && python3 plots.py 

#$(PYPLOTS_PDFS): %.pdf: %.py
#	python3 $< $@
#	pdfcrop $@ $@

paper.pdf: $(TEXFILES) 
	pdflatex -draftmode -shell-escape paper.tex
	bibtex paper.aux
	pdflatex -draftmode -shell-escape paper.tex
	pdflatex -shell-escape paper.tex

view: paper.pdf
	open paper.pdf

clean:
	rm -fv *.pdf *.aux *.bbl *.blg *.log *.out $(CROP_FILES) $(PDFFIGS) $(PYPLOTS_PDFS)
