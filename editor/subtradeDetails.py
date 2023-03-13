from PySide6.QtCore import QRect
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout, QPushButton, QLineEdit, QWidget

class SubtradeTradeDetails(QWidget):
    def __init__(self):
        super(SubtradeTradeDetails, self).__init__()
        
    def setupUi(self):
        
        self.setObjectName(u"tradeDetails")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 0, 3, 0)


        # ID
        self.IDLayout = QHBoxLayout()
        self.IDLayout.setObjectName(u"IDLayout")
        self.IDLabel = QLabel(self)
        self.IDLabel.setText(u"ID:")

        self.IDLayout.addWidget(self.IDLabel)

        self.IDValue = QLabel(self)
        self.IDValue.setText(u"0")

        self.IDLayout.addWidget(self.IDValue)

        self.IDSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.IDLayout.addItem(self.IDSpacer)

        self.verticalLayout.addLayout(self.IDLayout)

        # Current Price        
        self.currentPriceLayout = QHBoxLayout()
        self.currentPriceLayout.setObjectName(u"currentPriceLayout")
        self.currentPriceLabel = QLabel(self)
        self.currentPriceLabel.setText(u"currentPrice:")

        self.currentPriceLayout.addWidget(self.currentPriceLabel)

        self.currentPriceValue = QLabel(self)
        self.currentPriceValue.setText(u"0")

        self.currentPriceLayout.addWidget(self.currentPriceValue)

        self.currentPriceSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.currentPriceLayout.addItem(self.currentPriceSpacer)

        self.verticalLayout.addLayout(self.currentPriceLayout)

        # Entry
        self.entryLayout = QHBoxLayout()
        self.entryLayout.setObjectName(u"entryLayout")
        self.entryLabel = QLabel(self)
        self.entryLabel.setText(u"entry:")

        self.entryLayout.addWidget(self.entryLabel)

        self.entryValue = QLabel(self)
        self.entryValue.setText(u"0")

        self.entryLayout.addWidget(self.entryValue)

        self.entrySpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.entryLayout.addItem(self.entrySpacer)

        self.verticalLayout.addLayout(self.entryLayout)

        # Volume
        self.volumeLayout = QHBoxLayout()
        self.volumeLayout.setObjectName(u"volumeLayout")
        self.volumeLabel = QLabel(self)
        self.volumeLabel.setText(u"volume:")

        self.volumeLayout.addWidget(self.volumeLabel)

        self.volumeValue = QLabel(self)
        self.volumeValue.setText(u"0")

        self.volumeLayout.addWidget(self.volumeValue)

        self.volumeSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.volumeLayout.addItem(self.volumeSpacer)

        self.verticalLayout.addLayout(self.volumeLayout)


    def update(self, t):
        self.IDValue.setText(str(t.id))
        self.currentPriceValue.setText(str(t.currentPrice))
        self.entryValue.setText(str(t.entry))
        self.volumeValue.setText(str(t.volume))
