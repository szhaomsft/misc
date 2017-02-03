#preprocess MT corpus 
import math
import subprocess
import os.path
import string
import sys
import codecs
import glob
from random import random


t = random()

from re import compile as _Re

_unicode_chr_splitter = _Re( '(?s)((?:[\ud800-\udbff][\udc00-\udfff])|.)' ).split
def split_unicode_chrs( text ):
  return [ chr for chr in _unicode_chr_splitter( text ) if chr ]

characters = (
    '\u3007'         # Ideographic number zero, see issue #17
    '\u4E00-\u9FFF'  # CJK Unified Ideographs
    '\u3400-\u4DBF'  # CJK Unified Ideographs Extension A
    '\uF900-\uFAFF'  # CJK Compatibility Ideographs
)


def IsChinese(chr):
    if (chr > u'\u4e00' and chr < u'\u9fff') or  (chr > u'\u3400' and chr < u'\u4DBF') or  (chr > u'\uF900' and chr < u'\uFAFF') or (chr == '\u3007'):
        return True
    return False

def Join(list):
    line = ""
    pc = 0
    i = 0
    for c in list:
        if i > 0:
            if IsChinese(c):
               line = line + " "
            elif IsChinese(pc):
               line = line + " "        
        i = i + 1
        line = line + c     
        pc = c

    if len(line) == 0:
        print("error, empty line:" + str(list))
    return line

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
        if t > 0.002:
            trainf.write(arr[i])
            trainf1.write(arr1[i])
        elif t > 0.001:
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

def SplitCorpus(file, outFile, src, tgt):
    f = codecs.open(file, 'r', 'UTF-8')
    sf = codecs.open(outFile + "." + src, 'w', 'utf-8')
    tf = codecs.open(outFile + "." + tgt, 'w', 'utf-8')
    i = 0
    for line in f:
        #if i > 100:
        #    break
        if i % 2 == 0:
            sf.write(line)
        else:
            chrlist = split_unicode_chrs(line)
            line = Join(chrlist)
            tf.write(line)
        i = i + 1    
    
    sf.close()
    tf.close()
    f.close()   

    #split into train, dev, test
    SplitIntoThree(outFile + "." + src, outFile + "." + tgt);

#function to merge the corpus files
def MergeFiles(patten, outFile):
    files = [file for file in glob.glob(patten, recursive=True)]
    of = codecs.open(outFile, 'w', 'utf-8')
    print("merging into " + outFile)
    for f in files:
        f = codecs.open(f, 'r', 'UTF-8')
        for line in f:
            of.write(line)
        f.close()    
    of.close();

#main logic
#print(len(characters))
#print(characters[1])
#print('\u6000' in characters)

if (len(sys.argv) >= 2):
    sourcePath = sys.argv[1]


files = [file for file in glob.glob(sourcePath + '/**/*.txt', recursive=True)]

outFolder = "./"

#SplitCorpus("C:/github/MT/parallel-umcorpus-v1/UM-Corpus/data/Bilingual/Laws/Bi-Laws.txt", "./Bi-Laws.txt", "en-US", "zh-CN")

for file in files:
    print("processing " + file)
    head, filename = os.path.split(file)
    outFile = outFolder + filename;
    SplitCorpus(file, outFile, "en-US", "zh-CN")

MergeFiles(outFolder + "/*.en-US.train", "en-US.train.txt")
MergeFiles(outFolder + "/*.en-US.dev", "en-US.dev.txt")
MergeFiles(outFolder + "/*.en-US.test", "en-US.test.txt")

MergeFiles(outFolder + "/*.zh-CN.train", "zh-CN.train.txt")
MergeFiles(outFolder + "/*.zh-CN.dev", "zh-CN.dev.txt")
MergeFiles(outFolder + "/*.zh-CN.test", "zh-CN.test.txt")
