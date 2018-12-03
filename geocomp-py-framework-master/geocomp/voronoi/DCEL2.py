import math
from point import Point

class Vertex():
	""" The vertex record of a vertex v stores the coordinates of v in a field called
	Coordinates(v). It also stores a pointer IncidentEdge(v) to an arbitrary
	half-edge that has v as its origin.										  """

	def __init__(self, point, IncidentEdge=None):
		self.Coordinates = point
		self.IncidentEdge = IncidentEdge

	def __repr__(self):
		return f'<Vertex: ({int(self.Coordinates.x)}, {int(self.Coordinates.y)})>'


class Face():
	""" The face record of a face f stores a pointer OuterComponent(f) to some
	half-edge on its outer boundary. For the unbounded face this pointer is nil.
	It also stores a list InnerComponents( f ), which contains for each hole in
	the face a pointer to some half-edge on the boundary of the hole.		 """
	
	def __init__(self, OuterComponent, InnerComponents=None):
		self.OuterComponent = OuterComponent
		self.InnerComponents = InnerComponents

	def __repr__(self):
		return f'<Face: ({int(self.OuterComponent.Origin.Coordinates.x)}, {int(self.OuterComponent.Origin.Coordinates.y)})>'


class HalfEdge():
	""" The half-edge record of a half-edge e stores a pointer Origin(e) to its origin, 
	a pointer Twin(e) to its twin half-edge, and a pointer IncidentFace(e) to the 
	face that it bounds. We don’t need to store the destination of an edge, because
	it is equal to Origin(Twin(e)). The origin is chosen such that IncidentFace(e) 
	lies to the left of e when it is traversed from origin to destination. The 
	half-edge record also stores pointers Next(e) and Prev(e) to the next and previous 
	edge on the boundary of IncidentFace(e). Thus Next(e) is the unique half-edge on
	the boundary of IncidentFace(e) that has the destination of e as its origin, and 
	Prev(e) is the unique half-edge on the boundary of IncidentFace(e) that has 
	Origin(e) as its destination.												"""

	def __init__(self, Origin, Twin=None, IncidentFace=None, Prev=None, Next=None):
		self.Origin = Origin
		self.Twin = Twin
		self.IncidentFace = Face
		self.Prev = Prev
		self.Next = Next

	def __repr__(self):
		return f'<Half-Edge: \n Origin = ({int(self.Origin.Coordinates.x)}, {int(self.Origin.Coordinates.y)})>'

class DCEL():
	""" Implementa uma doubly-connected edge list """

	def __init__(self):
		self.vertices = []
		self.hedges = []
		self.faces = []

	def add_vertex(self, vertex):
		self.vertices.append(vertex)

	def add_hedge(self, hedge):
		self.hedges.append(hedge)

	def add_face(self, face):
		self.faces.append(face)



	def __str__(self):
		return  '<DCEL:' +\
		'\n  vertices: ' + ', '.join([str(v) for v in self.vertices]) +\
		'\n  hedges: '   + ', '.join([str(h) for h in self.hedges])   +\
		'\n  faces: '	+ ', '.join([str(f) for f in self.faces]) + '\n  >'


if __name__=='__main__':
	point1 = Point(1, 2)
	point2 = Point(2, 5)
	
	v = Vertex(point1)
	print(v)
	u = Vertex(point2)
	print(u)

	he1 = HalfEdge(v)
	he2 = HalfEdge(u)

	f1 = Face(he1)
	f2 = Face(he2)

	print(v)
	print(u)
	print(he1)
	print(he2)
	print(f1)
	print(f2)

	dcel = DCEL()

	dcel.add_vertex(v)
	dcel.add_vertex(u)
	dcel.add_hedge(he1)
	dcel.add_face(f1)
	print(dcel)