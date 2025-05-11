from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, \
                        QHBoxLayout, QDialog, QLineEdit, QLabel, \
                        QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QCoreApplication

class ProgressWindow(QWidget):
    def __init__(self, maximum, txt):
        QWidget.__init__(self)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)

        self.setWindowTitle("Обработка в процессе...")
        self.resize(400, 40)
        # self.setWindowFlags(self.windowFlags() | Qt.Window)
        self.setWindowModality(Qt.ApplicationModal)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.label = QLabel(str(txt))
        self.layout.addWidget(self.label)

        self.bar = QProgressBar()
        self.layout.addWidget(self.bar)

        self.bar.setMinimum(0)
        self.bar.setMaximum(maximum)

        self.show()
        QCoreApplication.processEvents()
    
    def set(self, k, txt):
        if k == None: k = self.bar.value() + 1
        if k >= self.bar.maximum(): self.deleteLater()
        self.bar.setValue(k)
        self.label.setText(txt)
        QCoreApplication.processEvents()

class ReduceStopsWindow(QDialog):
    
    def __init__(self, lat, lon, r):
        QDialog.__init__(self)
        
        self.setWindowTitle("Сокращение количества остановок в зоне")
        
        self.verticalLayout = QVBoxLayout()
        self.setLayout(self.verticalLayout)

        self.firstLabel = QLabel("<b>Хотите ли вы уменьшить количество остановок перед импортом графика?</b><br />" +
            "Мы рекомендуем вам размещать только те остановки, которые находятся в пределах определенного круга. " +
            "по его центру и его радиусу : ")
        self.verticalLayout.addWidget(self.firstLabel)

        self.horizontalWidget = QWidget()
        self.verticalLayout.addWidget(self.horizontalWidget)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalWidget.setLayout(self.horizontalLayout)
        
        self.latLabel = QLabel("Широта")
        self.horizontalLayout.addWidget(self.latLabel)
        self.latInput = QLineEdit(lat)
        self.horizontalLayout.addWidget(self.latInput)

        self.lonLabel = QLabel("Долгота")
        self.horizontalLayout.addWidget(self.lonLabel)
        self.lonInput = QLineEdit(lon)
        self.horizontalLayout.addWidget(self.lonInput)
        
        self.rLabel = QLabel("Радиус")
        self.horizontalLayout.addWidget(self.rLabel)
        self.rInput = QLineEdit(r)
        self.horizontalLayout.addWidget(self.rInput)

        self.helpLabel = QLabel("Центр по умолчанию")
        self.helpLabel.setFont(QFont('arial', 8))
        self.verticalLayout.addWidget(self.helpLabel)
        
        self.buttonWidget = QWidget()
        self.verticalLayout.addWidget(self.buttonWidget)
        self.buttonLayout = QHBoxLayout()
        self.buttonWidget.setLayout(self.buttonLayout)

        self.validateButton = QPushButton("Чтобы проверить")
        self.buttonLayout.addWidget(self.validateButton)

        self.refuseButton = QPushButton('Не уменьшайте')
        self.buttonLayout.addWidget(self.refuseButton)

        self.setResult(QDialog.Accepted)

        self.validateButton.clicked.connect(self.accept)
        self.refuseButton.clicked.connect(self.reject)
    
    def get(self):
        if self.exec_() == QDialog.Accepted:
            lat = float(self.latInput.text())
            lon = float(self.lonInput.text())
            r = float(self.rInput.text())
            return (lat, lon, r)
        return (None, None, None)
