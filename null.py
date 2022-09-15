length_list = [100,700,300,400,500,600,900,1000]
angle_list = [90,45,20,-45,45,60,90]
bend_point = 4

#切片测试
length_list_left = [length_list[i] for i in range(bend_point, -1, -1)]
length_list_right = [length_list[i] for i in range( bend_point + 1, length_list.__len__() ) ]
angle_list_left = [angle_list[i] for i in range(bend_point - 1, -1, -1)]
angle_list_right = [angle_list[i] for i in range( bend_point + 1, angle_list.__len__() ) ]
# print('length_list_left',length_list_left,
#     '\nlength_list_right',length_list_right,
#     '\nangle_list_left', angle_list_left,
#     '\nangle_list_right',angle_list_right)

# for n in range(angle_list.__len__()):
#     print(n, angle_list[n])

# print(angle_list.__len__())
# print(angle_list[-1])

# item_list = [1,2,3,4,5,6]
# for m in range(item_list.__len__()-1):
#     for n in range(m, item_list.__len__()):
#         if m != n:
#         # if item_list[m].collidesWithItem(item_list[n]):
#             print(m, n)


# pt_mold = [[1,2],[12,23],[2,45],[6,7]]
# pt_part = [[1,2],[12,23],[2,45],[6,7]]
# line_mold = []
# line_part = []
# for n in range(pt_mold.__len__()):
#     if n != pt_mold.__len__() - 1:
#         x1, y1 = pt_mold[n][0], pt_mold[n][1]
#         x2, y2 = pt_mold[n + 1][0], pt_mold[n + 1][1]
#         line_mold.append([x1, y1, x2, y2])
#     else: # 模具需要首尾相接
#         x1, y1 = pt_mold[n][0], pt_mold[n][1]
#         x2, y2 = pt_mold[0][0], pt_mold[0][1]
#         line_mold.append([x1, y1, x2, y2])
# # print('line_mold', line_mold)
# for n in range(pt_part.__len__() - 1):
#     x1, y1 = pt_part[n][0], pt_part[n][1]
#     x2, y2 = pt_part[n + 1][0], pt_part[n + 1][1]
#     line_part.append([x1, y1, x2, y2])
# print(line_part)

# import time
# length_list = [60, 60, 60, 60, 60, 60]
# angle_list = [90, 135, -90, 135, -90]
# bend_list = [0, 1, 4, 3, 2]

# angle_dynamic_list = [180 for i in range(length_list.__len__() - 1)]
# for n in range(bend_list.__len__()):
#     angle_dynamic_list[ bend_list[n] ] = angle_list[ bend_list[n] ]
#     print('angle_dynamic_list', angle_dynamic_list)
#     time.sleep(1)

#列表反转测试
a = [1,23,4,5,7,8,90]
b = list(reversed(a))
print(a)
print(b)




