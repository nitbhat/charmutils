import re
import sys
import os

suffix=".frontera.tacc.utexas.edu"

def getThreeDigitFormat(num):
  numStr = str(num)
  newNumStr = ""
  numZeros = 3 - len(numStr)
  #print "numzero is "+ str(numZeros)
  if(numZeros < 0):
    sys.exit("4 digit number here!")
  i=1
  while(i <= numZeros):
    newNumStr += "0";
    i += 1
  newNumStr += numStr
  return newNumStr

def getLongMachName(base, string):
  return base + "-" + string + suffix

def getSeparateList(base, nodelist):
  list3=[]
  list4 = nodelist.split(",")
  for val in list4:
    #print "val: " + val
    if(val == ""):
      continue
    list5 = val.split("-")
    #print list5
    if(len(list5) == 1):
      #print "1 sized list" + str(list5)
      num1  = int(list5[0])
      #print "number is " + str(num1)
      #print "base is " + base + " string is "+ str(num1)
      final = getLongMachName(base, getThreeDigitFormat(str(num1)))
      #print "final string is " + final
      finalList.append(final)
      #list3.append(final)
    elif(len(list5) == 2): #range
      #print "range list" + str(list5)
      num1  = int(list5[0])
      num2  = int(list5[1])
      #print "number is " + str(num1) + " and second number is " + str(num2)
      #print "Item 1 is "+list5[1] + " and item 2 is "+list5[2]
      for x in range(num1,num2 + 1):
        #print "base is " + base + " string is "+ str(x)
        final = getLongMachName(base, getThreeDigitFormat(str(x)))
        #print "final string is " + final
        finalList.append(final)
        #list3.append(final)
    else:
      sys.exit("Incorrect parsing in getSeparate list, cannot have size>2")
  return list3


n=len(sys.argv)

if(n < 2):
  sys.exit("Too few arguments! Pass the nodelist which you want to split");
elif(n > 2):
  sys.exit("Too many arguments! Pass the nodelist which you want to split");
else:
  nodes=sys.argv[1]


finalList=[]
#pattern = "c\d+-\[?[\d,]+\]?"
pattern = "c[\[\],\d-]+"
#nodes = "c108-[053,121],c109-[053,163,193],c110-123,c111-174,c117-191,c119-181,c120-[063,091,123,133],c122-[043,072,153]"
#nodes = "c45-001,c67-009,c67-878,c87-[078-080]"
#nodes = "c45[,c78,c78,c76[,c70-[078-080]"

nodelist = re.findall(pattern, nodes)
#print "nodelist is " + str(nodelist)
#print nodelist

for nodeStr in nodelist:
  #print "Node str is " + nodeStr
  pattern1 = "^(c\d+)-\[?([-,\d]+)\]?"
  regex1 = re.compile(pattern1)
  m1 = regex1.search(nodeStr)
  if m1:
    #print "match one is " + m1.group(1)
    #print "match two is " + m1.group(2)
    getSeparateList(m1.group(1), m1.group(2))
  else:
    print "no match"



#print "computed finalList of size :"+ str(len(finalList))
#print finalList

for i in finalList:
  print i+";",

#reSetOfNodes= "(\w+)-(\[[-,\w]+\])"
#getSeparateList("c161","002-004,011-014,021-024,031-034,041")
#c108-[053,121],c109-[053,163,193],c110-123,c111-174,c117-191,c119-181,c120-[063,091,123,133],c122-[043,072,153]
#list1 = nodes.split("c")
#print list1

#print "jobid is" + jobid
#jobQuery = "squeue -j "+ jobid + " -h -o %N"

#nodelist = os.system(jobQuery)

#print "nodelist is " + nodelist

#reSetOfNodes= "(\w+)-(\[[-,\w]+\])"
#p1 = reSetOfNodes.compile(reSetOfNodes)
#
#nodes="c161-[002-004,011-014,021-024,031-034,041],c787-[323]"
#list1 = nodes.split(,)
#
#for list2 in list1:
#  print "Set of Nodes:" + list2
#  m1 = p1.search(list2)
#  if(m1):
#    list3 = getSeparateList(m.group(1), m.group(2));
#
#
#
#getSeparateList(nodes)
#
#
#
#
#
#
#m = p.search(nodes)
#
#
#print "match is m"
#
#print "match one is " + m.group(1)
#print "match two is " + m.group(2)

#list3  = getSeparateList("c161","002-004,011-014,021-024,031-034,041")
#print list3
