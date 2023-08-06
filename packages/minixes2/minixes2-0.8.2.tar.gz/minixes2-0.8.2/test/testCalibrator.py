import os
import numpy as np
from minixs.exposure import Exposure
from minixs.misc import read_scan_info
from skimage.exposure import histogram
from matplotlib import pyplot as plt

projectDir = "/Users/hammonds/Downloads/miniXESdata/FromInhui/Co3O4"

scanFileBase = "Co3O4cali.0001"
scanFile = os.path.join(projectDir, scanFileBase)
camera = "pilatus"

energies = read_scan_info(scanFile, 0)
print (energies)
print (energies.size)
exposures = list()
imageSum = None
exposureHist = []

xtalFileName = os.path.join(projectDir, "%s.xtals" % scanFileBase)
xtalData = np.loadtxt(xtalFileName)
xtals = [[[x1,y1],[x2, y2]] for x1, y1, x2, y2 in xtalData]
print xtals
numXtals = len(xtals)
xtalRowsColumns = int(np.sqrt(numXtals)+1)


for i in list(range(1, energies.size+1)):
    imageFileName = os.path.join(projectDir, 
                                 "%s.%s" % (scanFile,camera), 
                                 "%s_%.3d.tif" %(camera, i) )
    print("Opening Exposure %s" % imageFileName)
    exposures.append(Exposure(imageFileName))
    
    #exposureHist.append(histogram(exposures[i-1].pixels, exposures[i-1].pixels.max()))
    exposureHist.append([])
    print("Showing ROI data")
#    fig, axs = plt.subplots(xtalRowsColumns, xtalRowsColumns,
#                            figsize=(11,8))
    for xt in range(numXtals):
        axRow = int(xt//xtalRowsColumns)
        axCol = int(xt - axRow*xtalRowsColumns)
        print ("axRow, axCol", (axRow, axCol))
        print(xtals[xt])
        x1 = int(xtals[xt][0][0])
        x2 = int(xtals[xt][1][0])
        y1 = int(xtals[xt][0][1])
        y2 = int(xtals[xt][1][1])
        print ("x1 %d x2 %d, y1 %d, y2 %d" %(x1,x2,y1,y2))
        #print exposures[i-1].pixels[x1:x2, y1:y2]
        roiData = exposures[i-1].pixels[y1:y2,x1:x2]
        exposureHist[i-1].append(histogram(roiData, roiData.max()))
        print ("roiData %s" % roiData)
#        axs[axRow, axCol].imshow(roiData,label=xt)
#    plt.loglog(exposureHist[i-1][1], exposureHist[i-1][0], label=str(i))
        if i == 1:
            imageSum = exposures[i-1].pixels
        else:
            imageSum = imageSum + exposures[i-1].pixels
        
#    plt.legend()        
#    plt.show()

histRatios = []
fig,axs = plt.subplots(xtalRowsColumns, xtalRowsColumns,
                            figsize=(17,11))
for i in list(range(1, energies.size+1)):
#    fig, axs = plt.subplots(xtalRowsColumns, xtalRowsColumns)
    for xt in range(numXtals):
        axRow = int(xt//xtalRowsColumns)
        axCol = int(xt - axRow*xtalRowsColumns)
        axs[axRow, axCol].loglog(exposureHist[i-1][xt][1],
                                 exposureHist[i-1][xt][0], 
                                 label=str(i))
        axs[axRow, axCol].set_title("Crystal %d" % xt)
        axs[axRow, axCol].set_xlabel("Pixel Intensity")
        axs[axRow, axCol].set_ylabel("# of pixels")
        
plt.tight_layout()
plt.show()
    
        
    
histlevels = histogram(imageSum, imageSum.max())
print (histlevels[0])

#plt.loglog( histlevels[0])
#plt.show()
