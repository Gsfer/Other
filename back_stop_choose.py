from pprint import pprint
from bend_and_expand_draw import pt_bend_expand

def location_point_generate(length_list, angle_dynamic_list, bend_point):

    # 求出所有可行定位点列表pt_list
    pt_list_left, pt_list_right = pt_bend_expand(length_list, angle_dynamic_list, bend_point)
    # print('pt_list_left',  pt_list_left)
    # print('pt_list_right', pt_list_right)

    pt_list_left.pop(0) # 该方法返回被删除的元素
    pt_list = list(reversed(pt_list_left)) # 反转列表，并覆盖原列表
    # print('pt_list_left after reverse',  pt_list_left)

    pt_list.extend(pt_list_right)
    # print('pt_list',  pt_list)

    # 计算左右两侧的备选的定位点和|x|max 值
    #左侧
    slice_list_left = pt_list[:bend_point + 1:]# 加一的原因是pt_list的中多两个端点
    # print('slice_list_left', slice_list_left)
    x_list_left = [abs(pt[0]) for pt in slice_list_left]
    # print('x_list_left', x_list_left)
    x_max_left = max(x_list_left)
    x_max_left_index = x_list_left.index(x_max_left) # 从零开始
    # print('x_max_left', x_max_left, 'x_max_left_index', x_max_left_index)

    for i in range(slice_list_left.__len__()-1, -1, -1):
        if i != 0:
            if angle_dynamic_list[i - 1] != 180:
                location_point_left = i # 这里的定位点考虑了端点情况，映射到角度列表上要减一
                break
        else:
            location_point_left = 0
    # print('location_point_left', location_point_left)

    #右侧
    slice_list_right = pt_list[bend_point + 2::]
    # print('slice_list_right', slice_list_right)
    x_list_right = [ pt[0] for pt in slice_list_right]
    # print('x_list_right', x_list_right)
    x_max_right = max(x_list_right)
    x_max_right_index = x_list_right.index(x_max_right) + bend_point + 2 # 从零开始
    # print('x_max_right', x_max_right, 'x_max_right_index', x_max_right_index)

    for i in range(slice_list_right.__len__()):
        if i != slice_list_right.__len__() - 1:
            if angle_dynamic_list[bend_point  + 1 + i] != 180:
                location_point_right = bend_point  + 2 + i # 这里的定位点考虑了端点情况，映射到角度列表上要加一
                break
        else:
            # location_point_right = bend_point + 1 + slice_list_right.__len__() - 1 + 1
            location_point_right = bend_point  + slice_list_right.__len__() + 1
    # print('location_point_right', location_point_right)
    return location_point_left, location_point_right, x_max_left, x_max_right

def location_point_choose(bend_point, location_point_left, location_point_right, x_max_left, x_max_right, precision_list):
    # 根据定位点是否相邻和精度要求选择定位点
    adjacent_marker_left = False # 待选左侧定位是否与当前折弯点邻接
    adjacent_marker_right = False # 待选右侧定位是否与当前折弯点邻接
    # 判断邻接
    if bend_point - (location_point_left - 1) == 1: # location_point_left 的值是考虑端点的
        adjacent_marker_left = True
    if location_point_right - 1 - bend_point == 1:
        adjacent_marker_right = True
    # print('adjacent_marker_left', adjacent_marker_left)
    # print('adjacent_marker_right', adjacent_marker_right)
    # 根据精度要求和前扩展要求选择定位点
    location_point = 0 # 定位点标记
    # 左右均相邻
    if adjacent_marker_left == True and adjacent_marker_right == True:
        # 折弯点两侧都有精度要求或者折弯点两侧均无精度要求
        if precision_list[bend_point + 1] == 2 or precision_list[bend_point + 1] == 0: 
            if x_max_left <= x_max_right:
                location_point = location_point_left
            else:
                location_point = location_point_right
        # 折弯点左侧有精度要求，右侧没有
        if precision_list[bend_point + 1] == -1: 
            location_point = location_point_left
        # 折弯点右侧有精度要求，左侧没有
        if precision_list[bend_point + 1] == 1: 
            location_point = location_point_right
    # 左邻而右不邻
    if adjacent_marker_left == True and adjacent_marker_right == False:
        # 折弯点两侧均无精度要求或者折弯点左侧没有而右侧有：
        # 即便右侧有精度要求，但是因为不和折弯点相邻，所以不优先
        if precision_list[bend_point + 1] == 0 or precision_list[bend_point + 1] == 1:
            if x_max_left <= x_max_right:
                location_point = location_point_left
            else:
                location_point = location_point_right
        # 折弯点左侧有精度要求而右侧没有或者折弯点两侧都有精度要求：
        if precision_list[bend_point + 1] == -1 or precision_list[bend_point + 1] == 2:
            location_point = location_point_left
    # 右邻而左不邻
    if adjacent_marker_left == False and adjacent_marker_right == True:
        if precision_list[bend_point + 1] == 0 or precision_list[bend_point + 1] == -1:
            if x_max_left <= x_max_right:
                location_point = location_point_left
            else:
                location_point = location_point_right
        if precision_list[bend_point + 1] == 1 or precision_list[bend_point + 1] == 2:
            location_point = location_point_right
    # 两侧都不邻
    if adjacent_marker_left == False and adjacent_marker_right == False:
        if x_max_left <= x_max_right:
            location_point = location_point_left
        else:
            location_point = location_point_right

    return location_point

if __name__ == '__main__':
    length_list = [60, 60, 60, 60, 60, 60, 60, 60, 60, 60] # N + 1
    angle_list = [90, 135, -90, 135, -90, 90, 135, -135, 90] # N
    bend_list = [4,  6,  3,  5,  7,  2,  8,  1, 0] # N
    # 考虑端点，右精度为1，左精度为-1，双精度为2，无精度为0
    precision_list = [0,0,0,0,0, 0 ,0,0,0,0,0] # N + 2
    location_point_list = [0 for i in range(angle_list.__len__())] # 定位点列表

    bend_point = 4
    angle_dynamic_list = [180 for i in range(length_list.__len__() - 1)]
    angle_dynamic_list[ bend_point ] = angle_list[ bend_point ]
    angle_dynamic_list[ 2 ] = angle_list[ 2 ]
    # angle_dynamic_list[ 3 ] = angle_list[ 3 ]
    angle_dynamic_list[ 5 ] = angle_list[ 5 ]
    angle_dynamic_list[ 7 ] = angle_list[ 7 ]

    location_point_left, location_point_right, x_max_left, x_max_right = \
    location_point_generate(length_list, angle_dynamic_list, bend_point)

    location_point = location_point_choose(bend_point, location_point_left, location_point_right, x_max_left, x_max_right, precision_list)
    location_point_list[bend_point] = location_point # location_point 从零开始，考虑端点
    print('location_point_list', location_point_list)
