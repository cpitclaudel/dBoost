import csv
import matplotlib as mpl
from matplotlib import pyplot, mlab
from mpl_toolkits.mplot3d import Axes3D
from utils import TANGO

mpl.rc('text', usetex=True)
mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['text.latex.preamble']=[r"\usepackage{amsmath,amssymb,calc}\usepackage{pifont}\newcommand{\cmark}{\ding{51}}\newcommand{\xmark}{\ding{55}}"]

sensors_schema = ["Temperature (C)","Humidity ($\%$)","Light","Voltage (V)"]

def get_sensor_data(fname):
    d = [[],[],[],[]]
    with open(fname,'r') as f:
        for line in f:
            line = line.strip().split()
            for i in range(len(line)):
                d[i].append(float(line[i]))
    return d

def get_outliers_by_index(fname):
    d = []
    with open(fname,'r') as f:
        for line in f:
            line = line.strip()
            d.append(int(line))
    return d

def sensors(title,x,y,dfile,ofile):
    d = get_sensor_data(dfile)
    outliers = get_outliers_by_index(ofile)
    ax = pyplot.gca()
    ax.set_title(title)
    ax.set_ylabel(sensors_schema[y])
    ax.set_xlabel(sensors_schema[x])
    o = [[],[],[],[]]
    for l in range(len(d[y])):
        if l in outliers:
            o[y].append(d[y][l])
            o[x].append(d[x][l])
    ax.scatter(d[x],d[y],color=TANGO["grey"][1],marker="o",alpha = 1)
    ax.scatter(o[x],o[y],color=TANGO["black"][2],marker="o")

def lof(title,dfile,ofile):
    d = get_sensor_data(dfile)
    ax = pyplot.gca()
    ax.set_title(title)
    ax.set_xlabel(sensors_schema[1])
    ax.set_ylabel(sensors_schema[0])
    ax.scatter(d[1],d[0],marker='o',color=TANGO["grey"][1],alpha = 1)
    with open(ofile,'r') as f:
        rdr = csv.reader(f,delimiter=' ')
        for l in rdr:
            l = [float(x) for x in l]
            if l[0] < 1.5: continue
            ax.scatter(l[2],l[1],marker='o',color=TANGO["black"][2],s=(l[0]*10))

