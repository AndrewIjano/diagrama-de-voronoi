#!/usr/bin/env python
"""Algoritmo de Fortune"""

# from geocomp.common.polygon import Polygon
from geocomp.common import control
from geocomp.common.guiprim import *
from queue import PriorityQueue
from heapq import heappush, heappop, heapify
from geocomp.common.point import Point
from geocomp.common.segment import Segment
from geocomp.voronoi.DCEL import DCEL
from geocomp.voronoi.BST import BST
from geocomp.voronoi.circumcircle import circumcenter, distance

class Event():
	def __init__(self, point, is_site_event, leaf=None):
		self.point = point
		self.is_site_event = is_site_event
		self.leaf = leaf

	def __repr__(self):
		return repr(self.point)

	def __eq__(self, other):
		return self.point.y == other.point.y

	def __lt__(self, other):
		return self.point.y > other.point.y

	def __gt__(self, other):
		return self.point.y < other.point.y

def event_queue(P):
	Q = [Event(p, True) for p in P]
	for p in P:
		p.plot(color='red')
	heapify(Q)
	return Q

def Fortune(P):
	Q = event_queue(P)
	V = DCEL()
	T = BST()
	id = None
	while Q:
		control.freeze_update()

		q = heappop(Q)
		q.point.hilight()
		sweep = Segment(Point(-10000, q.point.y), Point(10000, q.point.y))
		sweep.plot(cor='green')


		if q.is_site_event:
			print(f'({q.point.x}, {q.point.y})', 'evento ponto')
			handle_site_event(q.point, T, Q, V)
		else:
			print(f'({q.point.x}, {q.point.y})', 'evento circulo')
			handle_circle_event(q, T, Q, V)
			q.point.unplot()
			# trata_evento_circulo(q, T, Q, V)
		# print('T:', T)
		print()
		id = sweep
		control.sleep()
		control.thaw_update()
		control.update()
		sweep.hide()
		q.point.unhilight()

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
			Q.remove(f.event)


		u, f, v = T.split_and_insert(f, q)
		l = T.all_leaves()
		# print(l)
		update_events(Q, T, f, q)
		# print('f:', f)

def handle_circle_event(q, T, Q, V):
	f = q.leaf


def update_events(Q, T, f, q):
	leaves = T.all_leaves()
	i = leaves.index(f)
	if i > 1:
		p1 = f.point
		p2 = leaves[i - 1].point
		p3 = leaves[i - 2].point
		p2.hilight('yellow'), p3.hilight('yellow')

		center = circumcenter(p1, p2, p3)
		radius = distance(center, p1)
		id = control.plot_circle (center.x, center.y, 'red', radius)
		if center.y - radius < q.y:
			point = Point(center.x, center.y - radius)
			point.plot(color='cyan')
			heappush(Q, Event(point, False, f))
		control.sleep()
		p2.unhilight(), p3.unhilight()
		control.plot_delete(id)
	if len(leaves) - i > 2:
		p1 = f.point
		p2 = leaves[i + 1].point
		p3 = leaves[i + 2].point
		p2.hilight('yellow'), p3.hilight('yellow')

		center = circumcenter(p1, p2, p3)
		radius = distance(center, p1)
		id = control.plot_circle (center.x, center.y, 'red', radius)
		if center.y - radius < q.y:
			point = Point(center.x, center.y - radius)
			point.plot(color='cyan')
			heappush(Q, Event(point, False, f))
		control.sleep()
		p2.unhilight(), p3.unhilight()
		control.plot_delete(id)

if __name__== '__main__':
    P = [Point(x, x*(-1)**(x)) for x in range(10)]
    print(P)
    Fortune(P)

# def vertices_tangentes (Q, p):
# 	"""retorna os dois vertices de tangencia de Q em relacao a p
#
# 	Se existirem (i.e. se p estiver fora de Q), os vertices de tangencia
# 	sao retornados em uma lista. Na posicao [0] dessa lista esta o vertice
# 	"anterior" a p, e na posicao 1 o vertice "posterior" a p.
#
# 	Se p estiver dentro de Q, retorna uma lista vazia."""
#
# 	tan = []
# 	arestas = []
#
# 	pts = Q.pts
# 	area_old = area2 (pts.prev, pts, p)
# 	last = (area_old >= 0) # left_on
# 	for pts in Q.to_list ():
# 		prev = pts.prev
# 		next = pts.next
# 		cur = pts
#
# 		area = area2 (cur, next, p)
#
# 		now = (area >= 0) # left_on
# 		if last != now:
# 			if area_old == 0:
# 				# novo ponto e' colinear c/ aresta anterior
# 				#  --> pegamos verice mais distante
# 				tan.append (prev)
# 			elif area == 0:
# 				# novo ponto e' colinear c/ proxima aresta
# 				#  --> pegamos vertice mais distante
# 				tan.append (next)
# 			else:
# 				tan.append (cur)
# 		last = now
# 		area_old = area
#
# 	if len (tan) == 0:
# 		return []
#
# 	if len (tan) != 2:
# 		print('\n\n===> len (tan) != 0 e != 2 !!!!\n\n')
#
# 	if right (tan[0], tan[1], p):
# 		return [ tan[0], tan[1] ]
# 	else:
# 		return [ tan[1], tan[0] ]
#
#
# def Incremental (l):
# 	"Algoritmo incremental para o problema do fecho convexo de uma lista de pontos"
#
# 	if len (l) == 0: return None
#
# 	# crio um fecho c/ um ponto
# 	fecho = Polygon ([ l[0] ])
# 	fecho.plot ()
#
#
# 	# Como nao posso admitir que os pontos estao em posicao geral,
# 	# preciso tomar cuidado ate encontrar tres pontos nao colineares
# 	# :-(
# 	length = 1
# 	k = 0
# 	hi = l[k].hilight ()
# 	for k in range (1, len (l)):
# 		pts = fecho.pts
# 		l[k-1].unhilight (hi)
# 		hi = l[k].hilight ()
# 		control.thaw_update ()
#
# 		if length == 1:
# 			if l[k].x == pts.x and l[k].y == pts.y:
# 				continue
# 			fecho.hide ()
# 			pts.next = pts.prev = l[k]
# 			l[k].next = l[k].prev = pts
# 			fecho.pts = pts
# 			fecho.plot ()
# 			length = length + 1
#
# 		elif length == 2:
# 			next = pts.next
# 			dir = area2 (pts, next, l[k])
# 			if dir == 0:
# 				#Mais um ponto colinear -> pega o par mais distante
# 				fecho.hide ()
# 				dist_pts_next = dist2 (pts, next)
# 				dist_pts_lk = dist2 (pts, l[k])
# 				dist_next_lk = dist2 (next, l[k])
# 				if dist_pts_next >= dist_pts_lk and dist_pts_next >= dist_next_lk:
# 					a = pts
# 					b = next
# 				elif dist_pts_lk >= dist_pts_next  and  dist_pts_lk >= dist_next_lk:
# 					a = pts
# 					b = l[k]
# 				elif dist_next_lk >= dist_pts_lk and dist_next_lk >= dist_pts_next:
# 					a = next
# 					b = l[k]
# 				else:
# 					print('pau!!!')
#
# 				a.next = a.prev = b
# 				b.next = b.prev = a
# 				fecho.pts = a
# 				fecho.plot ()
#
# 				continue
# 			fecho.hide ()
# 			# Ponto nao colinear :) - basta tomar cuidado p/
# 			#   construir o poligono c/ a direcao certa
# 			if dir > 0:
# 				pts.prev = next.next = l[k]
# 				l[k].next = pts
# 				l[k].prev = next
# 			else:
# 				pts.next = next.prev = l[k]
# 				l[k].prev = pts
# 				l[k].next = next
#
# 			length = length + 1
# 			fecho.pts = pts
# 			fecho.plot ()
# 			break
#
# 	# Ja tenho um fecho com 3 pontos -> basta "cresce-lo"
# 	for k in range (k+1, len (l)):
# 		pts = fecho.pts
# 		l[k-1].unhilight (hi)
# 		hi = l[k].hilight ()
# 		control.thaw_update ()
#
# 		tan = vertices_tangentes (fecho, l[k])
# 		# l[k] esta fora do fecho atual <=> len (tan) == 2
# 		if len (tan) == 2:
# 			control.freeze_update ()
# 			fecho.hide ()
#
# 			tan[0].next.prev = None
# 			tan[0].next = l[k]
# 			l[k].prev = tan[0]
#
# 			if tan[1].prev: tan[1].prev.next = None
# 			tan[1].prev = l[k]
# 			l[k].next = tan[1]
#
# 			fecho.pts = tan[0]
# 			fecho.plot ()
#
# 			control.thaw_update ()
#
# 	l[k].unhilight (hi)
# 	fecho.plot ()
# 	fecho.extra_info = 'vertices: %d'%len (fecho.to_list ())
# 	return fecho
