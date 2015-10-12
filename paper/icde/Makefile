FIGDIR = ../graphics
TEXFILES=$(wildcard *.tex)

PYPLOTS_PDFS=$(wildcard $(FIGDIR)/*.pdf.py)
PYPLOTS_PNGS=$(wildcard $(FIGDIR)/*.png.py)
PYPLOTS_PDFS_RENDERED=$(PYPLOTS_PDFS:.pdf.py=.pdf)
PYPLOTS_PNGS_RENDERED=$(PYPLOTS_PNGS:.png.py=.png)

print-%:
	@echo $* = $($*)

all: bare_conf.pdf

$(PYPLOTS_PDFS_RENDERED): %.pdf: %.pdf.py
	$< $@
	pdfcrop $@ $@

$(PYPLOTS_PNGS_RENDERED): %.png: %.png.py
	$< $@
	convert $@ -trim "$@"

bare_conf.pdf: $(TEXFILES) $(PYPLOTS_PDFS_RENDERED) $(PYPLOTS_PNGS_RENDERED)
	pdflatex -draftmode -shell-escape bare_conf.tex
	bibtex bare_conf.aux
	pdflatex -draftmode -shell-escape bare_conf.tex
	pdflatex -shell-escape bare_conf.tex

paper-grayscale.pdf: paper.pdf
	gs -sDEVICE=pdfwrite -sProcessColorModel=DeviceGray \
	   -sColorConversionStrategy=Gray -dOverrideICC \
	   -o "bare_conf-grayscale.pdf" -f "base_conf.pdf"

grayscale: paper-grayscale.pdf

view: bare_conf.pdf
	open bare_conf.pdf

clean:
	rm -fv *.pdf *.aux *.bbl *.blg *.log *.out $(PYPLOTS_PDFS_RENDERED)

clean-all: clean
	rm -fv $(PYPLOTS_PNGS_RENDERED)
