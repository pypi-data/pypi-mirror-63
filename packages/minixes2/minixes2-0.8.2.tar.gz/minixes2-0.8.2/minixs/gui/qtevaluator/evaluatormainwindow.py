'''
 Copyright (c) 2020, UChicago Argonne, LLC
 See LICENSE file.
'''
import logging
import numpy as np
import PyQt5.QtWidgets as qtWidgets
import PyQt5.QtCore as qtCore
import matplotlib.pyplot as plt
from PyQt5.Qt import pyqtSlot, pyqtSignal, QMessageBox
from PyQt5.QtWidgets import QAction, QFileDialog
from minixs import METHOD_ENTER_STR, filetype
from minixs.gui.qtevaluator.evaluatorcontrols import ControlView
from minixs.gui.qtevaluator.imageview import ImageView
from minixs.gui.qtevaluator.plotview import PlotView
from minixs.gui.qthelpers.wildcards import WILDCARD_XTAL, WILDCARD_XTAL_EXPORT
from minixs.calibrate import Calibration
from minixs.gui.qtcalibrator.calibratormainwindow import INVALID_FILE_TEXT,\
    INVALID_FILE_TYPE_TEXT
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem

logger = logging.getLogger(__name__)

APP_NAME = "Evaluator"
EXPORT_XTAL_TITLE = "Export Crystal Boundaries"
IMPORT_XTAL_TITLE = "Import Crystal Boundaries"
READ_IMAGES_TITLE = "Load Images..."
class EvaluatorMainWindow(qtWidgets.QMainWindow):
    '''
    '''
    def __init__(self, parent=None):
        '''
        '''
        super(EvaluatorMainWindow, self).__init__(parent)
        self.lastPath = ""
        self.xtals = []
        self.exposures = []
        self.createMenuBar()
        
        self.splitter = qtWidgets.QSplitter(qtCore.Qt.Horizontal)
        self.imageView = ImageView()
        self.plotView = PlotView()

        self.evaluatorControls = ControlView(imageView=self.imageView, plotView=self.plotView)
        
        self.splitter.addWidget(self.evaluatorControls)
        self.splitter.addWidget(self.imageView)
        self.splitter.addWidget(self.plotView)
        
        self.setCentralWidget(self.splitter)
        statusBar = self.statusBar()
        self.setWindowTitle(APP_NAME)
        
    def createMenuBar(self):
        mainMenu = self.menuBar()
        
        fileMenu = mainMenu.addMenu('&File')
        viewMenu = mainMenu.addMenu('&View')
        processMenu = mainMenu.addMenu('&Process')
        selectImagesAction = QAction("&Select Images...", self)
        importXtalAction = QAction("&Import Crystals...", self)
        exportXtalAction = QAction("&Export Crystals...", self)
        modifyCrystalBoundsAction = QAction("Modify Crystal Boundaries...", self)
        
        fileMenu.addAction(selectImagesAction)
        fileMenu.addAction(importXtalAction)
        fileMenu.addAction(exportXtalAction)
        processMenu.addAction(modifyCrystalBoundsAction)
        
        selectImagesAction.triggered.connect(self.selectImages)
        importXtalAction.triggered.connect(self.importXtals)
        exportXtalAction.triggered.connect(self.exportXtals)
        modifyCrystalBoundsAction.triggered.connect(self.modifyCrystalBoundaries)
        
        
    @pyqtSlot()
    def exportXtals(self):
        logger.debug(METHOD_ENTER_STR)
        filename, _ = QFileDialog.getSaveFileName(self, EXPORT_XTAL_TITLE,
                                                   self.lastPath,
                                                   filter=WILDCARD_XTAL_EXPORT)
        if (filename != "") and (filename is not None):
            xtals = self.evaluatorControls.crystalSelector.crystals()
            with open(filename, 'w') as f:
                f.write("# miniXS crystal boundaries\n")
                f.write("# x1\ty1\tx2\ty2\n")
                for (x1,y1),(x2,y2) in xtals:
                    f.write("%d\t%d\t%d\t%d\n" % (x1,y1,x2,y2))
        
    @pyqtSlot()
    def importXtals(self):
        logger.debug(METHOD_ENTER_STR)
        filename, _ = QFileDialog().getOpenFileName(self, 
                                                      IMPORT_XTAL_TITLE,
                                                      self.lastPath,
                                                      filter=WILDCARD_XTAL)
        if filename != "" and filename is not None:
            error = None
            t = filetype.determine_filetype(filename)
            if t == filetype.FILE_CALIBRATION:
                ci = Calibration()
                ci.load(filename, header_only=True)
                xtals = ci.xtals
            elif t == filetype.FILE_XTALS or t == filetype.FILE_UNKNOWN:
                data = None
                try:
                    data = np.loadtxt(filename)
                    xtals = [[[x1,y1],[x2,y2]] for x1, y1, x2, y2 in data]
                except ValueError:
                    if data is not None:
                        if len(data.shape) == 1:
                            num = data.shape[0]
                        else:
                            num = data.shape1
                        if num !=4:
                            error = "Crystal file must contain 4 columns"
                        else:
                            error = INVALID_FILE_TEXT
                            
                    else:
                        error = INVALID_FILE_TEXT
            else:
                error = INVALID_FILE_TYPE_TEXT
                
            if error:
                QMessageBox.critical(self, "Error", "Invalid Xtal File")
                
            self.evaluatorControls.crystalSelector.setFileCrystals(xtals)
        
    @pyqtSlot()
    def modifyCrystalBoundaries(self):
        logger.debug(METHOD_ENTER_STR)
        xtals = self.evaluatorControls.crystalSelector.crystals()
        fileXtals = self.evaluatorControls.crystalSelector.fileCrystals()
        numXtals = len(xtals)
        for xtalNum in range(numXtals):
            image = self.evaluatorControls.imageSelector.getActiveImageSum(crystalBounds=xtals[xtalNum])
            verticalProfile = np.sum(image, axis=1)
            max = verticalProfile.max()
            highs = np.where(verticalProfile > max/12)
            logger.debug("Highs %s" % highs)
            diffs = np.diff(verticalProfile)
            logger.debug("diffs %s" %diffs)
#            plt.plot(verticalProfile)
            leftSide = highs[0][0]
            
            logger.debug("type[highs] %s" % type(highs) )
            logger.debug("type[highSide] %s" % type(leftSide) )
            rightSide = highs[0][-1]
            logger.debug("left, right %s, %s" %(leftSide, rightSide))
#            plt.axvspan(leftSide, rightSide, facecolor='#2ca02c')
#            plt.show()
            xtals[xtalNum][0][1] = leftSide + fileXtals[xtalNum][0][1]
            xtals[xtalNum][1][1] = rightSide + fileXtals[xtalNum][0][1]
            
        self.evaluatorControls.crystalSelector.setCrystals(xtals)
        
    @pyqtSlot()
    def selectImages(self):
        logger.debug(METHOD_ENTER_STR)
        filenames, _ = QFileDialog.getOpenFileNames(None, 
                                         caption=READ_IMAGES_TITLE, 
                                         directory=self.lastPath)
        if len(filenames) == 0:
            return 
        self.evaluatorControls.imageSelector.setImageFiles(filenames)
