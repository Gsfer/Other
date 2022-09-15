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
from bend_and_expand_draw import pt_bend_expand, \
                            pathItem_bend_expand_draw, pathItem_bend_end_draw, diePath, pt_bend_rot
from collision_detect import collision_mold_and_part

from Ui_GraphicsView_test import Ui_Form

class GraphicsView_test(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(GraphicsView_test, self).__init__(parent)
        self.setupUi(self)

        # self.path_list = []
        # self.item_list = []
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 780)
        self.graphicsView.setScene(self.scene)
        
        #上模
        filePath = './resource/upperDie/UD_10.116_86.json'
        self.pt_upper_die, path = diePath(filePath, 2, 500, 500 - 50 - 0.5)
        # self.path_list.append(path)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        # self.item_list.append(diePathItem)
        # diePathItem.setBrush(Qt.red)  #设置画刷
        #给图元设置标志，可选择，可设置焦点，可移动
        # diePathItem.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable|QGraphicsItem.ItemIsMovable)
        self.scene.addItem(diePathItem)

        #下模
        filePath = 'LD_1.json'
        self.pt_lower_die, path = diePath(filePath, 4, 500, 500 + 0.5)
        # self.path_list.append(path)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        # self.item_list.append(diePathItem)
        # diePathItem.setBrush(Qt.blue)  #设置画刷
        # diePathItem.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable|QGraphicsItem.ItemIsMovable)
        self.scene.addItem(diePathItem)

        self.on_pushButton_clicked()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        length_list = [60, 60, 60, 60, 60, 60]
        angle_list = [90, 135, -90, 135, -90]
        bend_point = 4
        pt_list_left, pt_list_right = pt_bend_expand(length_list, angle_list, bend_point)
        pt_left_move, path1, item1 = pathItem_bend_expand_draw(pt_list_left, 500, 500)
        self.scene.addItem(item1)
        pt_right_move, path2, item2 = pathItem_bend_expand_draw(pt_list_right, 500, 500)
        self.scene.addItem(item2)
        pt_left_rot, path3, item3 = pathItem_bend_end_draw(pt_list_left, (180-90)/2, 500, 500 - 50)
        self.scene.addItem(item3)
        pt_right_rot, path4, item4 = pathItem_bend_end_draw(pt_list_right, -(180-90)/2, 500, 500 - 50)
        self.scene.addItem(item4)
        # self.path_list.append(path1)
        # self.path_list.append(path2)
        # self.path_list.append(path3)
        # self.path_list.append(path4)

        # print(collision_mold_and_part(self.pt_upper_die, pt_list_left))
        # pt_left_move = pt_bend_move(pt_list_left, 500, 500)
        # pt_right_move = pt_bend_move(pt_list_right, 500, 500)
        # pt_left_rot = pt_bend_rot(pt_left_move, (180-135)/2, 500, 500)
        # pt_right_rot = pt_bend_rot(pt_right_move, -(180-135)/2, 500, 500)

        if collision_mold_and_part(self.pt_upper_die, pt_left_move):
            print('upper die collides with expanded part on left')
       
        if collision_mold_and_part(self.pt_upper_die, pt_right_move):
            print('upper die collides with expanded part on right')
        
        if collision_mold_and_part(self.pt_upper_die, pt_left_rot):
            print('upper die collides with bended part on left')
       
        if collision_mold_and_part(self.pt_upper_die, pt_right_rot):
            print('upper die collides with bended part on right')
        
        if collision_mold_and_part(self.pt_lower_die, pt_left_move):
            print('lower die collides with expanded part on left')
       
        if collision_mold_and_part(self.pt_lower_die, pt_right_move):
            print('lower die collides with expanded part on right')
        
        if collision_mold_and_part(self.pt_lower_die, pt_left_rot):
            print('lower die collides with bended part on left')
       
        if collision_mold_and_part(self.pt_lower_die, pt_right_rot):
            print('lower die collides with bended part on right')
        
        
        # print(pt_right_rot)
        # print(self.pt_lower_die)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GraphicsView_test()
    ui.show()
    sys.exit(app.exec_())

