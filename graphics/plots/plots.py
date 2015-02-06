import os,math,sys,types
import csv
from bisect import bisect_left
import matplotlib as mpl
from matplotlib import pyplot, mlab
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from  utils import filename, TANGO

sensors_dpath = "../../datasets/real/intel/"
sensors_opath = "../../results/intel/"
dfile = "sensors-1000-dirty.txt"
ofile = "sensors_dirty_"

sensors_schema = ["Temperature (C)","Humidity","Light","Voltage"]
sensors_title = "Intel Sensors "
mpl.rcParams['lines.linewidth'] = 2

def gaussian(x, mu, sigma):
    return mlab.normpdf(x, mu, sigma)

def cleanup_2d(ax):
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    pyplot.tight_layout()

def gaussian_plt():
    pyplot.clf()

    x = np.linspace(-10, 10, num = 200)
    y = gaussian(x, 0, 1)

    NDEV = 1.5
    nlo = bisect_left(x, -NDEV)
    nhi = bisect_left(x, +NDEV)

    xlo, ylo = x[:nlo], y[:nlo]
    xmi, ymi = x[nlo-1:nhi+1], y[nlo-1:nhi+1]
    xhi, yhi = x[nhi:], y[nhi:]

    ax = pyplot.axes(frameon = False)
    ax.set_xlim((-5,5))

    pyplot.plot(xmi, ymi, color = TANGO["green"][2])
    pyplot.fill_between(xmi, 0, ymi, color = TANGO["green"][1])
    for (xx, yy) in ((xlo, ylo), (xhi, yhi)):
        pyplot.plot(xx, yy, color = TANGO["red"][1])
        pyplot.fill_between(xx, 0, yy, color = TANGO["red"][0])
    #pyplot.axhline(y = y[nlo-1], color = TANGO["red"][2], linestyle = '--', linewidth = 1)

    cleanup_2d(ax)

def mixture_plt():
    from utils._multivariate import multivariate_normal
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm

    centers = ([0.5, 1.5], [-1, -2], [2, -1])
    covs = ([[1.2, 2],[0.7, 1]], [[0.75, 0.6],[0.6, 0.75]], [[2, 0],[0, 2]])
    coeffs = (1,1,1)

    fig = pyplot.figure()
    ax = fig.gca(projection='3d')

    RES = 500
    x = np.linspace(-5, 5, num = RES)
    y = np.linspace(-5, 5, num = RES)

    x, y = np.meshgrid(x, y)
    pos = np.empty(x.shape + (2,))
    pos[:, :, 0] = x; pos[:, :, 1] = y

    gaussians = (multivariate_normal(*param) for param in zip(centers, covs))
    z = sum(c * P for c, P in zip(coeffs, (g.pdf(pos) for g in gaussians)))

    from matplotlib import colors
    RED, GREEN = 0, 120
    HUES = (RED, GREEN)
    THRESHOLD = 0.1

    cmap_hsv = [(HUES[pos > THRESHOLD * 255] / 360,
                           0.25 + 0.75 * (pos / 255),
                           1 - 0.75 * (pos / 255))
                for pos in range(255)]
    cmap_rgb = colors.ListedColormap(colors.hsv_to_rgb(np.array([cmap_hsv]))[0])

    WHITE = (1, 1, 1, 0.05)
    ax.plot_surface(x, y, z, rstride = 5, cstride = 5, edgecolor = WHITE,
                    cmap = cmap_rgb, linewidth = 1, shade = True)
    ax.plot_wireframe(x, y, z, rstride = 5, cstride = 5, edgecolor = WHITE,
                      linewidth = 1)

    ax.dist = 7.5
    ax.elev = 20
    ax.set_axis_off()

def histogram_plt():
    y = [0.1, 1, 5, 6, 0.2, 1, 10, 8, 0]
    x = np.linspace(0, 8, num = 9)
    T = 0.5

    FILLS   = (TANGO["red"][0], TANGO["green"][1])
    STROKES = (TANGO["red"][1], TANGO["green"][2])
    colors = [FILLS[yy > T] for yy in y]
    edgecolors = [STROKES[yy > T] for yy in y]

    pyplot.clf()
    pyplot.bar(x, y, width=1)

    ax = pyplot.axes(frameon = False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    ax.set_xlim(-1, 10)

    pyplot.bar(x, y, width = 1, color = colors, edgecolor = edgecolors, linewidth = 2)
    pyplot.tight_layout()

def get_data(fname):
  f = open(fname,'r')
  d = [[],[],[],[]]
  for line in f:
    line = line.strip().split()
    for i in range(len(line)):
      d[i].append(float(line[i]))
  f.close()
  return d

def get_outliers(fname):
  f = open(fname,'r')
  d = []
  for line in f:
    line = line.strip()
    d.append(int(line))
  f.close()
  return d

def sensors(args):
  e,p,t,y,x = args[1:6]
  data = sensors_dpath + dfile
  d = get_data(data)
  ofile_ = ofile + "stat" + str(e) + "_mix"+str(p) + "_" + str(t) + ".out"
  outliers = get_outliers(sensors_opath + ofile_)
  ax = pyplot.gca()
  title = "Gaussian" if p == 1 else "Mixture"
  ax.set_title(title + "\n" + sensors_schema[x] + " vs. " + sensors_schema[y])# + "\n" + str(e) + " " + str(t) + " " + str(p))
  ax.set_ylabel(sensors_schema[y])
  ax.set_xlabel(sensors_schema[x])
  o = [[],[],[],[]]
  for l in range(len(d[y])):
    if l in outliers:
      o[y].append(d[y][l])
      o[x].append(d[x][l])
  ax.scatter(d[x],d[y],color='yellow',marker="x",alpha = 1)
  ax.scatter(o[x],o[y],color='red',marker="o")

def lof(args):
  k = args[1]
  data = sensors_dpath + dfile
  d = get_data(data)
  ofile_ = "k" + str(k) + "data01.out" 
  ax = pyplot.gca()
  ax.set_title("Local Outlier Factor k=" + str(k) + "\n" + str(sensors_schema[1]) + " vs. " + str(sensors_schema[0]))
  ax.set_xlabel(sensors_schema[1])
  ax.set_ylabel(sensors_schema[0])
  ax.scatter(d[1],d[0],marker='x',color='yellow',alpha = 1)
  with open(sensors_opath + ofile_,'r') as f:
    rdr = csv.reader(f,delimiter=' ')
    for l in rdr:
      l = [float(x) for x in l]
      if l[0] < 1.5: continue
      ax.scatter(l[2],l[1],marker='o',color='red',s=(l[0]*10))

def tostring(arg):
  if isinstance(arg,types.FunctionType):
    return arg.__name__
  return str(arg)

# Add the name of your plotting function here
plots = [
  (sensors,0,1,0.005,0,1),
  (sensors,0,1,0.005,0,3),
  (sensors,0.7,1,0.05,0,1),
  (sensors,0.7,1,0.05,0,3),
  (sensors,0.7,2,0.25,0,1),
  (sensors,0.7,2,0.25,0,3),
  (lof,2),
  (lof,10)]

#batch_mode, fname = filename("models-plots.pdf")

#if batch_mode:
fname = "models-plots.pdf"
pdf = PdfPages(fname)

for plotter in (gaussian_plt, mixture_plt, histogram_plt):
    plotter()
    pyplot.savefig(pdf, format = 'pdf', transparent = True)

pdf.close()

# Plot each graph
pyplot.figure()
for id, plotter in enumerate(plots):
    name = "_".join((tostring(x).replace('.','-') for x in plotter))
    print("Plotting", id+1,"/",len(plots),": ",name)
    pdf = PdfPages(name + ".pdf")
    plotter[0](plotter)
    pyplot.savefig(pdf, format = 'pdf', transparent = True)
    pdf.close()
    pyplot.clf()


