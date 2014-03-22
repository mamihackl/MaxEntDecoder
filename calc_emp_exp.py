#!/usr/bin/env python2.6
#Mami Hackl
#Nat Byington
#572 hw5: emipirical expectation 

import sys,re


# sort features
def sort_data(data):
    
   class_dict = {} 
    
   #read data line by line
   lines = data.split('\n')
   for l in lines:
       if not l:break
       class_name = re.match('^(\S+) (\S+)', l).group(2)  
       f_list = re.findall('(\w+) (\d+)', l)
       for t,c in f_list:
           c = int(c)
           if class_name not in class_dict: 
              class_dict[class_name] = dict([(t,c)])
           else:
              class_dict[class_name][t] = class_dict[class_name].get(t,0) + c 

   return class_dict,len(lines) - 1
    

# calculate empirical expectation
def calculate(class_dict,N):
 
   for c,list in class_dict.items():
       for feat,val in list.items():
           outf.write("%s %20s %5.15f\n" % (c,feat,val/float(N)))

#######################
#main function 

#open files
trainf = open(sys.argv[1],'r')
outf = open(sys.argv[2],'w')

#sort training data
data = trainf.read() 
class_dict,N = sort_data(data)

#calculate expectation
calculate(class_dict,N)

#close file handlers
trainf.close()
outf.close()
