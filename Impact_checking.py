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
from collision_detect import collision_mold_and_part
from back_stop_choose import location_point_generate, location_point_choose

from Ui_GraphicsView_test import Ui_Form

class GraphicsView_test(QWidget, Ui_Form):
    """
    Class documentation goes here.
    """
    run_signal = pyqtSignal(int ,list, list, list)

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

        self.location_point_list = [0 for i in range(19)] # 定位点列表
        # self.on_pushButton_clicked()
        self.work_step_num = 0
        self.run_signal.connect(self.run_process)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        # 17
        length_list = [60, 60, 60, 60, 60, 60, 60, 60, 100, 60, 60, 60, 60, 60,100, 60, 60,60]
        angle_list = [90, 135, -135, -135, 135, -90, 90, -90, -135, 135, 135,-135, -135,135, 90, -90,90]
        bend_list = [0, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
        precision_list = [0, 0, 1, 2, -1, 0, 0, 0, 0, 1, 2, -1, 0, 0,0, 0, 0,0,0]

        # # 9
        # length_list = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60]
        # angle_list = [90, 135, -90, 135, -90, 90, 135, -135, 90]
        # bend_list = [4,  6,  3,  5,  7,  2,  8,  1, 0]
        # precision_list = [0,0,0,0,1, 2 ,-1,0,0,0,0]
        
        # # 5 测试
        # length_list = [60, 60, 60, 60, 60, 60]
        # angle_list = [90, -135, 90, -135, 90]
        # bend_list = [2, 4 ,5 , 3, 1]
        # precision_list = [0,0,0,0,1, 2 ,-1]
        # 5 论文数据来源
        # length_list = [60, 100, 70, 50, 80, 60]
        # angle_list = [90, -135, 90, -135, 90]
        # bend_list = [1,3,4,2,0]
        # precision_list = [0,0,0,0,1, 2 ,-1]

        # bend_list = [0,1,2,3,4]
        
        bend_point = bend_list[self.work_step_num]
        
        angle_dynamic_list = [180 for i in range(length_list.__len__() - 1)]
        for n in range(self.work_step_num + 1):
            bend_point = bend_list[n]
            angle_dynamic_list[ bend_point ] = angle_list[ bend_point ]

        if self.work_step_num != bend_list.__len__() - 1:
            self.run_signal.emit(bend_point, length_list, angle_dynamic_list, precision_list)
            self.work_step_num += 1
        else:
            self.run_signal.emit(bend_point, length_list, angle_dynamic_list, precision_list)
            self.work_step_num = 0

    @pyqtSlot(int, list, list, list)
    def run_process(self, bend_point, length_list, angle_dynamic_list, precision_list):
        itemList = self.scene.items()
        if itemList.__len__() > 4:
            for i in range(4):
                self.scene.removeItem(itemList[i])

        print('current bend:', bend_point)
        print('angle_dynamic_list', angle_dynamic_list)
        #求左右两个定位点
        location_point_left, location_point_right, x_max_left, x_max_right = \
        location_point_generate(length_list, angle_dynamic_list, bend_point)
        print('location:',location_point_left, location_point_right, x_max_left, x_max_right)
        #干涉检查
        #右定位干涉检查
        right_position_mark = True
        item_list_right, path_list, impact_count_right = \
        work_step_impact_check(right_position_mark, bend_point, length_list, angle_dynamic_list, self.pt_upper_die, self.pt_lower_die,
                                [500, 500], 50)
        # print('right_impact_count', impact_count_right, '\n')
        #左定位干涉检查
        right_position_mark = False
        item_list_left, path_list, impact_count_left = \
        work_step_impact_check(right_position_mark, bend_point, length_list, angle_dynamic_list, self.pt_upper_die, self.pt_lower_die,
                                [500, 500], 50)
        # print('impact_count_left', impact_count_left, '\n')

        if impact_count_right != 0 and impact_count_left != 0:
            print('两者均碰撞')
            location_point = -1
        if impact_count_right == 0 and impact_count_left != 0:
            location_point = location_point_right
        if impact_count_right != 0 and impact_count_left == 0:
            location_point = location_point_left
        if impact_count_right == 0 and impact_count_left == 0:
            location_point = location_point_choose(bend_point, location_point_left, location_point_right, x_max_left, x_max_right, precision_list)
        print('location_point', location_point)
        self.location_point_list[bend_point] = location_point # location_point 从零开始，考虑端点
        print('location_list', self.location_point_list)

        if location_point - 1 > bend_point:
            item_list = item_list_right
        else:
            item_list = item_list_left
        for item in item_list:
            self.scene.addItem(item)
        self.graphicsView.setScene(self.scene)
        # self.graphicsView.show()

def work_step_impact_check(right_position_mark, bend_point, length_list, angle_list, pt_upper_die, pt_lower_die, 
                            base_point, upper_offset):
    """
    @fun: 根据折弯点和加工信息判断工件在折弯前后是否与上模和下模干涉
    @para: right_position_mark: 右定位标记，为True表示工件为默认的右向定位
            bend_point(int): 折弯序列, [0, angle_list.__len__())
             length_list[]: 长度序列
             angle_list[]: 角度序列
             pt_upper_die[point[x, y]]: 上模绘图点序列(不封闭，需要手动封闭)
             pt_lower_die[point[x, y]]: 下模绘图点序列(不封闭，需要手动封闭)
             base_point[x, y]: 定位基点坐标，用于定位展开工件
             upper_offset: 上模相对定位基点在纵轴负方向上的偏移量，用于定位折弯后的工件      
    """
    # 可视化测试用
    item_list = []
    path_list = []
    # 碰撞计数器
    impact_count = 0
    bend_angle = abs(angle_list[bend_point])
    x_base, y_base = base_point[0], base_point[1]
    #根据右定位标记调整pt_list_left, pt_list_right
    if right_position_mark == True:
        pt_list_left, pt_list_right = pt_bend_expand(length_list, angle_list, bend_point)
    else:
        pt_list_right, pt_list_left = pt_bend_expand(length_list, angle_list, bend_point)
        pt_list_left = [ [-pt[0],pt[1]] for pt in pt_list_left]
        pt_list_right = [ [-pt[0],pt[1]] for pt in pt_list_right]
    # #检查工件点坐标
    # print('pt_list_left',  pt_list_left)
    # print('pt_list_right', pt_list_right)
    # 计算展开时的相对定位基点的点集
    pt_left_move, path1, item1 = \
    pathItem_bend_expand_draw(pt_list_left, x_base, y_base)
    pt_right_move, path2, item2 = \
    pathItem_bend_expand_draw(pt_list_right, x_base, y_base)

    # 折弯后点集
    pt_left_rot, path3, item3 = \
    pathItem_bend_end_draw(pt_list_left, (180 - bend_angle) / 2, x_base, y_base - upper_offset)
    pt_right_rot, path4, item4 = \
    pathItem_bend_end_draw(pt_list_right, - (180 - bend_angle) / 2, x_base, y_base - upper_offset)

    item_list.append(item1)
    path_list.append(path1)
    item_list.append(item2)
    path_list.append(path2)
    item_list.append(item3)
    path_list.append(path3)
    item_list.append(item4)
    path_list.append(path4)

    if collision_mold_and_part(pt_upper_die, pt_left_move):
        impact_count += 1
        print('upper die collides with expanded part on left')

    if collision_mold_and_part(pt_upper_die, pt_right_move):
        impact_count += 1
        print('upper die collides with expanded part on right')
    
    if collision_mold_and_part(pt_upper_die, pt_left_rot):
        impact_count += 1
        print('upper die collides with bended part on left')

    if collision_mold_and_part(pt_upper_die, pt_right_rot):
        impact_count += 1
        print('upper die collides with bended part on right')
    
    if collision_mold_and_part(pt_lower_die, pt_left_move):
        impact_count += 1
        print('lower die collides with expanded part on left')

    if collision_mold_and_part(pt_lower_die, pt_right_move):
        impact_count += 1
        print('lower die collides with expanded part on right')
    
    if collision_mold_and_part(pt_lower_die, pt_left_rot):
        impact_count += 1
        print('lower die collides with bended part on left')

    if collision_mold_and_part(pt_lower_die, pt_right_rot):
        impact_count += 1
        print('lower die collides with bended part on right')

    return item_list, path_list, impact_count

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = GraphicsView_test()
    ui.show()
    sys.exit(app.exec_())

