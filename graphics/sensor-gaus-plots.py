from utils import filename
from utils.plots_helper import sensors 
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages

make,fname = filename("sensor-gaus-plots.pdf")
dfile = "../datasets/real/intel/sensors-1000-dirty.txt"

# e, s, y, x
args = [
    (1,2,0,1),
    (1,2,0,2),
    (1,2,0,3),
    (1,2,1,2),
    (1,2,1,3),
    (1,2,2,3),
    (1,2.5,0,1),
    (1,2.5,0,2),
    (1,2.5,0,3),
    (1,2.5,1,2),
    (1,2.5,1,3),
    (1,2.5,2,3)]

pdf = PdfPages(fname)
for (e,s,y,x) in args:
    title = "Outliers in Sensor Data\nGaussian, stddev=" + str(s)
    ofile = "../results/sensors_dirty_stat" + str(e) + "_gaus" + str(s) + ".out"
    sensors(title,x,y,dfile,ofile)
    pyplot.savefig(pdf, format = 'pdf', transparent = True)
    pyplot.clf()
pdf.close()
