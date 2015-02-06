from utils import filename
from utils.plots_helper import lof
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

make,fname = filename("lof-plots.pdf")
dfile = "../datasets/real/intel/sensors-1000-dirty.txt"

pdf = PdfPages(fname)
for k in [2,10]:
    title = "Local Outlier Factor\nk=" + str(k)
    ofile = "../results/k" + str(k) + "data01.out"
    lof(title,dfile,ofile)
    pyplot.savefig(pdf, format = 'pdf', transparent = True)
    pyplot.clf()
pdf.close()
