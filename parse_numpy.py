from charm_header import *
import re
import numpy as np
import copy

def getOutputfileName(expname, archopt, reg_mode, run_proc):
    outputfile = expname + "_" + archopt + "_" + reg_mode + "_" + str(run_proc)
    outputdir = outputbase + expname + "/"
    return outputdir + outputfile

def parseFromOutputFileNumpy(filename, boolean):
  data = np.genfromtxt(filename, dtype=float, skip_header=header_skip_lines, skip_footer=1)
  return data

titles = ["Size (B)","Size (KiB)","Size (MiB)", "#Number of Iterations","Regular API Oneway Time (us)", "REG Mode - ZC API GET Oneway Time(us)", "PREREG Mode - ZC API GET Oneway Time(us)", "UNREG Mode - ZC API GET Oneway Time(us)", "REG Mode - ZC API PUT Oneway Time(us)", "PREREG Mode - ZC API PUT Oneway Time(us)", "UNREG Mode - ZC API PUT Oneway Time(us)", "Speedup of REG Mode ZC GET over Regular API"]

def printDataArray(data_array):
  i=0
  for title in titles:
    print title + "\t",
  print
  for row in data_array:
    j=0
    for element in row:
      if(j==0 or j==3):
        print str(int(element)) +"\t",
      elif(j==1 or j==2):
        print str(round(float(element),5)) + "\t",
      else:
        print str(round(float(element),2)) + "\t",
      j+=1
    print
    i+=1


def getSpeedup(data_array):
  speedup = data_array[:,2]/data_array[:,3]
  return speedup

def getImprov(data_array):
  improv = 100*((data_array[:,2] - data_array[:,3])/(data_array[:,2]))
  return improv

def getKB(data_array):
  kb = data_array[:,0]/1024
  return kb;

def getMB(data_array):
  mb = data_array[:,0]/1024/1024;
  return mb;


i=0
for archopt in archopts_str:
  j=0
  data_array = np.array([])
  for reg_mode in reg_modes:
    outputfile = getOutputfileName(expname, archopts[i], reg_mode, run_proc);
    data = parseFromOutputFileNumpy(outputfile, True)
    if(j==0):
      data_array = data
    else:
      data_array = np.append(data_array, data[:,3:5], axis=1)
    j+=1

  data_array_copy = np.copy(data_array)

  data_array[:,4]=data_array_copy[:,5]
  data_array[:,5]=data_array_copy[:,7]
  data_array[:,6]=data_array_copy[:,4]
  data_array[:,7]=data_array_copy[:,6]

  speedup = getSpeedup(data_array)
  improv = getImprov(data_array)

  kb = getKB(data_array)
  mb = getMB(data_array)

  print kb

  data_array_modified = np.append(data_array, speedup[:, None], axis=1)
  #data_array_modified = np.append(data_array_modified, improv[:, None], axis=1)

  #printDataArray(data_array_modified)

  data_array_modified = np.hstack((data_array_modified[:,:1], kb[:, None], mb[:, None], data_array_modified[:,1:]))

  printDataArray(data_array_modified)

  #print data_array_modified
  i+=1
