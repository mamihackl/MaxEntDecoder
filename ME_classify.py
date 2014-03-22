#!/opt/python-2.6/bin/python2.6
# Mami Hackl and Nat Byington
# # LING 572 HW5 MaxEnt classifier
# Classify test data using a MaxEnt model learned from training data
# Args: test data, model file, system output > accuracy file

import sys
import re
import math

# Open file names from arguments.
test = open(sys.argv[1])
model_file = open(sys.argv[2])
SYS_OUT = open(sys.argv[3], 'w')

# Read model_file into the model hash.
model = {} # contains weight values for (term, class) keys
classes = set() # the set of all classes from model file
terms = set() # the set of all terms from model file
current_class = ''
class_re = re.compile(r'^FEATURES FOR CLASS ([\S]+)')
term_re = re.compile(r'^ ([\S]+) ([\S]+)')
for line in model_file.readlines():
    if class_re.match(line):
        current_class = class_re.match(line).group(1)
        classes.add(current_class)
    elif term_re.match(line):
        term = term_re.match(line).group(1)
        weight = float(term_re.match(line).group(2))
        terms.add(term)
        model[(term, current_class)] = weight

# Initialize confusion matrix.
MATRIX = dict( [(x, {}) for x in classes] )
for c in classes:
    for c2 in classes:
        MATRIX[c][c2] = 0

# Classify each vector in test data.
v_count = 0
for vector in test.readlines():
    Z = 0.0
    v_count += 1
    result = {}
    results_list = []
    instance, true_class = re.match(r'^([\S]+) ([\S]+) ', vector).group(1,2)
    terms = re.findall(r'([A-Za-z]+) ([0-9]+)', vector) # (term, count) in vector
    for c in classes:
        summ = model[('<default>', c)]
        for t in terms:
            summ += int(t[1]) * model[(t[0], c)]
        result[c] = math.exp(summ)
        Z += result[c]
    for c in classes:
        results_list.append(((result[c] / Z), c)) # (prob, class)
    results_list.sort(reverse=True) # find highest prob 
    assigned_class = results_list[0][1]
    MATRIX[true_class][assigned_class] += 1
    # output to sys_out
    out = instance + ' ' + true_class
    for i in results_list:
        out += ' ' + i[1] + ' ' + str(i[0])
    SYS_OUT.write(out + '\n')

# Output accuracy results using MATRIX data
sys.stdout.write('class_num=' + str(len(classes)) + ' feat_num=' + str(len(terms)) + '\n')
correct = 0.0
print 'Confusion matrix for Testing Data:'
print 'row is the truth, column is the system output'
print ''
sys.stdout.write('\t\t')
for c in classes:
    sys.stdout.write(' ' + c)
    correct += MATRIX[c][c]
sys.stdout.write('\n')
for c in classes:
    sys.stdout.write(c)
    for c2 in classes:
        sys.stdout.write(' ' + str(MATRIX[c][c2]))
    sys.stdout.write('\n')
print ''
print 'Test accuracy: ' + str(correct / float(v_count))
print ''

