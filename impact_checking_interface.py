# -*- coding: utf-8 -*-

"""
Module implementing GraphicsView_test.
"""
import time,json
from pprint import pprint
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import (QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, QGraphicsItem,
QGraphicsPathItem, QGraphicsLineItem)
from PyQt5.QtCore import Qt,pyqtSignal, pyqtSlot, QPoint,QRectF
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from bend_and_expand_draw import pt_bend_expand,pathItem_bend_expand_draw, pathItem_bend_end_draw, diePath
from collision_detect import collision_mold_and_part, process_impack_check

from Ui_GraphicsView_test import Ui_Form

class GraphicsView_test(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    run_signal = pyqtSignal(int ,list, list)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GraphicsView_test, self).__init__(parent)
        self.setupUi(self)

        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 780)
        self.graphicsView.setScene(self.scene)
        
        #上模
        filePath = './resource/upperDie/UD_10.116_86.json'
        self.pt_upper_die, path = diePath(filePath, 2, 500, 500 - 50 - 0.5)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        self.scene.addItem(diePathItem)

        #下模
        filePath = 'LD_1.json'
        self.pt_lower_die, path = diePath(filePath, 4, 500, 500 + 0.5)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        self.scene.addItem(diePathItem)

        self.on_pushButton_clicked()
        # self.work_step_num = 0
        # self.run_signal.connect(self.run_process)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        length_list = [60, 60, 60, 60, 60, 60]
        angle_list = [90, 135, -90, 135, -90]
        bend_list = [3, 1, 4, 0, 2]
        # bend_list = [0,1,2,3,4]

        pt_upper_die = self.pt_upper_die
        pt_lower_die = self.pt_lower_die
        base_point = [500, 500]
        upper_offset = 50

        process_impack_check(bend_list, length_list, angle_list, pt_upper_die, pt_lower_die,
                            base_point, upper_offset)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GraphicsView_test()
    ui.show()
    sys.exit(app.exec_())

