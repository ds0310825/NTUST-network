from time import sleep

from PyQt5.QtCore import QTimer, QThread, pyqtSignal

from searcher import search
from PyQt5 import QtWidgets, QtGui, QtCore
from dialog import Ui_Dialog
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from chromedriver_checker import check_browser_driver_available


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        internet_usage = search()
        super(MainWindow, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.lcdNumber.display(internet_usage)

        # daily limit 20GB
        usage_percent = float(internet_usage) / 20 * 100
        print(usage_percent)

        # set the progress bar
        self.ui.progressBar.setValue(usage_percent)
        self.ui.progressBar.setFormat("%.02f %%" % usage_percent)

        # this is a thread which can get the data and reflash the window
        self.thread = Thread()
        self.thread.trigger.connect(self.reflasher)

        self.thread.start()

        self.setWindowTitle("網路用量表 %.01f %%" % usage_percent)

    def reflasher(self, internet_usage):
        usage_percent = float(internet_usage) / 20 * 100
        print(usage_percent)

        self.setWindowTitle("網路用量表 %.01f %%" % usage_percent)

        self.ui.progressBar.setValue(usage_percent)
        self.ui.progressBar.setFormat("%.02f %%" % usage_percent)

        self.ui.lcdNumber.display(internet_usage)
        print('refreshed')


class Thread(QThread):
    # set the signal dtype
    trigger = pyqtSignal(str)

    def __init__(self):
        super(Thread, self).__init__()

    def run(self):
        while True:
            # reflash once per 2 minutes
            sleep(120)
            internet_usage = search()

            # send the signal
            self.trigger.emit(internet_usage)


if __name__ == '__main__':
    try:  # just avoid crash...
        try:
            check_browser_driver_available()
        except Exception as e:
            print(e)

        app = QtWidgets.QApplication([])
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(e)
