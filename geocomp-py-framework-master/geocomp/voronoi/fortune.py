#!/usr/bin/env python
"""Algoritmo de Fortune"""

# from geocomp.common.polygon import Polygon
from random import randint
from geocomp.common import control
from geocomp.common.guiprim import *
from queue import PriorityQueue
from pqdict import pqdict
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.voronoi.DCEL import DCEL, Vertex, Hedge, Face
from geocomp.voronoi.BST import BST
from geocomp.voronoi.circumcircle import circumcenter, distance, mid_point, get_line, perp_slope, get_line_from_slope
import math

from geocomp import config

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

def my_parabola(p, line_y):
	if(p.y == line_y):
		return []
	g = lambda h : lambda x : (x**2 - 2*h.x*x + h.x**2 + h.y**2- line_y**2)/(2*(h.y - line_y))
	f = g(p)
	points_i = [Point(x/50, f(x/50)) for x in range(-500, 500)]
	for p in points_i: p.plot(color='cyan', radius=1)
	return points_i

def my_unplot_parabola(parabola):
    for p in parabola:
        p.unplot()


def Fortune(P):
	Q = event_queue(P)
	V = DCEL()
	T = BST()
	id = None
	while Q:
		control.freeze_update()

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

		# print('Q:',Q)
		print('T:', T)
		print()
		control.sleep()
		lista_para = T.all_leaves()
		lista_plots = []
		for par in lista_para:
			lista_plots.append(control.plot_parabola(q.point.y,par.point.x,par.point.y,-200,200, steps=300))

		for h in V.hedges:
			h.segment.plot(cor='blue')
		control.sleep()
		for id in lista_plots:
			control.plot_delete(id)

		for h in V.hedges:
			h.segment.hide()
		control.thaw_update()

		control.plot_delete(sweep)
		q.point.unhilight()
		print('----------------')

	# finalize_voronoi(V, T)
	# for h in V.hedges:
	# 	h.segment.plot()
	print('fim do Voronoi')
	return V

def handle_site_event(q, T, Q, V):
	if T.is_empty():
		T.insert(q)
	else:
		f = T.search(q)
		# print('f:', f)
		if f.event is not None:
			f.event.point.unplot()
			Q.updateitem(f.event, math.inf)
			Q.pop()
			f.event = None

		u, f, v = T.split_and_insert(f, q)

		# print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa')
		print('pontos analisados:', f'({u.p_i.point.x}, {u.p_i.point.y}) ({u.p_j.point.x}, {u.p_j.point.y})')
		mid1 = mid_point(u.p_i.point, u.p_j.point)
		slope1 = perp_slope(get_line(u.p_i.point, u.p_j.point))
		f1 = lambda y : (y -  mid1.y)/slope1 + mid1.x
		# print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
		p1 = Point(f1(200), 200)
		p2 = Point(f1(-200), -200)
		print('- ', (p1.x, p1.y) , (p2.x, p2.y))

		v_1 = Vertex(p1)
		v_2 = Vertex(p2)

		h_12 = Hedge(v_1, v_2)
		h_12.segment.init = p1
		h_12.segment.to = p2
		u.hedge = h_12

		V.add_hedge(h_12)
		# h_21 = Hedge(v_2, v_1)
		# h_21.segment.init = p1
		# h_21.segment.to = p2
		v.hedge = h_12


		# h_12.segment.plot(cor='blue')

		update_events(Q, T, f, f, q)


def handle_circle_event(q, T, Q, V):
	f = q.leaf
	pred, succ, new_node = T.remove(f, Q)

	left_leaf = new_node.p_i
	right_leaf = new_node.p_j

	update_events(Q, T, left_leaf, right_leaf, q.point)
	c = q.center
	c.plot(color='purple')
	c.hilight()
	u = Vertex(c)
	pred.hedge.dest = u
	if pred.hedge.segment.to.y == -200:
		pred.hedge.segment.to = c
	else:
		pred.hedge.segment.init = c
	# if pred.hedge.segment.init is not None:
		# print('PRRRRRRRRRREEED')
	# pred.hedge.segment.plot()

	succ.hedge.dest = u
	if succ.hedge.segment.to.y == -200:
		succ.hedge.segment.to = c
	else:
		succ.hedge.segment.init = c
	# if succ.hedge.segment.init is not None:
		# print('SUUUUUUUUUUUUUUCCCCCCCCCCCCC')
	# succ.hedge.segment.plot()

	print('evento circulo')
	mid1 = mid_point(left_leaf.point, right_leaf.point)
	slope1 = perp_slope(get_line(left_leaf.point, right_leaf.point))
	f1 = lambda y : (y -  mid1.y)/slope1 + mid1.x

	p = Point(f1(-200), -200)
	v = Vertex(p)
	print('-> p:', (p.x,p.y))
	print('-> c:', (c.x, c.y))
	print('-> f:', f)
	h_uv = Hedge(u, v)
	V.add_hedge(h_uv)
	new_node.hedge = h_uv
	new_node.hedge.segment.init = c
	new_node.hedge.segment.to = p
	# new_node.hedge.segment.plot(cor='blue')

def is_there_left_triple(leaf):
	return leaf.pred is not None and leaf.pred.p_i.pred is not None

def is_there_right_triple(leaf):
	return leaf.succ is not None and leaf.succ.p_j.succ is not None

def update_events(Q, T, left_leaf, right_leaf, q):
	if is_there_left_triple(right_leaf):
		leaf2 = right_leaf.pred.p_i
		leaf3 = leaf2.pred.p_i
		if leaf2.event is None:
			add_circle_event(right_leaf, leaf2, leaf3, q, Q)

	if is_there_right_triple(left_leaf):
		leaf2 = left_leaf.succ.p_j
		leaf3 = leaf2.succ.p_j
		if leaf2.event is None:
			add_circle_event(left_leaf, leaf2, leaf3, q, Q)

def add_circle_event(leaf1, leaf2, leaf3, q, Q):
	p1, p2, p3 = leaf1.point, leaf2.point, leaf3.point
	p2.hilight('yellow'), p3.hilight('yellow')
	center = circumcenter(p1, p2, p3)
	radius = distance(center, p1)
	circle = control.plot_circle(center.x, center.y, 'blue', radius)
	if center.y - radius < q.y:
		point = Point(center.x, center.y - radius)
		print('------ cria evento circulo: ', leaf2)
		leaf2.event = Event(point, False, leaf2, center)
		Q.additem(leaf2.event, leaf2.event.point.y)
		point.plot(color='cyan')
	control.sleep()
	control.plot_delete(circle)
	p2.unhilight(), p3.unhilight()
