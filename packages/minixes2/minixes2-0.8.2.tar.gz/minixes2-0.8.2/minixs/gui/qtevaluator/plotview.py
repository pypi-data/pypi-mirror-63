'''
 Copyright (c) 2020, UChicago Argonne, LLC
 See LICENSE file.
'''
import numpy as np
import PyQt5.QtWidgets as qtWidgets
from pyqtgraph.widgets.GraphicsLayoutWidget import GraphicsLayoutWidget
from pyqtgraph.graphicsItems.PlotItem.PlotItem import PlotItem
from skimage.exposure.exposure import histogram
from pyqtgraph.graphicsItems.ScatterPlotItem import ScatterPlotItem

import logging
from pyqtgraph.graphicsItems.PlotDataItem import PlotDataItem
from PyQt5 import QtGui
logger = logging.getLogger(__name__)
class PlotView(qtWidgets.QWidget):
    
    def __init__(self, parent=None):
        super(PlotView, self).__init__(parent)
        layout = qtWidgets.QVBoxLayout()
        
        sectionLabel = qtWidgets.QLabel("Sum of Data for Crystal")
        graphicsWidget = GraphicsLayoutWidget()
        self.viewBox = graphicsWidget.addViewBox()
        self.viewBox.setAspectLocked(True)
        self.plotView = PlotItem()
        self.plotView.setLogMode(x=True, y=True)
        self.viewBox.invertY(True)
        font=QtGui.QFont()
        font.setPixelSize(4)
        self.plotView.getAxis('left').setWidth(15)
        logger.debug("Width for ticks %s" % self.plotView.getAxis('left').fixedWidth)
        self.plotView.getAxis('left').setTickFont(font)
        self.plotView.getAxis('bottom').setTickFont(font)
        
        self.viewBox.addItem(self.plotView)
        self.viewBox.show()
        layout.addWidget(sectionLabel)
        layout.addWidget(graphicsWidget)
        
        self.setLayout(layout)
        
    def displayImageHistograms(self, images):
        
        self.plotView.clear()
        histLocations = np.array([])
        histValues = np.array([])
        for image in images:
            hist = histogram(image, image.max())
            logger.debug(hist)
#             if len(histLocations) == 0:
#                 histLocations = np.array([hist[1],])
#                 histValues = np.array([hist[0],])
#             else:
#                 logger.debug(histLocations)
#                 histLocations = np.concatenate(histLocations, hist[1])
#                 histValues = np.concatenate(histValues, hist[0])
            logger.debug("Length of hist 0 & 1:  %d   %d" %(len(hist[0]), len(hist[1])) )
            dataItem = PlotDataItem(x=hist[1], y=hist[0])
            self.plotView.addItem(dataItem)
    
#         font=QtGui.QFont()
#         font.setPixelSize(15)
#         self.plotView.getAxis('left').setTickFont(font)
#         self.plotView.getAxis('bottom').setTickFont(font)
        