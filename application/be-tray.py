#!/usr/bin/env python3

#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from multiprocessing import Process
import json


def start_tray(ns, on, off):
    # Initialize QApplication
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)

    # Set icon
    icon = QIcon("../icons/shield.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    # Run tray
    app.exec_()


def check_services():
    name_services = []
    icon_paths_on = []
    icon_paths_off = []

    with open("../config/be-tray.json") as f:
        services = json.load(f)

    for s in services:
        name_services.append(s)

    for ns in name_services:
        icon_paths_on.append(services[ns][0])

    for ns in name_services:
        icon_paths_off.append(services[ns][1])

    return name_services, icon_paths_on, icon_paths_off


if __name__ == "__main__":
    name_services, icon_paths_on, icon_paths_off = check_services()

    num_services = len(name_services)

    for i in range(num_services):
        Process(target=start_tray,
                args=(
                    name_services[i],
                    icon_paths_on[i],
                    icon_paths_off[i],
                )).start()
