# -*- coding: utf-8 -*-

"""
Module implementing GraphicsView_test.
"""
import time
from pprint import pprint
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import (QWidget, QApplication, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QMainWindow, QLabel, QGraphicsItem,
QGraphicsPathItem, QGraphicsLineItem)
from PyQt5.QtCore import Qt,pyqtSignal, pyqtSlot, QPoint,QRectF
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from bend_and_expand_draw import ptExtend, ptRotation, pt_cal, pt_bend_expand, \
                            pathItem_bend_expand_draw, pathItem_bend_end_draw, diePath

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

        self.path_list = []
        self.item_list = []
        self.scene = QGraphicsScene()
        self.scene.setSceneRect(0, 0, 1000, 780)
        self.graphicsView.setScene(self.scene)
        
        #上模
        filePath = './resource/upperDie/UD_10.116_86.json'
        path = diePath(filePath, 2, 500, 400)
        # self.path_list.append(path)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        self.item_list.append(diePathItem)
        # diePathItem.setBrush(Qt.red)  #设置画刷
        #给图元设置标志，可选择，可设置焦点，可移动
        # diePathItem.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable|QGraphicsItem.ItemIsMovable)
        self.scene.addItem(diePathItem)

        #下模
        filePath = 'LD_1.json'
        path = diePath(filePath, 4, 500, 5 + 500)
        # self.path_list.append(path)
        diePathItem = QGraphicsPathItem()
        diePathItem.setPath(path)
        self.item_list.append(diePathItem)
        # diePathItem.setBrush(Qt.blue)  #设置画刷
        # diePathItem.setFlags(QGraphicsItem.ItemIsSelectable|QGraphicsItem.ItemIsFocusable|QGraphicsItem.ItemIsMovable)
        self.scene.addItem(diePathItem)

        self.on_pushButton_2_clicked()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        # pt_bend(length_list, angle_list, bend_list)
        length_list = [100]
        angle_list = []
        pt_list = pt_cal(length_list, angle_list)
        for pt in pt_list:
            pt[0] = -pt[0]
        
        #pathItem绘图
        pt_base = [500, 500] # 定位基点
        K = 1
        #先缩放，再平移
        for i in range(pt_list.__len__()):
            pt_list[i][0] = K * pt_list[i][0] + pt_base[0]#x = kx + x0
            pt_list[i][1] = -K * pt_list[i][1] + pt_base[1]#y = -ky +y0
#        print(pt_list)
        #pathItem绘图
        path = QPainterPath()
        path.moveTo(pt_list[0][0], pt_list[0][1]) # 移动到定位点
        for i in range(len(pt_list)):
            path.lineTo(pt_list[i][0], pt_list[i][1])    
        # path.closeSubpath() # 尾首相接封闭图形
        item = QGraphicsPathItem()
        item.setPath(path)
        self.scene.addItem(item)
        self.item_list.append(item)
        # self.graphicsView.setScene(self.scene)


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        length_list = [100, 100, 100, 100, 100, 100]
        angle_list = [90, 135, -90, 135, 90]
        bend_point = 1
        pt_list_left, pt_list_right = pt_bend_expand(length_list, angle_list, bend_point)
        path1, item1 = pathItem_bend_expand_draw(pt_list_left, 500, 500)
        self.scene.addItem(item1)
        path2, item2 = pathItem_bend_expand_draw(pt_list_right, 500, 500)
        self.scene.addItem(item2)
        path3, item3 = pathItem_bend_end_draw(pt_list_left, (180-135)/2, 500, 500)
        self.scene.addItem(item3)
        path4, item4 = pathItem_bend_end_draw(pt_list_right, -(180-135)/2, 500, 500)
        self.scene.addItem(item4)
        self.path_list.append(path1)
        self.path_list.append(path2)
        self.path_list.append(path3)
        self.path_list.append(path4)


    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        # item_list = self.scene.items() #返回一个栈列表
        # print('self.ItemList:', item_list)
        # print(item_list.__len__())
        # for m in range(item_list.__len__() - 1):
        #     for n in range(m, item_list.__len__()):
        #         if m != n:
        #             if item_list[m].collidesWithPath(item_list[n]):
        #                 print(m, n, '碰撞')
        """
        2022.3.11
        此方法存在bug, 可能需要重写collidesWithPath的shape()函数，
        后续再研究，不如直接解析法计算
        模具1，工件1明显不会干涉
        """
        print(self.item_list.__len__(), self.path_list.__len__())
        for i in range(self.item_list.__len__()):
            for j in range(self.path_list.__len__()):
                if self.item_list[i].collidesWithPath(self.path_list[j]):
                    print(i, j, 'collides')

        # itemChoosed = self.getItem(event)#获取当前选中对象
        #与所有的item都碰撞检查一遍(自己除外)
        # if itemChoosed != None:
        #     for i in range(len(itemList)):
        #         if i != self.getItemIndex(itemChoosed, itemList):
        #             if itemChoosed.collidesWithItem(itemList[i]) == True:
        #                 start =time.time()
        #                 itemInitiative = self.getItemIndex(itemChoosed, itemList)
        #                 itemPassive = self.getItemIndex(itemList[i], itemList)
        #                 print(itemInitiative,'与', itemPassive, '干涉碰撞')
        #                 end = time.time()
        #                 if end-start != 0:
        #                     print('运行时间：', end-start)

    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        # # self.graphicsView.setScene(self.scene)
        # #pathItem绘图
        # path = QPainterPath()
        # path.moveTo(100, 100)#移动到定位点
        # path.lineTo(150, 150)    
        # # path.closeSubpath()#尾首相接封闭图形
        # item1 = QGraphicsPathItem()
        # item1.setPath(path)
        # self.scene.addItem(item1)

        # path = QPainterPath()
        # path.moveTo(150, 150)#移动到定位点
        # path.lineTo(150, 200)    
        # # path.closeSubpath()#尾首相接封闭图形
        # item2 = QGraphicsPathItem()
        # item2.setPath(path)
        # self.scene.addItem(item2)
        # print(item1.collidesWithItem(item2))

        # print('self.path_list:', self.path_list)
        print(self.path_list.__len__())
        for m in range(self.path_list.__len__() - 1):
            for n in range(m, self.path_list.__len__()):
                if m != n:
                    if self.path_list[m].collidesWithPath(self.path_list[n]):
                        print(m, n, '碰撞')


    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GraphicsView_test()
    ui.show()
    sys.exit(app.exec_())

