from PySide6.QtCore import QRect
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QSpacerItem, QVBoxLayout, QPushButton, QLineEdit
from loguru import logger

from editor.subtradeDetails import SubtradeTradeDetails

class TradeDetails(QFrame):
    def __init__(self, lock):
        super(TradeDetails, self).__init__()
        self.lock = lock
        
    def setupUi(self):
        
        self.setObjectName(u"tradeDetails")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)


        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(3, 0, 3, 0)


        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 0, 3, 0)

        # Symbol
        self.symbolLabel = QLabel("", self)
        self.symbolLine = QFrame(self)
        self.symbolLine.setFrameShape(QFrame.HLine)
        self.symbolLine.setFrameShadow(QFrame.Sunken)

        self.verticalLayout.addWidget(self.symbolLabel)
        self.verticalLayout.addWidget(self.symbolLine)

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

        # Margin
        self.marginLayout = QHBoxLayout()
        self.marginLayout.setObjectName(u"marginLayout")
        self.marginLabel = QLabel(self)
        self.marginLabel.setText(u"margin:")

        self.marginLayout.addWidget(self.marginLabel)

        self.marginValue = QLabel(self)
        self.marginValue.setText(u"0")

        self.marginLayout.addWidget(self.marginValue)

        self.marginSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.marginLayout.addItem(self.marginSpacer)

        self.verticalLayout.addLayout(self.marginLayout)

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

        # Loss
        self.lossLayout = QHBoxLayout()

        self.lossLayout.setObjectName(u"lossLayout")
        self.lossLabel = QLabel(self)
        self.lossLabel.setText(u"loss:")
        self.lossLayout.addWidget(self.lossLabel)

        self.lossValue = QLabel(self)
        self.lossValue.setText(u"0")
        self.lossLayout.addWidget(self.lossValue)

        self.lossEdit = QLineEdit(self)
        self.lossEdit.returnPressed.connect(self._tradeDetailsEditCallback)
        self.lossLayout.addWidget(self.lossEdit)

        self.lossSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.lossLayout.addItem(self.lossSpacer)

        self.verticalLayout.addLayout(self.lossLayout)

        # Leverage
        self.leverageLayout = QHBoxLayout()
        self.leverageLayout.setObjectName(u"leverageLayout")
        self.leverageLabel = QLabel(self)
        self.leverageLabel.setText(u"leverage:")

        self.leverageLayout.addWidget(self.leverageLabel)

        self.leverageValue = QLabel(self)
        self.leverageValue.setText(u"0")

        self.leverageLayout.addWidget(self.leverageValue)

        self.leverageSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.leverageLayout.addItem(self.leverageSpacer)

        self.verticalLayout.addLayout(self.leverageLayout)

        # Config
        self.configLayout = QHBoxLayout()
        self.configLayout.setObjectName(u"configLayout")
        self.configLabel = QLabel(self)
        self.configLabel.setText(u"config:")

        self.configLayout.addWidget(self.configLabel)

        self.configValue = QLabel(self)
        self.configValue.setText(u"0")

        self.configLayout.addWidget(self.configValue)

        self.configSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.configLayout.addItem(self.configSpacer)

        self.verticalLayout.addLayout(self.configLayout)

        # Subtrade
        self.subtradeLayout = QHBoxLayout()
        self.subtradeLayout.setObjectName(u"subtradeLayout")
        self.subtradeLabel = QLabel(self)
        self.subtradeLabel.setText(u"subtrade:")

        self.subtradeLayout.addWidget(self.subtradeLabel)

        self.subtradeValue = QLabel(self)
        self.subtradeValue.setText(u"0")

        self.subtradeLayout.addWidget(self.subtradeValue)

        self.subtradeSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.subtradeLayout.addItem(self.subtradeSpacer)

        self.verticalLayout.addLayout(self.subtradeLayout)

        # Subtrade Threshold
        self.subtradeThresholdLayout = QHBoxLayout()

        self.subtradeThresholdLayout.setObjectName(u"subtradeThresholdLayout")
        self.subtradeThresholdLabel = QLabel(self)
        self.subtradeThresholdLabel.setText(u"subtradeThreshold:")
        self.subtradeThresholdLayout.addWidget(self.subtradeThresholdLabel)

        self.subtradeThresholdValue = QLabel(self)
        self.subtradeThresholdValue.setText(u"0")
        self.subtradeThresholdLayout.addWidget(self.subtradeThresholdValue)

        self.subtradeThresholdEditLine = QLineEdit(self)
        self.subtradeThresholdEditLine.returnPressed.connect(self._tradeDetailsEditCallback)
        self.subtradeThresholdLayout.addWidget(self.subtradeThresholdEditLine)

        self.subtradeThresholdSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.subtradeThresholdLayout.addItem(self.subtradeThresholdSpacer)

        self.verticalLayout.addLayout(self.subtradeThresholdLayout)

        # Subtrade Trigger 
        self.subtradeTriggerLayout = QHBoxLayout()

        self.subtradeTriggerLayout.setObjectName(u"subtradeTriggerLayout")
        self.subtradeTriggerPNLLabel = QLabel(self)
        self.subtradeTriggerPNLLabel.setText(u"subtradeTriggerPNL:")
        self.subtradeTriggerLayout.addWidget(self.subtradeTriggerPNLLabel)

        self.subtradeTriggerPNLValue = QLabel(self)
        self.subtradeTriggerPNLValue.setText(u"0")
        self.subtradeTriggerLayout.addWidget(self.subtradeTriggerPNLValue)

        self.subtradeTriggerLineEdit = QLineEdit(self)
        self.subtradeTriggerLineEdit.returnPressed.connect(self._tradeDetailsEditCallback)
        self.subtradeTriggerLayout.addWidget(self.subtradeTriggerLineEdit)

        self.subtradeTriggerPNLSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.subtradeTriggerLayout.addItem(self.subtradeTriggerPNLSpacer)

        self.verticalLayout.addLayout(self.subtradeTriggerLayout)

        # Reopen
        self.reopenedLayout = QHBoxLayout()
        self.reopenedLayout.setObjectName(u"reopenedLayout")
        self.reopenedLabel = QLabel(self)
        self.reopenedLabel.setText(u"reopened:")

        self.reopenedLayout.addWidget(self.reopenedLabel)

        self.reopenedValue = QLabel(self)
        self.reopenedValue.setText(u"0")

        self.reopenedLayout.addWidget(self.reopenedValue)

        self.reopenedSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.reopenedLayout.addItem(self.reopenedSpacer)

        self.verticalLayout.addLayout(self.reopenedLayout)

        # Close
        self.closeButtonLayout = QHBoxLayout()
        self.closeButton = QPushButton(self)
        self.closeButton.setText("Close")
        self.closeButton.clicked.connect(self._tradeCloseCallback)
        self.closeButtonLayout.addWidget(self.closeButton)

        self.closeButtonSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.closeButtonLayout.addItem(self.reopenedSpacer)

        self.verticalLayout.addLayout(self.closeButtonLayout)
        
        self.horizontalLayout.addLayout(self.verticalLayout)
        
        
        # Subtrade
        self.verticalLayout2 = QVBoxLayout() # I know shitty naming conversions, but I'm lazy :')
        sizePolicy = QSizePolicy()
        sizePolicy.setHorizontalPolicy(QSizePolicy.Minimum)
        sizePolicy.setVerticalPolicy(QSizePolicy.Maximum)

        self.subtradeWidget = SubtradeTradeDetails()
        sizePolicy.setHeightForWidth(self.subtradeWidget.sizePolicy().hasHeightForWidth())
        self.subtradeWidget.setSizePolicy(sizePolicy)
        self.subtradeWidget.setupUi()
        self.subtradeWidget.hide()
        self.verticalLayout2.addWidget(self.subtradeWidget)

        self.verticalLayout2Spacer = QSpacerItem(40, 20, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.verticalLayout2.addItem(self.verticalLayout2Spacer)

        # Stats------------------
        # PNL
        self.pnlLayout = QHBoxLayout()

        self.pnlLabel = QLabel(self)
        self.pnlLabel.setText(u"PNL:")
        self.pnlLayout.addWidget(self.pnlLabel)

        self.pnlValue = QLabel(u"0")
        self.pnlLayout.addWidget(self.pnlValue)

        self.actualPnlValue = QLabel(u" (0)")
        self.pnlLayout.addWidget(self.actualPnlValue)

        self.pnlSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.pnlLayout.addItem(self.pnlSpacer)

        self.verticalLayout2.addLayout(self.pnlLayout)

        # Profit
        self.profitLayout = QHBoxLayout()

        self.profitLabel = QLabel(self)
        self.profitLabel.setText(u"profit:")
        self.profitLayout.addWidget(self.profitLabel)

        self.profitValue = QLabel(u"0")
        self.profitLayout.addWidget(self.profitValue)

        self.actualProfitValue = QLabel(u" (0)")
        self.profitLayout.addWidget(self.actualProfitValue)

        self.profitSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.profitLayout.addItem(self.profitSpacer)

        self.verticalLayout2.addLayout(self.profitLayout)


        self.horizontalLayout.addLayout(self.verticalLayout2)

    def setTradeDetailsCallback(self, func):
        self.tradeDetailsCallback = func

    def setTradeDetailsEditCallback(self, func):
        self.tradeDetailsEditCallback = func

    def setTradeCloseCallback(self, func):
        self.tradeCloseCallback = func

    def setStatsCallback(self, func):
        self.statsCallback = func

    def _tradeDetailsEditCallback(self):
        self.lock.lock()
        try:
            l = float(self.lossEdit.text())
            self.tradeDetailsEditCallback('loss', self.symbolLabel.text(), l)
            self.lossEdit.clear()
        except: pass

        try:
            trig = float(self.subtradeTriggerLineEdit.text())
            self.tradeDetailsEditCallback('triggerPNL', self.symbolLabel.text(), trig)
            self.subtradeTriggerLineEdit.clear()
        except: pass
            

        try:
            threshold = float(self.subtradeThresholdEditLine.text())
            self.tradeDetailsEditCallback('threshold', self.symbolLabel.text(), threshold)
            self.subtradeThresholdEditLine.clear()
        except: pass

        self.lock.unlock()

    def _tradeCloseCallback(self):
        self.lock.lock()
        self.tradeCloseCallback(self.symbolLabel.text())
        self.lock.unlock()

    def _statsCallback(self):
        stats = self.statsCallback(self.symbolLabel.text())

        self.pnlValue.setText(str(round(stats['pnl'][0], 4)))
        self.actualPnlValue.setText(f" ({round(stats['pnl'][1], 4)})")

        self.profitValue.setText(str(round(stats['profit'][0], 4)))
        self.actualProfitValue.setText(f" ({round(stats['profit'][1], 4)})")

    def update(self, x):
        t = self.tradeDetailsCallback(x)
        self.IDValue.setText(str(t.id))
        self.symbolLabel.setText(str(t.symbol))
        self.currentPriceValue.setText(str(t.currentPrice))
        self.entryValue.setText(str(t.entry))
        self.marginValue.setText(str(t.margin))
        self.volumeValue.setText(str(t.volume))
        self.lossValue.setText(str(t.loss))
        self.leverageValue.setText(str(t.leverage))
        self.configValue.setText(str(t.config))
        self.subtradeValue.setText("Opened" if t.subtrade else "Closed")
        self.subtradeThresholdValue.setText(str(t.subtradeThreshold))
        self.subtradeTriggerPNLValue.setText(str(t.subtradeTriggerPNL))
        self.reopenedValue.setText(str(t.reopened))

        if t.subtrade:
            self.subtradeWidget.show()
            self.subtradeWidget.update(t.subtrade)
        else:
            self.subtradeWidget.hide()

        self._statsCallback()