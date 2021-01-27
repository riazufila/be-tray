#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from multiprocessing import Process
import subprocess
import json
import os
import time


class systemTray():
    def check_service(self, ns, ip):
        sp = str(
            subprocess.run(
                ["systemctl", "is-active", "--quiet", ns, "/dev/null"],
                capture_output=True))

        if sp.__contains__("returncode=0"):
            ipc = ip[0]
            state = "active"
        else:
            ipc = ip[1]
            state = "inactive"

        return ipc, state

    def read_config(self):
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

    def start_tray(self, ns, ip):
        # Initialize QApplication
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.action = QAction()

        # Check service status
        ipc, state = self.check_service(ns, ip)

        # Set icon
        icon = QIcon(srcdir + ipc)
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.setToolTip(ns + " is " + state)

        # Set menu
        self.menu = QMenu()
        self.quit = QAction("Exit")
        self.quit.triggered.connect(self.app.quit)
        self.menu.addAction(self.quit)

        # Add menu to tray
        self.tray.setContextMenu(self.menu)

        # Run tray
        self.app.exec_()


if __name__ == "__main__":
    # making path global
    global srcdir

    be_tray = systemTray()

    # Some variables assignments
    srcdir = os.path.dirname(os.path.realpath(__file__))
    name_services, icon_paths = be_tray.read_config()
    num_services = len(name_services)

    # Start tray in new process
    for i in range(num_services):
        Process(target=be_tray.start_tray,
                args=(
                    name_services[i],
                    icon_paths[i],
                )).start()
