#preprocess MT corpus 
import math
import subprocess
import os.path
import string
import sys
import codecs
import glob
from random import random


#function to preprocess corpus line by line into source and target
def SplitIntoThree(file, file1):
    sf = codecs.open(file, 'r', 'UTF-8')
    tf = codecs.open(file1, 'r', 'UTF-8')
    arr = sf.readlines()
    arr1 = tf.readlines()
    if len(arr) != len(arr1):
        print("error, no same lines")
    trainf = codecs.open(file + ".train", 'w', 'utf-8')
    devf = codecs.open(file + ".dev", 'w', 'utf-8')
    testf = codecs.open(file + ".test", 'w', 'utf-8')

    trainf1 = codecs.open(file1 + ".train", 'w', 'utf-8')
    devf1 = codecs.open(file1 + ".dev", 'w', 'utf-8')
    testf1 = codecs.open(file1 + ".test", 'w', 'utf-8')
    for i in range(0, len(arr)):
        t = random()
        if t > 0.06:
            trainf.write(arr[i])
            trainf1.write(arr1[i])
        elif t > 0.03:
            devf.write(arr[i])
            devf1.write(arr1[i])
        else:
            testf.write(arr[i])
            testf1.write(arr1[i])
    trainf.close()
    devf.close()
    testf.close()
    trainf1.close()
    devf1.close()
    testf1.close()
    sf.close()    
    tf.close()    


#function to merge the corpus files
def MergeFiles(basefile, domainfile, n,  outFile):
    files = [basefile]
    for i in range(0, n):
        files.append(domainfile)
    of = codecs.open(outFile, 'w', 'utf-8')
    print("merging into " + outFile)
    for f in files:
        f = codecs.open(f, 'r', 'UTF-8')
        for line in f:
            of.write(line)
        f.close()    
    of.close();


# C:\Users\szhao\Desktop\NMT\Office

rootpath="C:/Users/szhao/Desktop/NMT/"

SplitIntoThree(rootpath + "Office/enus.txt", rootpath + "Office/zhcn.txt")

MergeFiles(rootpath + "en-US.train.txt", rootpath + "Office/enus.txt.train", 10,  rootpath + "en-US.train.office.txt")
MergeFiles(rootpath + "en-US.dev.txt", rootpath + "Office/enus.txt.dev", 2,  rootpath + "en-US.dev.office.txt")
MergeFiles(rootpath + "Office/enus.txt.test", "", 0,  rootpath + "en-US.test.office.txt")


MergeFiles(rootpath + "zh-CN.train.txt", rootpath + "Office/zhcn.txt.train", 10,  rootpath + "zh-CN.train.office.txt")
MergeFiles(rootpath + "zh-CN.dev.txt", rootpath + "Office/zhcn.txt.dev", 2,  rootpath + "zh-CN.dev.office.txt")
MergeFiles(rootpath + "Office/zhcn.txt.test", "", 0,  rootpath + "zh-CN.test.office.txt")
