import json
import DXF_tools

def dxf_to_json(dxf_path, json_path):
    """
    @fun: 将dxf文件编译为json类型的点集文件
    """
    list = DXF_tools.read_dxf(dxf_path, 0.5).DxfSample() # 第二个参数为精度
    # print(list)
    # 输出文件
    with open(json_path, 'w') as f:
        json.dump(list[0], f)
    # 读取程序数据文件
    with open(json_path, 'r') as fr:
        data = json.load(fr)
    print(data)

dxf_path = './resource/lowerDie/CADfile/LD_1_0.dxf' # ../相对路径，返回上一级
json_path = 'LD_1.json'
# 如果陷入死循环，有以下两种可能：
# 1. DXF图形开环
# 2. DXF图形中存在多余的线隐藏在图形中，一般由于删除不彻底被新线覆盖
dxf_to_json(dxf_path, json_path)