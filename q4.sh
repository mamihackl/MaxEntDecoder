#!/bin/bash
#Ling572 HW5 model expectation
#Nat Byington
#Mami Hackl
command='./calc_model_exp.py'
path='/opt/dropbox/09-10/572/hw5/examples/'
trainf='train2.vectors.txt'
outputf='output_q4'
modelf='mallet_model_q1.txt'
$command $path$trainf $outputf $modelf
#$command $path$trainf $outputf 
