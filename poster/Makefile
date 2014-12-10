all: master.pdf

../graphics/models-plots.pdf:
	cd ../graphics/ && python3 models-plots.py

../graphics/models-plots-crop.pdf: ../graphics/models-plots.pdf
	cd ../graphics/ && pdfcrop models-plots.pdf

master.pdf: master.tex ../graphics/models-plots-crop.pdf
	pdflatex master.tex
