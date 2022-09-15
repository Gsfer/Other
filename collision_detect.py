from bend_and_expand_draw import pt_bend_expand, pathItem_bend_expand_draw, pathItem_bend_end_draw

#Python3.6
class point(): # 定义类
    def __init__(self,x,y):
        self.x=x
        self.y=y   

def cross(p1,p2,p3):# 跨立实验
    x1=p2.x-p1.x
    y1=p2.y-p1.y
    x2=p3.x-p1.x
    y2=p3.y-p1.y
    return x1*y2-x2*y1     

def IsIntersec(x1,y1,x2,y2,x3,y3,x4,y4): # 判断两线段是否相交
    p1 = point(x1, y1)
    p2 = point(x2, y2)
    p3 = point(x3, y3)
    p4 = point(x4, y4)

    #快速排斥，以l1、l2为对角线的矩形必相交，否则两线段不相交
    if(max(p1.x,p2.x)>=min(p3.x,p4.x)    #矩形1最右端大于矩形2最左端
    and max(p3.x,p4.x)>=min(p1.x,p2.x)   #矩形2最右端大于矩形最左端
    and max(p1.y,p2.y)>=min(p3.y,p4.y)   #矩形1最高端大于矩形最低端
    and max(p3.y,p4.y)>=min(p1.y,p2.y)): #矩形2最高端大于矩形最低端

    #若通过快速排斥则进行跨立实验
        if(cross(p1,p2,p3)*cross(p1,p2,p4)<=0
           and cross(p3,p4,p1)*cross(p3,p4,p2)<=0):
            return True
        else:
            return False
    else:
        return False

def collision_mold_and_part(pt_mold, pt_part):
    """
    @fun: 对输入的模具点集和工件点集进行干涉检查
    @para: pt_mold[]: 模具
           pt_part[]: 工件
    """
    line_mold = []
    line_part = []
    for n in range(pt_mold.__len__()):
        if n != pt_mold.__len__() - 1:
            x1, y1 = pt_mold[n][0], pt_mold[n][1]
            x2, y2 = pt_mold[n + 1][0], pt_mold[n + 1][1]
            line_mold.append([x1, y1, x2, y2])
        else: # 模具需要首尾相接
            x1, y1 = pt_mold[n][0], pt_mold[n][1]
            x2, y2 = pt_mold[0][0], pt_mold[0][1]
            line_mold.append([x1, y1, x2, y2])
    # print('line_mold', line_mold)
    for n in range(pt_part.__len__() - 1):
        x1, y1 = pt_part[n][0], pt_part[n][1]
        x2, y2 = pt_part[n + 1][0], pt_part[n + 1][1]
        line_part.append([x1, y1, x2, y2])
    # print('line_part', line_part)
    # 干涉检查
    for m in range(line_part.__len__()):
        for n in range(line_mold.__len__()):
            x1, y1, x2, y2 \
            = line_part[m][0], line_part[m][1], line_part[m][2], line_part[m][3]
            x3, y3, x4, y4 \
            = line_mold[n][0], line_mold[n][1], line_mold[n][2], line_mold[n][3]
            # result = IsIntersec(x1, y1, x2, y2, x3, y3, x4, y4)
            # print(m, n, result)
            if IsIntersec(x1, y1, x2, y2, x3, y3, x4, y4):
                print(m, n, 'collision')
                return True 
    return False 

def process_impack_check(bend_list, length_list, angle_list, pt_upper_die, pt_lower_die,
                        base_point, upper_offset):
    """
    @fun: 根据折弯工序进行各个工步的干涉检查
    @para: bend_list[]: 折弯工步序列
            length_list[]: 长度序列
            angle_list[]: 角度序列
            pt_upper_die[point[x, y]]: 上模绘图点序列(不封闭，需要手动封闭)
            pt_lower_die[point[x, y]]: 下模绘图点序列(不封闭，需要手动封闭)
            base_point[x, y]: 定位基点坐标，用于定位展开工件
            upper_offset: 上模相对定位基点在纵轴负方向上的偏移量，用于定位折弯后的工件
    # TODO: 模具输入应该为一套，当前只考虑一种模具的情况，后续补充完整模具
    """
    # 动态角度列表，按工步顺序输出角度序列的变化过程
    angle_dynamic_list = [180 for i in range(length_list.__len__() - 1)]
    # 干涉检测主循环
    for n in range(bend_list.__len__()):
        # 折弯点
        bend_point = bend_list[n]
        # 动态角度列表
        angle_dynamic_list[ bend_point ] = angle_list[ bend_point ]
        # 干涉检测
        print('current bend:', bend_point)
        print('angle_dynamic_list', angle_dynamic_list)
        item_list, path_list, impact_count = \
        work_step_impact_check(bend_point, length_list, angle_dynamic_list, pt_upper_die, pt_lower_die,
                            base_point, upper_offset)
        print('impact_count', impact_count, '\n')
                
def work_step_impact_check(bend_point, length_list, angle_list, pt_upper_die, pt_lower_die, 
                            base_point, upper_offset):
    """
    @fun: 根据折弯点和加工信息判断工件在折弯前后是否与上模和下模干涉
    @para: check_direction: 碰撞检查的方向，即工件摆放的方向，分为左和右
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
    # 角度这里用绝对值！！！
    bend_angle = abs(angle_list[bend_point])
    x_base, y_base = base_point[0], base_point[1]
    pt_list_left, pt_list_right = pt_bend_expand(length_list, angle_list, bend_point)
    pt_left_move, path1, item1 = \
    pathItem_bend_expand_draw(pt_list_left, x_base, y_base)
    item_list.append(item1)
    path_list.append(path1)
    pt_right_move, path2, item2 = \
    pathItem_bend_expand_draw(pt_list_right, x_base, y_base)
    item_list.append(item2)
    path_list.append(path2)
    pt_left_rot, path3, item3 = \
    pathItem_bend_end_draw(pt_list_left, (180 - bend_angle) / 2, x_base, y_base - upper_offset)
    item_list.append(item3)
    path_list.append(path3)
    pt_right_rot, path4, item4 = \
    pathItem_bend_end_draw(pt_list_right, - (180 - bend_angle) / 2, x_base, y_base - upper_offset)
    item_list.append(item4)
    path_list.append(path4)
    # 干涉检查使用点集完成
    # 上模与展开件左侧干涉检查
    if collision_mold_and_part(pt_upper_die, pt_left_move):
        impact_count += 1
        print('upper die collides with expanded part on left')
    # 上模与展开件右侧干涉检查
    if collision_mold_and_part(pt_upper_die, pt_right_move):
        impact_count += 1
        print('upper die collides with expanded part on right')
    # 上模与折弯件左侧干涉检查
    if collision_mold_and_part(pt_upper_die, pt_left_rot):
        impact_count += 1
        print('upper die collides with bended part on left')
    # 上模与折弯件右侧干涉检查
    if collision_mold_and_part(pt_upper_die, pt_right_rot):
        impact_count += 1
        print('upper die collides with bended part on right')
    # 下模与展开件左侧干涉检查
    if collision_mold_and_part(pt_lower_die, pt_left_move):
        impact_count += 1
        print('lower die collides with expanded part on left')
    # 下模与展开件右侧干涉检查
    if collision_mold_and_part(pt_lower_die, pt_right_move):
        impact_count += 1
        print('lower die collides with expanded part on right')
    # 下模与折弯件左侧干涉检查
    if collision_mold_and_part(pt_lower_die, pt_left_rot):
        impact_count += 1
        print('lower die collides with bended part on left')
    # 下模与折弯件右侧干涉检查
    if collision_mold_and_part(pt_lower_die, pt_right_rot):
        impact_count += 1
        print('lower die collides with bended part on right')

    return item_list, path_list, impact_count

if __name__ == '__main__':
    print(IsIntersec(0,0,100,0,100,0,101,0))