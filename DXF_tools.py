import matplotlib.pyplot as plt, math, numpy as np
import dxfgrabber
# import DXFtools
from shapely.geometry import LinearRing
class read_dxf():
    def __init__(self, file, Inter_acc):
        self.Inter_acc = Inter_acc
        self.dxf_doc = dxfgrabber.readfile(file)
        
    def dxf_dots(self,dxf_doc):
        dots = list()
        for e in dxf_doc.entities:
            if e.dxftype == 'LINE':
                x0 = float('%.4f' % e.start[0])
                y0 = float('%.4f' % e.start[1])
                x1 = float('%.4f' %e.end[0])
                y1 = float('%.4f' %e.end[1])
                line = ['L', [[x0,y0],[x1,y1]]]
                dots.append(line)
            elif e.dxftype == 'ARC':
                A_x = float('%.4f' % e.center[0])
                A_y = float('%.4f' % e.center[1])
                r = float('%.4f' %  e.radius)
                start_angle = e.start_angle
                end_angle = e.end_angle
                arc_points = points_on_arc([A_x,A_y],r,start_angle,end_angle, int(r * self.Inter_acc))
                arc = ['ARC',[[A_x,A_y],r,start_angle,end_angle],arc_points]
                dots.append(arc)
            elif e.dxftype == 'CIRCLE':
                C_x = float('%.4f' % e.center[0]) 
                C_y = float('%.4f' % e.center[1])
                R = float('%.4f' % e.radius) 
                c = ['C',[C_x,C_y],R]
                dots.append(c)
            elif e.dxftype == 'POLYLINE':
                points = points_on_spline(e.points)
                spline = ['SPLINE',points]
                dots.append(spline)
        return dots

    def DxfSample(self):
        """
        整理dxf文件中读取出来的点集，将属于同一样片中的点放入一个列表中
        Args:
            dots ([list]): lists of dots
        Returns:
            a list of samples
        """
        dots = self.dxf_dots(self.dxf_doc)
        Samples = list()
        for dot in dots:
            if dot[0] == 'C': 
                pt = points_on_circle(dot[1], dot[2] , int(dot[2] * self.Inter_acc))
                Samples.insert(0,pt)
                del dots[dots.index(dot)]
        while len(dots) > 0:                            
            Sample_temp = dots[0][-1]
            del dots[0]
            while len(dots) >= 0:
                if CoPoints(Sample_temp):
                    for i in range(len(dots)): 
                        if abs(dots[i][-1][0][0] - Sample_temp[-1][0]) < 0.001 and abs(dots[i][-1][0][1] - Sample_temp[-1][1]) < 0.001:
                            if dots[i][0] =="L":
                                Sample_temp.append(dots[i][-1][-1])
                            else:
                                for j in range(len(dots[i][-1])):
                                    Sample_temp.append(dots[i][-1][j])
                            del dots[i]
                            break
                        elif abs(dots[i][-1][-1][0] - Sample_temp[-1][0]) < 0.001 and abs(dots[i][-1][-1][1] - Sample_temp[-1][1]) < 0.001:
                            # 变换位置
                            dots[i][-1].reverse()
                            if dots[i][0] =="L":
                                Sample_temp.append(dots[i][-1][-1])
                            else:
                                for k in range(len(dots[i][-1])):
                                    Sample_temp.append(dots[i][-1][k])
                            del dots[i]
                            break
                
                if CoPoints1(Sample_temp):
                    del Sample_temp[-1]
                    ring = LinearRing(Sample_temp)
                    if ring.is_ccw:
                        Samples.append(Sample_temp)
                    else:
                        Sample_temp.reverse()
                        Samples.append(Sample_temp)
                    break
        return Samples

def CoPoints(dot):
    if abs(dot[-1][0] - dot[0][0]) > 0.001 or abs(dot[-1][1] - dot[0][1]) > 0.001:
        return True
    else:
        return False
    
def CoPoints1(dot):
    if abs(dot[-1][0] - dot[0][0]) < 0.001 and abs(dot[-1][1] - dot[0][1]) < 0.001: 
        return True
    else:
        return False  

def points_on_arc(
    center,
    radius: float,
    theta_start: float,
    theta_end: float,
    spacing: float):
    
    """Generate points along an arc.
    Args:
        center: The center of the arc.
        radius: The radius of the arc.
        theta_start: The starting position in degrees.
        theta_end: The ending position in degrees.
        spacing: The approximate distance between adjacent points.
    Returns:
        A list of points."""
    
    theta_start = theta_start * math.pi / 180
    theta_end = theta_end * math.pi / 180
    if theta_start > theta_end:
        theta_start = theta_start - 2 * np.pi
    theta = float(theta_end - theta_start)
    n_points = int(abs(theta) * radius / spacing) + 1
    theta_p = np.linspace(theta_start, theta_end,n_points)
    return [endpoint(center, t, radius) for t in theta_p]

def points_on_circle(center,radius,spacing):
    theta_start = 0
    theta_end = 2 * np.pi
    n_points = int(2 * np.pi * radius / spacing) + 1
    theta_p = np.linspace(theta_start, theta_end ,n_points)
    return [endpoint(center, t, radius) for t in theta_p]

def points_on_spline(pts):
    sp = []
    for pt in pts:
        temp_sp = [pt[0],pt[1]]
        sp.append(temp_sp)
    return sp

def endpoint(start, angle: float, distance: float):
    """
    Args:
        start: Starting point.
        angle: Direction from starting point in radians.
        distance: Distance from starting point.
    Returns:
        A point ``distance`` from ``start`` in the direction ``angle``.
    """
    x = start[0] + math.cos(angle) * distance
    y = start[1] + math.sin(angle) * distance
    return [x, y]

def showResult(Samples):
    for sample in Samples:
        x_list = [sample[i][0] for i in range(len(sample))]
        x_list.append(sample[0][0])
        y_list = [sample[i][1] for i in range(len(sample))]
        y_list.append(sample[0][1])
        plt.plot(x_list, y_list)
    plt.show()


