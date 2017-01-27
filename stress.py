import math
import subprocess
import os.path
import string
import sys


if (len(sys.argv) >= 3):
    exePath = sys.argv[1]
    sourcePath = sys.argv[2]
else:
    print("need to specify source wave folder")
    sys.exit(-1)

if not os.path.exists("tmp/"):
    os.makedirs("tmp/")
program=exePath
for filename in os.listdir(sourcePath):
    arguments=(sourcePath + '/' + filename, "tmp/t.wav", "1", "1")
    cmd = program + ' ' + " ".join(arguments)
    print(cmd)
    subprocess.check_output(cmd, shell=True)

#convert.exe still bugger, seems to crash when i = 1, j = 1