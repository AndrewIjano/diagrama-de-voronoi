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
		update_events(Q, T, f, q)

def handle_circle_event(q, T, Q, V):
	f = q.leaf
	print('remove', f, f.pred, f.succ)
	pred, succ, new_node = T.remove(f, Q)


def update_events(Q, T, f, q):
	if f.pred is not None and f.pred.p_i.pred is not None:
		leaf2 = f.pred.p_i
		leaf3 = leaf2.pred.p_i
		add_circle_event(f, leaf2, leaf3, q, Q)

	if f.succ is not None and f.succ.p_j.succ is not None:
		leaf2 = f.succ.p_j
		leaf3 = leaf2.succ.p_j
		add_circle_event(f, leaf2, leaf3, q, Q)

def add_circle_event(leaf1, leaf2, leaf3, q, Q):
	p1, p2, p3 = leaf1.point, leaf2.point, leaf3.point
	p2.hilight('yellow'), p3.hilight('yellow')
	center = circumcenter(p1, p2, p3)
	radius = distance(center, p1)
	circle = control.plot_circle(center.x, center.y, 'blue', radius)
	if center.y - radius < q.y:
		point = Point(center.x, center.y - radius)
		leaf2.event = Event(point, False, leaf2, center)
		Q.additem(leaf2.event, leaf2.event.point.y)
		point.plot(color='cyan')
	control.sleep()
	control.plot_delete(circle)
	p2.unhilight(), p3.unhilight()


if __name__== '__main__':
    P = [Point(x, x*(-1)**(x)) for x in range(10)]
    print(P)
    Fortune(P)
