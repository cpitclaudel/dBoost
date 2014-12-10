#!/usr/bin/python
import os,math,sys
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d import Axes3D

def get_data(fname):
  f = open(fname,'r')
  t = []
  h = []
  l = []
  v = []
  for line in f:
    line = line.strip().split()
    t.append(line[0])
    h.append(line[1])
    l.append(line[2])
    v.append(line[3])
  f.close()
  return t,h,l,v

data_base = "../samples/sensors-1000_dataonly.txt"
data_gm = "gaus_plot_data"
data_mm = "gmm_plot_data"


t,h,l,v = get_data(data_base)
fig_gm = plt.figure()
fig_mm = plt.figure()
#fig.set_size_inches(1.8,0.6)
ax = fig_gm.add_subplot(1,1,1)
ax.set_title("Intel Lab Sensor Data")
#ax.set_ylabel("Humidity (%)")
ax.set_ylabel("Temperature (C)")
ax.set_xlabel("Voltage (V)")
ax.scatter(v,t,color='blue')

ax = fig_mm.add_subplot(1,1,1)
ax.set_title("Intel Lab Sensor Data")
#ax.set_ylabel("Humidity (%)")
ax.set_ylabel("Temperature (C)")
ax.set_xlabel("Voltage (V)")
ax.scatter(v,t,color='blue')


t,h,l,v=get_data(data_gm)
ax = fig_gm.add_subplot(1,1,1)
ax.scatter(v,t,color='red')
  
t,h,l,v=get_data(data_mm)
ax = fig_mm.add_subplot(1,1,1)
ax.scatter(v,t,color='red')

pdf = PdfPages("sensors_gm.pdf")
fig_gm.savefig(pdf,format='pdf',transparent= True)
pdf.close()
pdf = PdfPages("sensors_mm.pdf")
fig_mm.savefig(pdf,format='pdf',transparent= True)
pdf.close()

fig_3d = plt.figure()
ax = fig_3d.gca(projection='3d')

t,h,l,v = get_data(data_base)
ax.scatter(v,t,h)

t,h,l,v=get_data(data_mm)
ax.scatter(v,t,h)
ax.set_title("Intel Lab Sensor Data")
ax.set_xlabel("Voltage (V)")
ax.set_ylabel("Temperature (C)")
ax.set_zlabel("Humidity (%)")

pdf = PdfPages("sensors_mm_3d.pdf")
fig_3d.savefig(pdf,format='pdf',transparent= True)
pdf.close()
