from charm_header import *
import re

def getOutputfileName(expname, archopt, reg_mode, run_proc):
    outputfile = expname + "_" + archopt + "_" + reg_mode + "_" + str(run_proc)
    outputdir = outputbase + expname + "/"
    return outputdir + outputfile

megalist=[]
megalistDup=[]

#1024			1000			2.563477			10.583997			11.309028
p = re.compile("(\d+)\s+(\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)")
def parseFromOutputFile(filename, boolean):
  if os.path.exists(filename):
    print "exists"
    reglist=[]
    getgetlist=[]
    putputlist=[]
    iteralist=[]
    sizelist=[]

    sizelist.append("Size")
    iteralist.append("Number of Iterations")
    reglist.append("Regular API messaging")
    getgetlist.append("Get Get Pinpong")
    putputlist.append("Put Put Pingpong")

    lines = open(filename, "r");
    for line in lines:
      m = p.search(line)
      if m:
        size = float(m.group(1))
        itera = float(m.group(2))
        reg = float(m.group(3))
        getget = float(m.group(4))
        putput = float(m.group(5))

        sizelist.append(size)
        getgetlist.append(getget)
        putputlist.append(putput)
        iteralist.append(itera)
        reglist.append(reg)

    if(boolean):
      numrows = len(reglist)
      print "numrows is "+ str(numrows)
      megalist.append(sizelist)
      megalist.append(iteralist)
      megalist.append(reglist)

    megalist.append(getgetlist)
    megalist.append(putputlist)

    if(boolean):
      return numrows

def printMegaList(biglist, numrows):
  for j in range(numrows):
    #print j
    for sublist in biglist:
      print str(sublist[j]) + ",",
    print
    #print "========="


def modifyMegaList(numrows):
  megalist[4] = megalistDup[5]
  megalist[5] = megalistDup[7]
  megalist[6] = megalistDup[4]
  megalist[7] = megalistDup[6]


i=0
for archopt in archopts_str:
  boolean = True
  if(i==0):
    for reg_mode in reg_modes:
      outputfile = getOutputfileName(expname, archopts[i], reg_mode, run_proc);
      print outputfile
      if(boolean):
        numrows = parseFromOutputFile(outputfile, True)
        boolean = False
      else:
        parseFromOutputFile(outputfile, False)
  i+= 1

megalistDup = list(megalist)
printMegaList(megalist, numrows)
print "megalist print done"
modifyMegaList(numrows)
printMegaList(megalist, numrows)
print "megalist numcols is" + str(len(megalist)) + " and numrows is "+ str(numrows)



