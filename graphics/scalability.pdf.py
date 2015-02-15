#!/usr/bin/env python3
from utils import filename, save2pdf, setup
from utils.plots_helper import sensors 
import matplotlib
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
import itertools

matplotlib.rcParams['text.latex.preamble'] = [r"\usepackage{siunitx}"]

make,fname = filename("scalability.pdf")

# labels: vary train size + algo type
# x: vary test size
# y: runtime in s

trs = [1000,10000,100000]#,2313153]
tes = [100,1000,10000,100000,1000000,2313153]
#es = ["1_gaussian1.5","0.7_mixture1_0.075","0.7_mixture2_0.075"]
es = [
    [1,"gaussian",1.5],
    [0.7,"mixture1",0.075],
    [0.7,"mixture2",0.075]
]
# build data
results = {} 
results2 = {} 

for (tr,te,e) in itertools.product(trs,tes,es):
    if e[1] == "gaussian":
        ofile = "../results/sensors_{}_{}_stat{}_{}{}.out".format(tr,te,*e)
    else:
        ofile = "../results/sensors_{}_{}_stat{}_{}_{}.out".format(tr,te,*e)
    with open(ofile,'r') as f:
        for line in f:
            line = line.strip().split()
            if line[0] == "Runtime:":
                if (e[1],te) not in results2:
                    results2[(e[1],te)] = []
                if (e[1],tr) not in results:
                    results[(e[1],tr)] = []
                results[(e[1],tr)].append(float(line[1]))
                results2[(e[1],te)].append(float(line[1]))
                continue
dfile = "../datasets/real/intel/sensors-1000-dirty.txt"
pdf = PdfPages(fname)
#setup()

ax = pyplot.gca()
ax.set_title("Scalability")
ax.set_xlabel("Test Set Size")
ax.set_ylabel("Runtime (s)")
lines = ["-","--","-."]
linecycler = itertools.cycle(lines)
ax.set_color_cycle(['g','g','g','r','r','r','b','b','b'])
#ax.set_xscale('log')
for (e,tr) in itertools.product(es,trs):
    ax.plot(tes,results[(e[1],tr)],next(linecycler),label = "{}, {}".format(e[1].capitalize(),tr))

ax.legend(loc=2)
save2pdf(pdf)
pdf.close()
