#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from multiprocessing import Process
import subprocess
import json
import os
import time


def start_tray(ns, ip):
    # Initialize QApplication
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    action = QAction()

    # Check service status
    sp = str(
        subprocess.run(["systemctl", "is-active", "--quiet", ns, "/dev/null"],
                       capture_output=True))

    if sp.__contains__("returncode=0"):
        ipc = ip[0]
        state = "active"
    else:
        ipc = ip[1]
        state = "inactive"

    # Set icon
    icon = QIcon(srcdir + ipc)
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    tray.setToolTip(ns + " is " + state)

    # Set menu
    menu = QMenu()
    toggle = QAction("Enable/Disable")
    quit = QAction("Exit")
    quit.triggered.connect(app.quit)
    menu.addAction(toggle)
    menu.addAction(quit)

    # Add menu to tray
    tray.setContextMenu(menu)

    # Run tray
    app.exec_()


def read_config():
    # Some variables assignments
    name_services = []
    icon_paths = []

    # Parsing config from json to dictionary
    with open(srcdir + "/../config/be-tray.json") as f:
        services = json.load(f)

    # Appending values in declared tuples
    for ns, ip in services.items():
        name_services.append(ns)
        icon_paths.append(ip)

    return name_services, icon_paths


if __name__ == "__main__":
    # making path global
    global srcdir

    # Some variables assignments
    srcdir = os.path.dirname(os.path.realpath(__file__))
    name_services, icon_paths = read_config()
    num_services = len(name_services)

    # Start tray in new process
    for i in range(num_services):
        Process(target=start_tray, args=(
            name_services[i],
            icon_paths[i],
        )).start()
