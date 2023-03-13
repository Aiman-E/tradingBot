from PySide6.QtCore import Qt, QRect
from PySide6.QtWidgets import QFrame, QLabel, QListWidget, QPushButton, QVBoxLayout, QSizePolicy, QListWidgetItem
from loguru import logger


class TradeList(QFrame):
    def __init__(self, lock):
        super(TradeList, self).__init__()
        self.lock = lock

    def setupUi(self):
        # Size policy
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        # Frame
        self.setObjectName(u"tradeListFrame")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)

        # Main layout
        self.tradeListLayout = QVBoxLayout(self)
        self.tradeListLayout.setContentsMargins(0, 0, 0, 0)
        self.tradeListLayout.setSpacing(0)
        
        # Label
        self.tradeListLabel = QLabel("Trades", self)
        self.tradeListLabel.setObjectName(u"tradeListLabel")
        self.tradeListLabel.setAlignment(Qt.AlignCenter)
        sizePolicy.setHeightForWidth(self.tradeListLabel.sizePolicy().hasHeightForWidth())
        sizePolicy.setVerticalStretch(0)
        self.tradeListLabel.setSizePolicy(sizePolicy)

        self.tradeListLayout.addWidget(self.tradeListLabel)

        # List
        self.tradeListWidget = QListWidget(self)
        self.tradeListWidget.setObjectName(u"tradeListWidget")
        self.tradeListWidget.setFrameShape(QFrame.NoFrame)
        self.tradeListWidget.setFrameShadow(QFrame.Plain)
        self.tradeListWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tradeListWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tradeListWidget.setDragDropOverwriteMode(False)
        sizePolicy.setHeightForWidth(self.tradeListWidget.sizePolicy().hasHeightForWidth())
        sizePolicy.setVerticalStretch(1)
        self.tradeListWidget.setSizePolicy(sizePolicy)

        self.tradeListLayout.addWidget(self.tradeListWidget)

        # Load btn
        self.loadTradeBtn = QPushButton("Load Trades", self)
        self.loadTradeBtn.setObjectName(u"loadTradeBtn")
        self.loadTradeBtn.setAutoDefault(False)
        self.loadTradeBtn.setFlat(True)
        self.loadTradeBtn.setDefault(False)
        self.loadTradeBtn.clicked.connect(self._loadCallback)
        sizePolicy.setHeightForWidth(self.loadTradeBtn.sizePolicy().hasHeightForWidth())
        sizePolicy.setVerticalStretch(0)
        self.loadTradeBtn.setSizePolicy(sizePolicy)

        self.tradeListLayout.addWidget(self.loadTradeBtn)

        # Callbacks
        self.tradeListWidget.itemClicked.connect(self._selectionCallback)

    def setSelectionCallback(self, func):
        self.selectionCallback = func

    def setLoadCallback(self, func):
        self.loadCallback = func

    def _selectionCallback(self, x):
        self.selectionCallback(x.text())

    def _loadCallback(self):
        try:
            self.lock.lock()
            l = self.loadCallback()
            self.tradeListWidget.clear()
            if l:
                for i in l:
                    self.tradeListWidget.addItem(i)
        except Exception as e:
            logger.warning(e)

        self.lock.unlock()