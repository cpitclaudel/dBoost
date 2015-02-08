import csv
import matplotlib as mpl
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
from utils import TANGO

mpl.rcParams['text.latex.preamble'] = [r"\usepackage{siunitx}"]

LOF_SCALE, BASE_SIZE = 5, 10
MARKER_ALPHA, EDGE_WIDTH, = 1, 0.1

def get_marker_params(color, **kwargs):
    return dict(marker='o', color=TANGO[color][0], edgecolor=TANGO[color][2],
                alpha=MARKER_ALPHA, linewidth=EDGE_WIDTH, **kwargs)
INLIER = get_marker_params('green', s=BASE_SIZE)
OUTLIER = get_marker_params('red')

sensors_schema = [r"Temperature (\si{\degreeCelsius})",r"Humidity (\si{\percent})",r"Light (TODO: Unit)",r"Voltage (\si{\volt})"]

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
    ax.scatter(d[x],d[y],**INLIER)
    ax.scatter(o[x],o[y], s=BASE_SIZE, **OUTLIER)

def lof(title,dfile,ofile):
    d = get_sensor_data(dfile)
    ax = pyplot.gca()
    ax.set_title(title)
    ax.set_xlabel(sensors_schema[1])
    ax.set_ylabel(sensors_schema[0])
    ax.scatter(d[1],d[0],**INLIER)
    with open(ofile,'r') as f:
        rdr = csv.reader(f,delimiter=' ')
        for l in rdr:
            l = [float(x) for x in l]
            if l[0] < 1.5: continue
            ax.scatter(l[2],l[1],s=(l[0]*LOF_SCALE),**OUTLIER)
