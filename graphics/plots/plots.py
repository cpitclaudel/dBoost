import os,math,sys
from bisect import bisect_left
import matplotlib as mpl
from matplotlib import pyplot, mlab
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

mpl.rcParams['lines.linewidth'] = 2

TANGO = {"yellow": ("#fce94f", "#edd400", "#c4a000"),
         "orange": ("#fcaf3e", "#f57900", "#ce5c00"),
         "brown": ("#e9b96e", "#c17d11", "#8f5902"),
         "green": ("#8ae234", "#73d216", "#4e9a06"),
         "blue": ("#729fcf", "#3465a4", "#204a87"),
         "purple": ("#ad7fa8", "#75507b", "#5c3566"),
         "red": ("#ef2929", "#cc0000", "#a40000"),
         "grey": ("#eeeeec", "#d3d7cf", "#babdb6"),
         "black": ("#888a85", "#555753", "#2e3436")}

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
    from _multivariate import multivariate_normal
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
  t,h,l,v = [],[],[],[]
  for line in f:
    line = line.strip().split()
    t.append(float(line[0]))
    h.append(float(line[1]))
    l.append(float(line[2]))
    v.append(float(line[3]))
  f.close()
  return t,h,l,v


def sensors_gm():
  data_base = "../../samples/sensors-1000_dataonly.txt"
  data = "../../samples/gaus_plot_data"
  t,h,l,v = get_data(data_base)
  fig = pyplot.figure()
  ax = fig.add_subplot(1,1,1)
  ax.set_title("Intel Lab Sensor Data")
  ax.set_ylabel("Temperature (C)")
  ax.set_xlabel("Voltage (V)")
  ax.scatter(v,t,color='blue')
  t,h,l,v=get_data(data)
  ax = fig.add_subplot(1,1,1)
  ax.scatter(v,t,color='red')

def sensors_mm():
  data_base = "../../samples/sensors-1000_dataonly.txt"
  data = "../../samples/gmm_plot_data"
  t,h,l,v = get_data(data_base)
  fig = pyplot.figure()
  ax = fig.add_subplot(1,1,1)
  ax.set_title("Intel Lab Sensor Data")
  ax.set_ylabel("Temperature (C)")
  ax.set_xlabel("Voltage (V)")
  ax.scatter(v,t,color='yellow')
  t,h,l,v=get_data(data)
  ax = fig.add_subplot(1,1,1)
  ax.scatter(v,t,color='red')


# Add the name of your plotting function here
plots = (sensors_gm,sensors_mm)
#plots = (gaussian_plt, mixture_plt, histogram_plt,sensors_gm,sensors_mm)

# Plot each graph
for id, plotter in enumerate(plots):
    print("Plotting", id+1)
    pdf = PdfPages(plotter.__name__ + ".pdf")
    plotter()
    pyplot.savefig(pdf, format = 'pdf', transparent = True)
    pdf.close()


