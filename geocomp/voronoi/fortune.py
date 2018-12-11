#!/usr/bin/env python
"""Algoritmo de Fortune"""

import math
from pqdict import pqdict

from geocomp import config
from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.segment import Segment

from geocomp.voronoi.point import Point
from geocomp.voronoi.BST import *
from geocomp.voronoi.DCEL import *
from geocomp.voronoi.circumcircle import *

FORTUNE_EPS = 1e-6
FORTUNE_INF = 200
FORTUNE_PLOT_RATE = 0.05

class Event():
	def __init__(self, point, is_site_event, leaf=None, center=None):
		self.point = point
		self.is_site_event = is_site_event
		self.leaf = leaf
		self.center = center

	def __str__(self):
		return f'({self.point.x}, {self.point.y})'


def plot_all(leaves, V, line_y):

	par_plot = []
	for leaf in leaves:
		if leaf.pred is not None:
			pred_breakpoints = get_x_breakpoints(leaf.pred, line_y)
			startx = choose_x_breakpoint(leaf.pred, pred_breakpoints, line_y)

			bissect_line = bissect_line_function(leaf.pred)
			leaf.pred.hedge.update_origin(Point(startx, bissect_line(startx)))
		else:
			startx = -FORTUNE_INF


		if leaf.succ is not None:
			succ_breakpoints = get_x_breakpoints(leaf.succ, line_y)
			endx = choose_x_breakpoint(leaf.succ, succ_breakpoints, line_y)
			bissect_line = bissect_line_function(leaf.succ)
			leaf.succ.hedge.update_origin(Point(endx, bissect_line(endx)))
		else:
			endx = FORTUNE_INF

		par_plot += [control.plot_parabola(line_y, leaf.point.x, leaf.point.y, startx, endx, steps=400)]

	for h in V.hedges:
		h.segment.plot()

	sweep = control.plot_horiz_line(line_y, color='green')
	return par_plot, sweep

def unplot_all(par_plots, hedges, sweep):
	for par in par_plots:
		control.plot_delete(par)

	for h in hedges:
		if h.segment.lid is None:
			continue
		h.segment.hide()

	control.plot_delete(sweep)

def event_queue(P):
	events = [Event(Point(p.x, p.y), True) for p in P]
	Q = pqdict({e : e.point for e in events}, reverse=True)
	return Q

def Fortune(P):
	Q = event_queue(P)
	V = DCEL()
	T = BST()
	while Q:
		q = Q.pop()
		q.point.hilight()
		par_plots, sweep = plot_all(T.all_leaves(), V, q.point.y)
		control.sleep()

		if q.is_site_event:
			print(f'({q.point.x}, {q.point.y})', 'evento ponto')
			handle_site_event(q.point, T, Q, V)
		else:
			print(f'({q.point.x}, {q.point.y})', 'evento circulo')
			handle_circle_event(q, T, Q, V)
			q.point.unplot()

		print('T:', T)
		print()
		control.sleep()
		if len(Q) > 0:
			next_y = Q.top().point.y
			line_y = q.point.y
			while not math.isclose(line_y, next_y, rel_tol=4*FORTUNE_PLOT_RATE):
				control.freeze_update()
				line_y -= FORTUNE_PLOT_RATE
				unplot_all(par_plots, V.hedges, sweep)

				par_plots, sweep = plot_all(T.all_leaves(), V, line_y)
				control.sleep()

		unplot_all(par_plots, V.hedges, sweep)

		q.point.unhilight()
		print('----------------')
		control.update()

	for h in V.hedges:
		h.segment.plot()
	# finalize_voronoi(V, T)
	print('fim do Voronoi')
	return V

def handle_site_event(q, T, Q, V):
	if T.is_empty():
		T.insert(q)
	else:
		f = T.search(q)
		if f.event is not None:
			f.event.point.unplot()
			Q.updateitem(f.event, Point(math.inf, math.inf))
			Q.pop()
			f.event = None

		u, f, v = T.split_and_insert(f, q)

		bissect_line = bissect_line_function(u)
		v_1 = V.add_vertex(Point(-FORTUNE_INF, bissect_line(-FORTUNE_INF)))
		v_2 = V.add_vertex(Point(FORTUNE_INF, bissect_line(FORTUNE_INF)))

		h_12 = Hedge(v_1, v_2)
		V.add_hedge(h_12)
		u.hedge = h_12

		h_21 = Hedge(v_2, v_1)
		V.add_hedge(h_21)
		v.hedge = h_21

		h_12.add_twin(h_21)

		update_events(Q, T, f, f, q)


def handle_circle_event(q, T, Q, V):
	f = q.leaf
	pred, succ, new_node = T.remove(f, Q)

	left_leaf = new_node.p_i
	right_leaf = new_node.p_j

	update_events(Q, T, left_leaf, right_leaf, q.point)

	u = V.add_vertex(q.center)

	update_hedge(pred, q, u)
	update_hedge(succ, q, u)

	mid1 = mid_point(left_leaf.point, right_leaf.point)
	slope1 = perp_slope(get_line(left_leaf.point, right_leaf.point))

	bissect_line = lambda y : (y - mid1.y)/slope1 + mid1.x

	v = V.add_vertex(Point(bissect_line(-FORTUNE_INF), -FORTUNE_INF))
	h_vu = Hedge(v, u)
	V.add_hedge(h_vu)
	new_node.hedge = h_vu

	h_uv = Hedge(u, v)
	V.add_hedge(h_uv)
	
	h_uv.add_twin(h_vu)

def update_hedge(node, event, vertex):
	node.hedge.update_origin(vertex)

	x_breakpoints = get_x_breakpoints(node, event.point.y)
	bissec = bissect_line_function(node)

	if math.isclose(x_breakpoints[0], event.center.x, rel_tol=FORTUNE_EPS):
		point = Point(FORTUNE_INF, bissec(FORTUNE_INF))
	else:
		point = Point(-FORTUNE_INF, bissec(-FORTUNE_INF))

	if abs(node.hedge.dest.p.x) == FORTUNE_INF:
		node.hedge.update_dest(point)

def is_there_left_triple(leaf):
	return leaf.pred is not None and leaf.pred.p_i.pred is not None

def is_there_right_triple(leaf):
	return leaf.succ is not None and leaf.succ.p_j.succ is not None

def update_events(Q, T, left_leaf, right_leaf, q):
	if is_there_left_triple(right_leaf):
		node1 = right_leaf.pred
		leaf2 = node1.p_i
		node2 = leaf2.pred
		leaf3 = node2.p_i
		print('left:')
		print(leaf2, leaf3)
		if leaf2.event is None:
			add_circle_event(right_leaf, leaf2, leaf3, node1, node2, q, Q)

	if is_there_right_triple(left_leaf):
		node1 = left_leaf.succ
		leaf2 = node1.p_j
		node2 = leaf2.succ
		leaf3 = node2.p_j
		print('right:')
		print(leaf2, leaf3)
		if leaf2.event is None:
			add_circle_event(left_leaf, leaf2, leaf3, node1, node2, q, Q)

def is_valid_event(center, radius, q):
	is_under_sweep = center.y - radius < q.y - FORTUNE_EPS
	is_on_sweep = math.isclose(center.y - radius, q.y)
	is_on_the_right = center.x - radius > q.x + FORTUNE_EPS

	return is_under_sweep or (is_on_sweep and is_on_the_right)

def is_divergent(node, center):
	if node.p_i.point.y < node.p_j.point.y:
		return node.p_i.point.x > center.x
	else:
		return node.p_j.point.x < center.x

def add_circle_event(leaf1, leaf2, leaf3, node1, node2, q, Q):
	p1, p2, p3 = leaf1.point, leaf2.point, leaf3.point
	p2.hilight('yellow')
	p3.hilight('yellow')

	center = circumcenter(p1, p2, p3)
	radius = distance(center, p1)
	circle = control.plot_circle(center.x, center.y, 'blue', radius)

	is_convergent = not(is_divergent(node1, center) and is_divergent(node2, center))
	if is_valid_event(center, radius, q) and is_convergent:
		point = Point(center.x, center.y - radius)
		print('------ cria evento circulo: ', leaf2, f'({center.x}, {center.y})')
		leaf2.event = Event(point, False, leaf2, center)
		Q.additem(leaf2.event, point)
		point.plot(color='cyan')

	control.sleep()
	control.plot_delete(circle)
	p2.unhilight()
	p3.unhilight()
