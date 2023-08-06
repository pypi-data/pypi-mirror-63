'''
 Copyright (c) 2020, UChicago Argonne, LLC
 See LICENSE file.
'''

import logging
import copy
import PyQt5.QtWidgets as qtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.Qt import pyqtSlot, QIntValidator, qApp, QValidator
from PyQt5.QtCore import Qt

from skimage.io import imread_collection
from minixs import METHOD_ENTER_STR


logger = logging.getLogger(__name__)

class ControlView(qtWidgets.QWidget):

    def __init__(self, parent=None, imageView=None, plotView=None):
        super(ControlView, self).__init__(parent)
        self.xtals = []
        layout = qtWidgets.QVBoxLayout()
        self.crystalSelector=CrystalSelector()
        self.imageSelector = ImageSelector()

        self.imageView = imageView
        self.plotView = plotView
        self.crystalSelector.crystalListChanged.connect(self.handleCrystalListChanged)
        self.crystalSelector.crystalNumberChanged.connect(self.handleCrystalNumberChanged)
        self.crystalSelector.crystalRegionChanged.connect(self.handleCrystalRegionChanged)
        self.imageSelector.imageListChanged.connect(self.handleImageListChanged)
        self.imageSelector.imageList.itemChanged.connect(self.handleImageStatusChanged)
        
        
        layout.addWidget(self.crystalSelector)
 
#        layout.addWidget(self.crystalRegionEditor)
        
        layout.addWidget(self.imageSelector)
        self.setLayout(layout)
        self.show()
    
    @pyqtSlot()
    def handleCrystalListChanged(self):
        logger.debug(METHOD_ENTER_STR)
        if not (self.crystalSelector.hasXtals() and 
            self.imageSelector.hasImages()):
            return 
        
        
    @pyqtSlot()
    def handleCrystalNumberChanged(self):
        logger.debug(METHOD_ENTER_STR % self.crystalSelector.activeCrystal())
        if not (self.crystalSelector.hasXtals() and 
            self.imageSelector.hasImages()):
            return
        currentXtal = self.crystalSelector.activeCrystal()
        fileXtal = self.crystalSelector.activeFileCrystal()
        sumImage = self.imageSelector.getActiveImageSum(fileXtal)
        self.imageView.setImage(sumImage, fileXtal)
        self.imageView.setROI(currentXtal, fileXtal)
        images = []
        # Loop over selected images
        for imageNum in  self.imageSelector.activeImageNums():
            images.append(self.imageSelector.getImage(imageNum, currentXtal))
        self.plotView.displayImageHistograms(images)
            
    
    @pyqtSlot()
    def handleCrystalRegionChanged(self):
        logger.debug(METHOD_ENTER_STR)
        if not (self.crystalSelector.hasXtals() and 
            self.imageSelector.hasImages()):
            return 
        currentXtal = self.crystalSelector.activeCrystal()
        fileXtal = self.crystalSelector.activeFileCrystal()
        sumImage = self.imageSelector.getActiveImageSum(fileXtal)
        self.imageView.setImage(sumImage, fileXtal)
        self.imageView.setROI(currentXtal, fileXtal)
        images = []
        # Loop over selected images
        for imageNum in  self.imageSelector.activeImageNums():
            images.append(self.imageSelector.getImage(imageNum, currentXtal))
        self.plotView.displayImageHistograms(images)
    
    @pyqtSlot()
    def handleImageListChanged(self):
        logger.debug(METHOD_ENTER_STR)
        if not (self.crystalSelector.hasXtals() and 
            self.imageSelector.hasImages()):
            return 
        currentXtal = self.crystalSelector.activeCrystal()
        fileXtal = self.crystalSelector.activeFileCrystal()
        sumImage = self.imageSelector.getActiveImageSum(fileXtal)
        self.imageView.setImage(sumImage, fileXtal)
        self.imageView.setROI(currentXtal, self.crystalSelector.activeFileCrystal())
        images = []
        # Loop over selected images
        for imageNum in  self.imageSelector.activeImageNums():
            images.append(self.imageSelector.getImage(imageNum, currentXtal))
        self.plotView.displayImageHistograms(images)
        
    def handleImageStatusChanged(self):
        logger.debug(METHOD_ENTER_STR)
        if not (self.crystalSelector.hasXtals() and 
            self.imageSelector.hasImages()):
            return 
        currentXtal = self.crystalSelector.activeCrystal()
        fileXtal = self.crystalSelector.activeFileCrystal()
        sumImage = self.imageSelector.getActiveImageSum(fileXtal)
        self.imageView.setImage(sumImage, fileXtal)
        self.imageView.setROI(currentXtal, self.crystalSelector.activeFileCrystal())
        images = []
        # Loop over selected images
        for imageNum in  self.imageSelector.activeImageNums():
            images.append(self.imageSelector.getImage(imageNum, currentXtal))
        self.plotView.displayImageHistograms(images)
        
        
class CrystalSelector(qtWidgets.QWidget):
    crystalListChanged = pyqtSignal(name="crystalListChanged")
    crystalNumberChanged = pyqtSignal(name="crystalNumberChanged")
    crystalRegionChanged = pyqtSignal(name="crystalRegionChanged")
    
    def __init__(self, parent=None):
        super(CrystalSelector,self).__init__(parent)
        self.xtals = []
        self.fileXtals = []
        layout = qtWidgets.QHBoxLayout()
        label = qtWidgets.QLabel("Crystal #")
        self.crystalNumber = qtWidgets.QComboBox()
        self.crystalNumber.currentIndexChanged[int].connect(self.handleCrystalNumberChanged)
        regionLayout = qtWidgets.QVBoxLayout()
        sectionLabel = qtWidgets.QLabel("Crystal Region")
        x1Layout = qtWidgets.QHBoxLayout()
        x1Label = qtWidgets.QLabel("x1")
        self.x1Txt = qtWidgets.QLineEdit()
        x1Layout.addWidget(x1Label)
        x1Layout.addWidget(self.x1Txt)
        x2Layout = qtWidgets.QHBoxLayout()
        x2Label = qtWidgets.QLabel("x2")
        self.x2Txt = qtWidgets.QLineEdit()
        x2Layout.addWidget(x2Label)
        x2Layout.addWidget(self.x2Txt)
        y1Layout = qtWidgets.QHBoxLayout()
        y1Label = qtWidgets.QLabel("y1")
        self.y1Txt = qtWidgets.QLineEdit()
        y1Layout.addWidget(y1Label)
        y1Layout.addWidget(self.y1Txt)
        y2Layout = qtWidgets.QHBoxLayout()
        y2Label = qtWidgets.QLabel("y2")
        self.y2Txt = qtWidgets.QLineEdit()
        y2Layout.addWidget(y2Label)
        y2Layout.addWidget(self.y2Txt)
        self.x1Txt.setValidator(QIntValidator())
        self.x2Txt.setValidator(QIntValidator())
        self.y1Txt.setValidator(QIntValidator())
        self.y2Txt.setValidator(QIntValidator())
        #self.x1Txt.textChanged.connect(self.handleCrystalRegionTextChanged)
        self.x1Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.x2Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.y1Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.y2Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        regionLayout.addWidget(sectionLabel)
        regionLayout.addLayout(x1Layout)
        regionLayout.addLayout(x2Layout)
        regionLayout.addLayout(y1Layout)
        regionLayout.addLayout(y2Layout)

        layout.addWidget(label)
        layout.addWidget(self.crystalNumber)
        layout.addLayout(regionLayout)
        
        self.setLayout(layout)

    def activeCrystal(self):
        xtalNum = self.crystalNumber.currentIndex()
        return self.xtals[xtalNum]
        
    def addTxtConnections(self):
        self.x1Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.x2Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.y1Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        self.y2Txt.editingFinished.connect(self.handleCrystalRegionChanged)
        #self.x1Txt.textChanged.connect(self.handleCrystalRegionTextChanged())

    def deleteTxtConnections(self):
        self.x1Txt.editingFinished.disconnect(self.handleCrystalRegionChanged)
        self.x2Txt.editingFinished.disconnect(self.handleCrystalRegionChanged)
        self.y1Txt.editingFinished.disconnect(self.handleCrystalRegionChanged)
        self.y2Txt.editingFinished.disconnect(self.handleCrystalRegionChanged)
        #self.x1Txt.textChanged.disconnect(self.handleCrystalRegionTextChanged())

    def emitTxtChanged(self):
        self.x1Txt.editingFinished.emit()
        self.x2Txt.editingFinished.emit()
        self.y1Txt.editingFinished.emit()
        self.y2Txt.editingFinished.emit()
        #self.y2Txt.textChanged.emit()
        
    def activeFileCrystal(self):
        xtalNum = self.crystalNumber.currentIndex()
        return self.fileXtals[xtalNum]
        
    def crystals(self):
        '''
        reads the current set of crystals.  These may have been modified since 
        the last read/write from file.
        '''
        return self.xtals
    
    def fileCrystals(self):
        '''
        returns the list of crystals last read from/written to file
        '''
        return self.fileXtals
    
    @pyqtSlot(int)
    def handleCrystalNumberChanged(self, xtalNumber):
        #self.deleteTxtConnections()
        self.setXtalValuesToCrystal(self.xtals[xtalNumber])
        #self.addTxtConnections()
        
    def handleCrystalRegionTextChanged(self ):
        logger.debug(METHOD_ENTER_STR)
        sender = self.sender()
        logger.debug("sender type %s" % type(sender))
        validator=sender.validator()
        state = validator.validate(sender.text(), 0)[0]
        if state == QValidator.Acceptable:
            color = '#c4df9b'
        if state == QValidator.Intermediate:
            color == '#fff79a'
        else:
            color == '#f6989d'
        sender.setStylesheet('QLineEdit {backgroundColor: %s}' % color)

    def handleCrystalRegionChanged(self):
        xtalNum = self.crystalNumber.currentIndex()
#         if self.x1Txt.validator().validate(self.x1Txt.text(), 0) == QValidator.Acceptable:
#             self.xtals[xtalNum][0][0] = int(self.x1Txt.text())
#         else:
#             qApp.beep()
        self.xtals[xtalNum][0][0] = int(self.x1Txt.text())
        self.xtals[xtalNum][1][0] = int(self.x2Txt.text())
        self.xtals[xtalNum][0][1] = int(self.y1Txt.text())
        self.xtals[xtalNum][1][1] = int(self.y2Txt.text())
        self.setValidatorLimits()
        self.crystalRegionChanged.emit()
        
    def hasXtals(self):
        return len(self.xtals) > 0
    
    def setFileCrystals(self, xtals):
        self.fileXtals = xtals
        self.setCrystals(xtals)
        
        
    def setCrystals(self, xtals):
        logger.debug(METHOD_ENTER_STR)
        self.xtals = copy.deepcopy(xtals)
        self.crystalNumber.clear()
        xtalNames = []

        for i in range(1,len(self.xtals)+1):
            xtalNames.append("Crystal %d" % i)
        self.crystalNumber.addItems(xtalNames)
        self.crystalNumber.setCurrentIndex(0)
        self.setXtalValuesToCrystal(xtals[0])
        #self.crystalListChanged.emit()
        
    def setValidatorLimits(self):
        xtalNum = self.crystalNumber.currentIndex()
        logger.debug("CrystalNumber %d" % xtalNum)
        fileXtal = self.fileXtals[xtalNum]
        xtal = self.xtals[xtalNum]
#         self.x1Txt.validator().setBottom(fileXtal[0][0])
#         self.x1Txt.validator().setTop(xtal[1][0])
        x1validator = self.x1Txt.validator()
        logger.debug("setting x1 validator range %d %d" % (int(fileXtal[0][0]),int(xtal[1][0])))
        x1validator.setRange(int(fileXtal[0][0]),int(xtal[1][0]))
        
        logger.debug("setting x2 validator range %d %d" % (int(xtal[0][0]),int(fileXtal[1][0])))
        self.x2Txt.validator().setRange(xtal[0][0], fileXtal[1][0])

        logger.debug("setting y1 validator range %d %d" % (int(fileXtal[0][1]),int(xtal[1][1])))
        self.y1Txt.validator().setRange(fileXtal[0][1], xtal[1][1])

        logger.debug("setting y2 validator range %d %d" % (int(xtal[0][1]),int(fileXtal[1][1])))
        self.y2Txt.validator().setRange(xtal[0][1], fileXtal[1][1])
        
        
    def setXtalValuesToCrystal(self, xtal):
        logger.debug(METHOD_ENTER_STR % xtal)
        self.x1Txt.setText(str(int(xtal[0][0])))
        self.x2Txt.setText(str(int(xtal[1][0])))
        self.y1Txt.setText(str(int(xtal[0][1])))
        self.y2Txt.setText(str(int(xtal[1][1])))
        self.setValidatorLimits()
        self.crystalNumberChanged.emit()

class ImageSelector(qtWidgets.QWidget):
    imageListChanged = pyqtSignal(name="imageListChanged")
    
    def __init__(self, parent=None):
        super(ImageSelector, self).__init__(parent)
        self.filenames = []
        self.imageCollection = None
        self.xtal = None
        layout = qtWidgets.QVBoxLayout()
        imageLabel = qtWidgets.QLabel("ImageLayout")
        self.imageList = qtWidgets.QListWidget()
        self.imageList.setMinimumSize(150, 400)
        
        layout.addWidget(imageLabel)
        layout.addWidget(self.imageList)
        
        self.setLayout(layout)
        
    def activeImageNums(self):
        logger.debug(METHOD_ENTER_STR)
        imageNums = []
        for itemNum in range(self.imageList.count()):
            item = self.imageList.item(itemNum)
            if item.checkState() == Qt.Checked:
                imageNums.append(itemNum)
        return imageNums
    
    def activeNames(self):
        logger.debug(METHOD_ENTER_STR)
        imageNames = []
        for itemNum in range(self.imageList.count()):
            item = self.imageList.item(itemNum)
            if item.checkState() == Qt.Checked:
                imageNames.append(item.text())
        return imageNames
    
    def getImage(self, imageNum, crystalBounds=None):
        if not self.hasImages():
            raise IndexError("No Images are loaded")
        
        if len(self.imageCollection) < imageNum-1:
            raise IndexError("Image Number %d is greater than the size of "
                             "image collection loaded" % imageNum)
        if crystalBounds is None:    
            return self.imageCollection[imageNum]
        else:
            x1 = int(crystalBounds[0][0])
            x2 = int(crystalBounds[1][0])
            y1 = int(crystalBounds[0][1])
            y2 = int(crystalBounds[1][1])
            return self.imageCollection[imageNum][y1:y2+1,x1:x2+1]

        
    def hasImages(self):
        return len(self.filenames) > 0
    
    def numImages(self):
        return len(self.imageCollection)
    
    def setImageFiles(self, filenames):
        self.filenames = filenames
        self.imageList.clear()
        for imageNum in range(len(filenames)):            
            self.imageList.addItem(filenames[imageNum])
            item = self.imageList.item(imageNum)
            item.setFlags(item.flags()| Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Checked)
        self.imageCollection = imread_collection(filenames)
        self.imageListChanged.emit()

    def getActiveImageSum(self, crystalBounds=None):
        imageSum = None
        for imageNum in self.activeImageNums():
            thisImage = self.getImage(imageNum, crystalBounds)
            if imageSum is None:
                imageSum = thisImage
            else:
                imageSum = imageSum + thisImage
        return imageSum
        
        
    def updateImage(self):
        logger.debug(METHOD_ENTER_STR)

