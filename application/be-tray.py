#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from multiprocessing import Process
import subprocess
import json
import os
import time


class worker(QObject):
    newIcon = pyqtSignal(object)

    @pyqtSlot()
    def run(self):
        while True:
            self.newIcon.emit(
                QIcon(
                    "/home/riazufila/Repositories/be-tray/icons/shield-off.png"
                ))
            QThread.msleep(1000)


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

        # create thread
        self.thread = QThread()
        # create object which will be moved to another thread
        self.worker = worker()
        # move object to another thread
        self.worker.moveToThread(self.thread)
        # after that, we can connect signals from this object to slot in GUI thread
        self.worker.newIcon.connect(self.updateIcon)
        # connect started signal to run method of object in another thread
        self.thread.started.connect(self.worker.run)
        # start thread
        self.thread.start()

        # Run tray
        self.app.exec_()

    def updateIcon(self, icon):
        self.tray.setIcon(icon)


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
