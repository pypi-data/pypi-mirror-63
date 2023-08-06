'''
Created on Feb 24, 2020

@author: hammonds
'''
import os
from minixs.calibrate import Calibration

projectDir = "/Users/hammonds/Downloads/miniXESdata/FromInhui/Co3O4"

scanFile = os.path.join(projectDir, "Co3O4cali.0001")
camera = "pilatus"
crystals = []
for i in list(range(1, 26)):
    try:
        filename = os.path.join(projectDir, "Calibration", "%d.calib" %i)
        ci = Calibration()
        ci.load(filename, header_only=True)
        crystals.append(ci.xtals[0])
    except Exception:
        pass
    
filename = os.path.join(projectDir, "%s.xtals" %scanFile)
print (crystals)
with open(filename, 'w') as f:
    f.write("# miniXS crystal boundaries\n")
    f.write("# x1\ty1\tx2\ty2\n")
    for (x1,y1),(x2,y2) in crystals:
        f.write("%d\t%d\t%d\t%d\n" % (x1,y1,x2,y2))
        

