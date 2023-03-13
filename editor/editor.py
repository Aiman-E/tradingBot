from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, 
                               QVBoxLayout, QHBoxLayout, QSizePolicy)
from loguru import logger

import editor.tradeList as tradeList
import editor.tradeDetails as tradeDetails
import editor.tradeOrder as tradeOrder


class Editor(QApplication):
    selectedTrade = ''
    centralWidget = None
    centralLayout = None
    lock = None

    def  __init__(self, lock):
        super().__init__()
        self.lock = lock

        self.window = QMainWindow()
        self.window.setGeometry(100, 100, 600, 600)

        self.centralWidget = QWidget(self.window)
        self.centralLayout = QVBoxLayout(self.centralWidget)
        self.window.setCentralWidget(self.centralWidget)

        self.initUI()

    def initUI(self):
        # --------------TRADES--------------
        self.tradeDetailMainWidget = QWidget(self.centralWidget)
        self.tradeDetailMainLayout = QHBoxLayout(self.tradeDetailMainWidget)
        self.tradeDetailMainLayout.setContentsMargins(3, 0, 3, 0)  
        tradeSizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        tradeSizePolicy.setHeightForWidth(self.tradeDetailMainWidget.sizePolicy().hasHeightForWidth())
        tradeSizePolicy.setHorizontalStretch(0)
        tradeSizePolicy.setVerticalStretch(1) 
        self.tradeDetailMainWidget.setSizePolicy(tradeSizePolicy)

        # Init List
        self.tradeList = tradeList.TradeList(self.lock)
        self.tradeList.setupUi()
        tradeSizePolicy.setHeightForWidth(self.tradeList.sizePolicy().hasHeightForWidth())
        tradeSizePolicy.setHorizontalStretch(0)
        tradeSizePolicy.setVerticalStretch(0) 
        self.tradeList.setSizePolicy(tradeSizePolicy)
        self.tradeList.setSelectionCallback(self.selectTradeCallback)
        self.tradeDetailMainLayout.addWidget(self.tradeList)
        
        # Init details
        # Main trade----------
        self.tradeDetails = tradeDetails.TradeDetails(self.lock)
        self.tradeDetails.setupUi()        
        tradeSizePolicy.setHeightForWidth(self.tradeDetails.sizePolicy().hasHeightForWidth())
        tradeSizePolicy.setHorizontalStretch(1)
        tradeSizePolicy.setVerticalStretch(0) 
        self.tradeDetails.setSizePolicy(tradeSizePolicy)
        self.tradeDetails.closeButton.clicked.connect(self.clearSelectedTrade)
        self.tradeDetails.closeButton.clicked.connect(self.tradeList._loadCallback)
        self.tradeDetailMainLayout.addWidget(self.tradeDetails)

        self.centralLayout.addWidget(self.tradeDetailMainWidget)


        # -----------------ORDER-----------------
        self.tradeOrder = tradeOrder.TradeOrder(self.lock)
        self.tradeOrder.setupUi()
        self.centralLayout.addWidget(self.tradeOrder)
        
        self.window.show()

    def setOpenAndFetchCallback(self, open, fetch):
        self.tradeOrder.setOpenOrderCallback(open)
        self.tradeOrder.setFetchOrderCallback(fetch)

    def setLoadCallback(self, func):
        self.tradeList.setLoadCallback(func)

    def selectTradeCallback(self, x):
        self.selectedTrade = x

    def setDetailsCallback(self, func):
        self.tradeDetails.setTradeDetailsCallback(func)

    def setDetailsEditCallback(self, func):
        self.tradeDetails.setTradeDetailsEditCallback(func)

    def setTradeCloseCallback(self, func):
        self.tradeDetails.setTradeCloseCallback(func)

    def setStatsCallback(self, func):
        self.tradeDetails.setStatsCallback(func)

    def clearSelectedTrade(self):
        self.selectedTrade = ''

    def tick(self):
        if self.selectedTrade:
            self.tradeDetails.update(self.selectedTrade)
    
        

if __name__=='__main__':
  editor = Editor()
  
  editor.exec()   