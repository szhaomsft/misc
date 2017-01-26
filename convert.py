import math
import subprocess
import os.path
import string
import sys

print('Number of arguments:', len(sys.argv), 'arguments.')
print('Argument List:', str(sys.argv))

iMin = 5
iMax = 10
jMin = 5
jMax = 10

if (len(sys.argv) >= 2):
    sourcePath = sys.argv[1]
else:
    print("need to specify source wave folder")
    sys.exit(-1)

if (len(sys.argv) >= 6): 
    iMin = int(sys.argv[2])
    iMax = int(sys.argv[3])
    jMin = int(sys.argv[4])
    jMax = int(sys.argv[5])
    print(iMin, iMax, jMin, jMax)

    

program='C:/github/misc/convert.exe'
for i in range(iMin, iMax):
    for j in range(jMin, jMax):
        for filename in os.listdir(sourcePath):
            newpath = sourcePath + '-' + str(i) + '-' + str(j)
            if not os.path.exists(newpath):
                os.makedirs(newpath)
            arguments=(sourcePath + '/' + filename, newpath + '/' + filename, str(i/10.0), str(j/10.0))
            cmd = program + ' ' + " ".join(arguments)
            print(cmd)
            subprocess.check_output(cmd, shell=True)


#convert.exe still bugger, seems to crash when i = 1, j = 1