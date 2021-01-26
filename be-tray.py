#!/usr/bin/env python3

#!/usr/bin/env python3

from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

app = QApplication([])
app.setQuitOnLastWindowClosed(False)

icon = QIcon("icons/shield.png")
tray = QSystemTrayIcon()
tray.setIcon(icon)

tray.setVisible(True)

#menu = QMenu()
#entries = ["One", "Two", "Three"]
#for entry in entries:
#    action = QAction(entry)
#    menu.addAction(action)
#    action.triggered.connect(app.quit)

#tray.setContextMenu(menu)

app.exec_()
