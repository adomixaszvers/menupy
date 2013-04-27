#!/usr/bin/env python2
from PyQt4 import QtGui, QtCore
import sys, subprocess
import keybinder
import threading

pakeitimo_komanda = "setxkbmap"


class Tray(QtGui.QSystemTrayIcon):
  def __init__(self, variantai, parent=None):
    super(QtGui.QSystemTrayIcon, self).__init__(QtGui.QApplication.style().standardIcon(QtGui.QStyle.SP_DriveDVDIcon), parent)
    menu = QtGui.QMenu()
    for variantas in variantai:
      menu.addAction(QtGui.QAction(variantas, menu))

    exitAction = QtGui.QAction('Exit', menu)
    exitAction.setStatusTip('Exit application')
    exitAction.triggered.connect(sys.exit)

    menu.addAction(exitAction)
    menu.triggered.connect(self.pakeisk)
    
    self.setContextMenu(menu)

  def pakeisk(self, veiksmas):
    variantas = veiksmas.text()
    if variantas != "Exit":
      if not subprocess.call([pakeitimo_komanda,  "%s" % variantas]):
	self.showMessage("Pakeista", variantas, msecs=2000)
      else:
	tray.showMessage("Nepakeista", variantas+"\n\n\n", msecs=2000)
      self.setToolTip(variantas)

class KeyBinder:
  def __init__(self, variantai, keystr, tray):
    self.variantai = variantai
    self.skaicius = 0
    keybinder.bind(keystr, self.pakeisk)
  def pakeisk(self):
    self.skaicius += 1
    if self.skaicius >= len(self.variantai):
      self.skaicius = 0
    variantas = self.variantai[self.skaicius]
    if not subprocess.call([pakeitimo_komanda,  "%s" % variantas]):
      tray.showMessage("Pakeista", variantas+"\n\n\n", msecs=2000)
    else:
      tray.showMessage("Nepakeista", variantas+"\n\n\n", msecs=2000)
    tray.setToolTip(variantas)


if __name__ == "__main__":
  variantai = ["lt", "us"]
  app = QtGui.QApplication(sys.argv)
  tray = Tray(variantai)
  tray.show()
  key = KeyBinder(variantai, "<Shift>space", tray)
  sys.exit(app.exec_())
