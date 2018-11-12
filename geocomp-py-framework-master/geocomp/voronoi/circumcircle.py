import math
from geocomp.common.point import Point
import numpy as np

from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.segment import Segment

def mid_point(p1, p2):
    """Encontra o ponto médio entre dois pontos"""
    return Point((p1.x + p2.x)/2, (p1.y + p2.y)/2)

def get_line(p1, p2):
    """Encontra a reta que corta dois pontos"""
    slope = (p2.y - p1.y)/(p2.x - p1.x)
    y_int = p1.y - slope * p1.x
    return (slope, y_int)

def perp_slope(line):
    """Encontra o coeficiente angula da reta perpedicular"""
    return -1 / line[0]

def get_line_from_slope(slope, point):
    """Encontra a reta dado um ponto e seu coeficiente angular"""
    return (slope, point.y - slope*point.x)

def intersection(line1, line2):
    """Encontra o ponto de interseção de duas retas"""
    x = (line2[1] - line1[1])/(line1[0] - line2[0])
    y = line1[0] * x + line1[1]
    return Point(x, y)

def distance(p1, p2):
    """Retorna a distância entre dois pontos"""
    return math.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def circumcenter(p1, p2, p3):
    """Encontra o cicuncentro de três pontos"""
    mid1 = mid_point(p1, p2)
    mid2 = mid_point(p2, p3)

    line1 = get_line(p1, p2)
    line2 = get_line(p2, p3)

    perp1 = perp_slope(line1)
    perp2 = perp_slope(line2)

    bissect1 = get_line_from_slope(perp1, mid1)
    bissect2 = get_line_from_slope(perp2, mid2)

    f1 = lambda x : bissect1[0] * x + bissect1[1]
    f2 = lambda x : bissect2[0] * x + bissect2[1]

    p1, p2 = Point(-100, f1(-100)), Point(100, f1(100))
    p1.lineto(p2)

    p3, p4 = Point(-100, f2(-100)), Point(100, f2(100))
    p3.lineto(p4)

    inter = intersection(bissect1, bissect2)

    inter.plot()
    control.sleep()
    control.thaw_update()
    control.update()

    p1.remove_lineto(p2)
    p3.remove_lineto(p4)
    inter.unplot()
    return inter
