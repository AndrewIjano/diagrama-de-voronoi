#!/usr/bin/env python
"""Algoritmo de Fortune"""

# from geocomp.common.polygon import Polygon
from geocomp.common import control
from geocomp.common.guiprim import *
from queue import PriorityQueue
from pqdict import pqdict
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.voronoi.DCEL import DCEL
from geocomp.voronoi.BST import BST
from geocomp.voronoi.circumcircle import circumcenter, distance
import math
class Event():
	def __init__(self, point, is_site_event, leaf=None, center=None):
		self.point = point
		self.is_site_event = is_site_event
		self.leaf = leaf
		self.center = center

	def __str__(self):
		return f'({self.point.x}, {self.point.y})'

def event_queue(P):
	events = [Event(p, True) for p in P]
	Q = pqdict({e : e.point.y for e in events}, reverse=True)
	return Q

def Fortune(P):
	Q = event_queue(P)
	V = DCEL()
	T = BST()
	id = None
	while Q:
		control.freeze_update()

		# q = heappop(Q)
		q = Q.pop()
		q.point.hilight()
		sweep = control.plot_horiz_line(q.point.y, color='green')
		if q.is_site_event:
			print(f'({q.point.x}, {q.point.y})', 'evento ponto')
			handle_site_event(q.point, T, Q, V)
		else:
			print(f'({q.point.x}, {q.point.y})', 'evento circulo')
			handle_circle_event(q, T, Q, V)
			q.point.unplot()
		# print('T:', T)
		print()
		control.sleep()
		control.thaw_update()

		control.plot_delete(sweep)
		q.point.unhilight()

	# finalize_voronoi(V, T)
	print('fim do Voronoi')
	return V

def handle_site_event(q, T, Q, V):
	if T.is_empty():
		T.insert(q)
	else:
		f = T.search(q)
		print('f:', f)
		if f.event is not None:
			f.event.point.unplot()
			Q.updateitem(f.event, math.inf)
			Q.pop()

		u, f, v = T.split_and_insert(f, q)
		l = T.all_leaves()
		update_events(Q, T, f, q)

def handle_circle_event(q, T, Q, V):
	f = q.leaf
	print('remove', f, f.pred, f.succ)
	pred, succ, new_node = T.remove(f)


def update_events(Q, T, f, q):
	leaves = T.all_leaves()
	i = leaves.index(f)
	if i > 1:
		p2, p3 = leaves[i-1].point, leaves[i-2].point
		p2.hilight('yellow'), p3.hilight('yellow')
		add_circle_event(f, leaves[i-1], leaves[i-2], q, Q)
		p2.unhilight(), p3.unhilight()

	if len(leaves) - i > 2:
		p2, p3 = leaves[i+1].point, leaves[i+2].point
		p2.hilight('yellow'), p3.hilight('yellow')
		add_circle_event(f, leaves[i+1], leaves[i+2], q, Q)
		p2.unhilight(), p3.unhilight()


def add_circle_event(leaf1, leaf2, leaf3, q, Q):
	center = circumcenter(leaf1.point, leaf2.point, leaf3.point)
	radius = distance(center, leaf1.point)
	circle = control.plot_circle(center.x, center.y, 'blue', radius)
	if center.y - radius < q.y:
		point = Point(center.x, center.y - radius)
		leaf2.event = Event(point, False, leaf2, center)
		Q.additem(leaf2.event, leaf2.event.point.y)
		point.plot(color='cyan')
	control.sleep()
	control.plot_delete(circle)

if __name__== '__main__':
    P = [Point(x, x*(-1)**(x)) for x in range(10)]
    print(P)
    Fortune(P)
