#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QAction, QMenu
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from multiprocessing import Process
import subprocess
import os


def check_service(self, ns, ip):
    sp = str(
        subprocess.run(["systemctl", "is-active", "--quiet", ns, "/dev/null"],
                       capture_output=True))

    if sp.__contains__("returncode=0"):
        ipc = ip[0]
        state = "active"
    else:
        ipc = ip[1]
        state = "inactive"

    return ipc, state


def read_config():
    # Some variables assignments
    name_services = []
    icon_paths = []

    # Parsing config from json to dictionary
    with open(srcdir + "be-tray.conf", "r") as f:
        services = f.read().splitlines()

    for l in services:
        if l.startswith("#") or len(l.strip()) == 0:
            pass
        else:
            line = l.split("=")
            name_services.append(line[0].strip())
            ip_buffer = line[1].replace(" ", "").split(",")
            ip = []
            for m in ip_buffer:
                ip.append(m)

            icon_paths.append(ip)

    return name_services, icon_paths


class worker(QObject):
    cs = check_service
    newIcon = pyqtSignal(object)
    newToolTip = pyqtSignal(str)

    def __init__(self, ns, ip):
        super().__init__()
        self.ns = ns
        self.ip = ip

    def run(self):
        while True:
            ipc, state = self.cs(self.ns, self.ip)
            self.newIcon.emit(QIcon(srcdir + ipc))
            self.newToolTip.emit(self.ns + " is " + state)
            QThread.msleep(1000)


class systemTray(QObject):
    cs = check_service

    def start_tray(self, ns, ip):
        # Initialize QApplication
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

        # Check service status
        ipc, state = self.cs(ns, ip)

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

        # Create thread
        self.thread = QThread()
        # Create object which will be moved from main thread to worker thread
        self.worker = worker(ns, ip)
        # Move object to worker thread
        self.worker.moveToThread(self.thread)
        # Connect object to signal
        self.worker.newIcon.connect(self.updateIcon)
        self.worker.newToolTip.connect(self.updateToolTip)
        # Connect started signal to run method of object in worker thread
        self.thread.started.connect(self.worker.run)
        # Start thread
        self.thread.start()

        # Run tray
        self.app.exec_()

    def updateIcon(self, icon):
        self.tray.setIcon(icon)

    def updateToolTip(self, tooltip):
        self.tray.setToolTip(tooltip)


if __name__ == "__main__":
    # making path global
    global srcdir

    # Object initialization
    be_tray = systemTray()

    # Some variables assignments
    srcdir = os.path.dirname(os.path.realpath(__file__)) + "/"
    name_services, icon_paths = read_config()
    num_services = len(name_services)

    # Start tray in new process
    for i in range(num_services):
        Process(target=be_tray.start_tray,
                args=(
                    name_services[i],
                    icon_paths[i],
                )).start()
