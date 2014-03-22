#!/usr/bin/env python2.6
#Mami Hackl
#Nat Byington
#572 hw5: model expectation 

import sys,re,math

MODEL = 0

class Struct:

    # default constructor
    def __init__(self):
       self.instance = ''
       self.cls = ''
       self.feat_dict = {}


#######################
# sort features
def sort_data(data):

   table_list = []
   class_dict = {}
     
   #read data line by line
   lines = data.split('\n')
   for l in lines:
       if not l:break
       newl = re.match('^(\S+) (\S+)', l)
       table = Struct()
       table.instance = newl.group(1)
       class_name = newl.group(2)
       table.cls = class_name 
       f_list = re.findall('(\w+) (\d+)', l)
       for t,c in f_list:
           c = int(c)
           if t not in table.feat_dict:
              table.feat_dict[t] = c    
           else:
              table.feat_dict[t] = table.feat_dict.get(t,0) + c
           if class_name not in class_dict:
              class_dict[class_name] = dict([(t,c)])
           else:
              class_dict[class_name][t] = class_dict[class_name].get(t,0) + c
       table_list.append(table)

   return table_list,class_dict,len(lines) - 1
    

#######################
#process model file 
def process_modelf(prob_dict,modelf):

    # calculate P(y|x) using model info
    model = {}
    current_class = ''
    class_re = re.compile(r'^FEATURES FOR CLASS ([\S]+)')
    term_re = re.compile(r'^ ([\S]+) ([\S]+)')
    for line in modelf.readlines():
        if class_re.match(line):
            current_class = class_re.match(line).group(1)
        elif term_re.match(line):
            term = term_re.match(line).group(1)
            weight = float(term_re.match(line).group(2))
            model[(term, current_class)] = weight

    for table in table_list:
       Z = 0.0 
       result = {}
       for c in class_dict.keys():
           sum = model[('<default>',c)] 
           for feat,val in table.feat_dict.items():
               sum += val * model[(feat,c)] 
           result[c] = math.exp(sum)
           Z += result[c]
       for c in class_dict.keys():
           prob_dict[(c,table.instance)] = result[c]/float(Z)

    return prob_dict


#######################
#calculate probabilities 
def calculate(table_list,class_dict,prob_dict,N):

  model_expect = {}
  for table in table_list:
     for feat,val in table.feat_dict.items():
        for c in class_dict.keys():
             if MODEL:
                prob = prob_dict[(c,table.instance)] 
             else:
                prob = 1/float(len(class_dict))
             val = 1/float(N) * prob
             if c not in model_expect:      
                model_expect[c] = dict([(feat,val)])
             else:
                model_expect[c][feat] = model_expect[c].get(feat,0) + val

  return model_expect            


#######################
# output
def output(class_dict,model_expect):

    for c,list in class_dict.items():
       for feat,val in list.items():
           val = model_expect[c].get(feat,0)   
           if val > 0:
              outf.write("%s %20s %5.15f\n" % (c,feat,val))


#######################
#main function 

#open files
trainf = open(sys.argv[1],'r')
outf = open(sys.argv[2],'w')

#sort training data
data = trainf.read() 
table_list,class_dict,N = sort_data(data)

#calculate probabilities
prob_dict = {}
if len(sys.argv) == 4:
   MODEL = 1
   modelf = open(sys.argv[3],'r')
   prob_dict=process_modelf(prob_dict,modelf)

model_expect = calculate(table_list,class_dict,prob_dict,N)

#calculate expectation
output(class_dict,model_expect)

#close file handlers
trainf.close()
outf.close()
if MODEL:
   modelf.close()
