from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QFrame, QLabel, QPushButton, QVBoxLayout,
                                QHBoxLayout, QLineEdit, QRadioButton, QSpacerItem, 
                                QSizePolicy)
from loguru import logger


class TradeOrder(QFrame):
    def __init__(self, lock):
        super(TradeOrder, self).__init__()
        self.lock = lock
        self.openOrderCallback = None
        self.fetchOrderCallback = None

    def setupUi(self):
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setObjectName(u"mainLayout")
        self.mainLayout.setContentsMargins(3, 3, 3, 3)
        self.symbolLayout = QHBoxLayout()
        self.symbolLayout.setObjectName(u"symbolLayout")
        self.symbol = QLabel(self)
        self.symbol.setText(u"symbol:")

        self.symbolLayout.addWidget(self.symbol)

        self.symbolEdit = QLineEdit(self)
        self.symbolEdit.setObjectName(u"symbolEdit")

        self.symbolLayout.addWidget(self.symbolEdit)


        self.mainLayout.addLayout(self.symbolLayout)

        self.entryLayout = QHBoxLayout()
        self.entryLayout.setObjectName(u"entryLayout")
        self.entry = QLabel(self)
        self.entry.setText(u"entry:")

        self.entryLayout.addWidget(self.entry)

        self.entryEdit = QLineEdit(self)
        self.entryEdit.setObjectName(u"entryEdit")

        self.entryLayout.addWidget(self.entryEdit)


        self.mainLayout.addLayout(self.entryLayout)

        self.marginLayout = QHBoxLayout()
        self.marginLayout.setObjectName(u"marginLayout")
        self.margin = QLabel(self)
        self.margin.setText(u"margin:")

        self.marginLayout.addWidget(self.margin)

        self.marginEdit = QLineEdit(self)
        self.marginEdit.setObjectName(u"marginEdit")

        self.marginLayout.addWidget(self.marginEdit)


        self.mainLayout.addLayout(self.marginLayout)

        self.lossLayout = QHBoxLayout()
        self.lossLayout.setObjectName(u"lossLayout")
        self.loss = QLabel(self)
        self.loss.setText(u"loss:")

        self.lossLayout.addWidget(self.loss)

        self.lossEdit = QLineEdit(self)
        self.lossEdit.setObjectName(u"lossEdit")

        self.lossLayout.addWidget(self.lossEdit)


        self.mainLayout.addLayout(self.lossLayout)

        self.leverageLayout = QHBoxLayout()
        self.leverageLayout.setObjectName(u"leverageLayout")
        self.leverage = QLabel(self)
        self.leverage.setText(u"leverage:")

        self.leverageLayout.addWidget(self.leverage)

        self.leverageEdit = QLineEdit(self)
        self.leverageEdit.setObjectName(u"leverageEdit")

        self.leverageLayout.addWidget(self.leverageEdit)


        self.mainLayout.addLayout(self.leverageLayout)

        self.sideLayout = QHBoxLayout()
        self.sideLayout.setObjectName(u"sideLayout")
        self.longRadio = QRadioButton(self)
        self.longRadio.setText(u"Long")

        self.sideLayout.addWidget(self.longRadio)

        self.shortRadio = QRadioButton(self)
        self.shortRadio.setText(u"Short")

        self.sideLayout.addWidget(self.shortRadio)
        self.sideSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.sideLayout.addItem(self.sideSpacer)


        self.mainLayout.addLayout(self.sideLayout)

        self.buttonLayout = QHBoxLayout()
        self.buttonLayout.setObjectName(u"buttonLayout")

        self.openButton = QPushButton(self)
        self.openButton.setText(u"Open")
        self.openButton.clicked.connect(self._openOrderCallback)

        self.buttonLayout.addWidget(self.openButton)

        self.fetchButton = QPushButton(self)
        self.fetchButton.setText(u"Fetch")
        self.fetchButton.clicked.connect(self._fetchOrderCallback)

        self.buttonLayout.addWidget(self.fetchButton)
        self.buttonSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.buttonLayout.addItem(self.buttonSpacer)


        self.mainLayout.addLayout(self.buttonLayout)
        

    def setOpenOrderCallback(self, func):
        self.openOrderCallback = func

    def setFetchOrderCallback(self, func):
        self.fetchOrderCallback = func

    def _openOrderCallback(self):
        if not self.openOrderCallback:
            logger.warning("Open order button callback not set yet!")
            return
        
        s = "long" if self.longRadio.isChecked() else "short"
        try:
            self.lock.lock()
            self.openOrderCallback(symbol=self.symbolEdit.text(),
                entry=float(self.entryEdit.text()),
                margin=float(self.marginEdit.text()),
                loss=float(self.lossEdit.text()),
                leverage=int(self.leverageEdit.text()),
                side=s)
            
            
            self.symbolEdit.setText("")
            self.entryEdit.setText("")
            self.marginEdit.setText("")
            self.lossEdit.setText("")
            self.leverageEdit.setText("")
            self.longRadio.toggle()
        except Exception as e:
            logger.warning(e)
        self.lock.unlock()

    def _fetchOrderCallback(self):
        if not self.fetchOrderCallback:
            logger.warning("Fetch order button callback not set yet!")
            return

        s = "long" if self.longRadio.isChecked() else "short"

        try:
            self.lock.lock()
            self.fetchOrderCallback(symbol=self.symbolEdit.text(),
                loss=float(self.lossEdit.text()),
                leverage=int(self.leverageEdit.text()),
                side=s)

            self.symbolEdit.setText("")
            self.entryEdit.setText("")
            self.marginEdit.setText("")
            self.lossEdit.setText("")
            self.leverageEdit.setText("")
            self.longRadio.toggle()
        except Exception as e:
            logger.warning(e)
        self.lock.unlock()
