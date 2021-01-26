#!/usr/bin/env python3

#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from multiprocessing import Process
import json


def start_tray(s):
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


def check_services():
    with open("config") as f:
        services = json.load(f)

    return services


if __name__ == "__main__":
    services = check_services()
    print(len(services))
    print(services)

    #for s in services:
    #   Process(target=start_tray, args=(s, )).start()
