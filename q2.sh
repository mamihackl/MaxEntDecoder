#!/bin/bash
#Ling572 HW5 Q2 MaxEnt classifier 
#Nat Byington
#Mami Hackl
command='./ME_classify.py'
path='/opt/dropbox/09-10/572/hw5/examples/'
testf='test2.vectors.txt'
outputf='output_q2'
accf='acc_q2'
modelf='mallet_model_q1.txt'
$command $path$testf $modelf $outputf > $accf 

