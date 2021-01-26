#!/usr/bin/env python3

#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction
from PyQt5.QtGui import QIcon
from multiprocessing import Process


def start_tray():
    # Initialize QApplication
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Set icon
    icon = QIcon("icons/shield.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Run tray
    app.exec_()


if __name__ == "__main__":
    start_tray()
