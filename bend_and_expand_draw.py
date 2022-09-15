import math, numpy as np, ast, json
from PyQt5.QtGui import QPainterPath
from PyQt5.QtWidgets import (QWidget, QApplication,QGraphicsScene,QGraphicsView,QGraphicsRectItem,QMainWindow,QLabel,QGraphicsItem,
QGraphicsPathItem, QGraphicsLineItem)
from PyQt5.QtCore import Qt,pyqtSignal, pyqtSlot, QPoint,QRectF
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets

def calLength(x1, y1, x2, y2):
    """
    求线段长度
    """
    vx = x2 - x1
    vy = y2 - y1
    length = math.sqrt(vx**2 + vy**2)
    return length

def ptExtend(length, startX, startY, endX, endY):
    """
    @fun: 求解直线延伸或压缩后的新点
    @para: start(X, Y): 起始点
            end(X, Y): 结束点
    """
    oldLength =calLength(startX, startY, endX, endY)
    L = length/oldLength
    xN = startX + L*(endX - startX)
    yN = startY + L*(endY - startY)
    return xN, yN
    
def ptRotation(angle, cenX, cenY, rotX, rotY):
    #求向两个方向旋转后的点
    angle = angle*(np.pi/180)
    rotXN = (rotX - cenX)*math.cos(angle) - (rotY - cenY)*math.sin(angle) + cenX
    rotYN = (rotX - cenX)*math.sin(angle) + (rotY - cenY)*math.cos(angle) + cenY
    return rotXN, rotYN

def pt_cal(length_list, angle_list):
    """
    @fun: 求解从左到右方向的折线段，做一个镜像可以得出左侧的
    @para: length_list: 长度列表
            angle_list: 角度列表(比长度列表少一个元素)
    """
    # 折弯点列表
    pt_list = [[0, 0]]
    # 处理第一段特殊情况
    x_1 = length_list[0]
    y_1 = 0
    pt_list.append([x_1, y_1])
    # 后面以一个折弯点加一段直线的形式重复
    for n in range(angle_list.__len__()):
        length = length_list[n + 1]
        x_rot_base, y_rot_base = pt_list[-1][0], pt_list[-1][1]
        endX, endY = pt_list[-2][0], pt_list[-2][1]
        x_temp, y_temp = ptExtend(length, x_rot_base, y_rot_base, endX, endY)
        angle = angle_list[n]
        x_rot, y_rot = ptRotation(angle, x_rot_base, y_rot_base, x_temp, y_temp)
        pt_list.append([x_rot, y_rot])
    return pt_list

def pt_bend_expand(length_list, angle_list, bend_point):
    """
    @fun: 求解折弯件按折弯点展开后的长度和角度序列，分为左序列和右序列
    @oara: length_list[]: 折弯长度序列
            angle_list[]: 折弯角度序列
            bend_point(int): 折弯点(折弯角表示), 从0开始计数，0为第一个折弯点，而不是工件起点
    """
    # 存放折弯点左侧的长度序列，与原长度序列的方向相反
    # 从后向前切片列表
    length_list_left = [length_list[i] for i in range( bend_point, -1, -1 )]
    # 存放折弯点右侧的长度序列，与原长度序列的方向相同
    # 从前向后切片列表
    length_list_right = [length_list[i] for i in range( bend_point + 1, length_list.__len__() )]
    # 存放折弯点左侧的角度序列，与原角度序列的方向相反
    # 从后向前切片列表，不包含折弯点
    angle_list_left = [angle_list[i] for i in range( bend_point - 1, -1, -1 )]
    # for n in range(angle_list_left.__len__()): # 由于绘图时左半部分由右半部分翻转，所以角度要取反
    #     if angle_list_left[n] != 180:
    #         angle_list_left[n] = - angle_list_left[n]
    # print('angle_list_left', angle_list_left)
    # 存放折弯点左侧的角度序列，与原角度序列的方向相反
    # 从前向后切片列表，不包含折弯点
    angle_list_right = [angle_list[i] for i in range( bend_point + 1, angle_list.__len__() )]
    # 测试代码
    # print('length_list_left',length_list_left,
    #         '\nlength_list_right',length_list_right,
    #         '\nangle_list_left', angle_list_left,
    #         '\nangle_list_right',angle_list_right)
    # 折弯点列表
    # 左序列由右序列镜像得到
    pt_list_left = pt_cal(length_list_left, angle_list_left)
    for n in range(pt_list_left.__len__()): # 已纵轴为基准镜像
        pt_list_left[n][0] = -pt_list_left[n][0]
    pt_list_right = pt_cal(length_list_right, angle_list_right)
    # 当展开处的折弯角为负值时，以横轴为基准镜像左序列和右序列
    if angle_list[bend_point] < 0:
        for n in range(pt_list_left.__len__()):
            pt_list_left[n][1] = - pt_list_left[n][1]
        for n in range(pt_list_right.__len__()):
            pt_list_right[n][1] = - pt_list_right[n][1]
    return pt_list_left, pt_list_right

def pt_bend_move(pt_list, x_base, y_base):
    """
    @fun: 将输入列表中的点以base点为基准移动
    """
    # 新建列表存储修改后的值，防止修改传入的列表
    pt_move = [] 
    # pathItem绘图
    pt_base = [x_base, y_base] # 定位基点
    K = 1
    #先缩放，再平移
    # for i in range(pt_list.__len__()):
    for i in range(pt_list.__len__()):
        # pt_list[i][0] = K * pt_list[i][0] + pt_base[0] # x = kx + x0
        # pt_list[i][1] = K * pt_list[i][1] + pt_base[1] # y = ky +y0
        pt_move.append([K * pt_list[i][0] + pt_base[0], K * pt_list[i][1] + pt_base[1]])
    return pt_move   

def pathItem_bend_expand_draw(pt_list, x_base, y_base):
    """
    @fun: 使用pathitem折弯绘制折弯展开图
    @para: pt_list: 点列表
            base(X, Y): 定位基点
    """
    pt_move_list = pt_bend_move(pt_list, x_base, y_base)
    #pathItem绘图
    path = QPainterPath()
    path.moveTo(pt_move_list[0][0], pt_move_list[0][1]) # 移动到定位点
    for i in range(pt_move_list.__len__()):
        path.lineTo(pt_move_list[i][0], pt_move_list[i][1])    
    # path.closeSubpath() # 尾首相接封闭图形
    item = QGraphicsPathItem()
    item.setPath(path)
    return pt_move_list, path, item

def pt_bend_rot(pt_list, rot_angle, x_base, y_base):
    """
    @fun: 求解列表中点以某点为基准旋转指定角度的后的点坐标
    """
    pt_rot_list = []
    for n in range(pt_list.__len__()):
        # pt_list[n][0], pt_list[n][1] = ptRotation(rot_angle, 0, 0, pt_list[n][0], pt_list[n][1])
        x_rot, y_rot = ptRotation(rot_angle, x_base, y_base, pt_list[n][0], pt_list[n][1])
        pt_rot_list.append([x_rot, y_rot])
    # print('pt_rot_list', pt_rot_list)
    return pt_rot_list

def pathItem_bend_end_draw(pt_list, rot_angle, x_base, y_base):
    """
    @fun: 折弯完成绘图
    @para: pt_list: 点列表
           rot_angle: 旋转角
            base(X, Y): 定位基点
    """
    # 这里由于要调用pathItem_bend_expand_draw,所以只对点进行旋转，移动和绘图的工作由pathItem_bend_expand_draw完成
    pt_rot = pt_bend_rot(pt_list, rot_angle, 0, 0) # base(0, 0)!!!
    pt_rot_list, path, item = pathItem_bend_expand_draw(pt_rot, x_base, y_base)
    return pt_rot_list, path, item

def diePath(filePath, K, baseX, baseY):
    #读取模具几何信息
    f = open(filePath, mode='r')
    # ptList = ast.literal_eval(f.readlines()[0])#将文本型的列表转换为数值型列表
    #处理点集，当参考点为(0,0)时，坐标映射x = x + x0 ,y = -y +y0（关于x=x0对称）
    ptList = json.load(f)
    basePt = [baseX, baseY]#定位基点
    #先缩放，再平移
    for i in range(len(ptList)):
        ptList[i][0] = K*ptList[i][0] + basePt[0] #x = kx + x0
        ptList[i][1] = -K*ptList[i][1] + basePt[1] #y = -ky +y0
#        print(ptList)
    #pathItem绘图
    path = QPainterPath()
    path.moveTo(ptList[0][0], ptList[0][1])#移动到定位点
    for i in range(len(ptList)):
        path.lineTo(ptList[i][0], ptList[i][1])    
    path.closeSubpath()#尾首相接封闭图形  
    return ptList, path
    
    







        


