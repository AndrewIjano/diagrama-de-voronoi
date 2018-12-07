from geocomp.common.segment import Segment
from geocomp.common.point import Point
class Vertex():
    """Implementa um vértice 2D de uma DCEL"""

    def __init__(self, p):
        self.p  = p
        self.hedge = None

    def add_hedge(self, hedge):
        self.hedge = hedge

    def hedge(self):
        return self.hedge

    def __str__(self):
        return f'<Vertex, ({self.p.x},{self.p.y})>'

class Hedge():
    """Implementa uma meia-aresta de uma DCEL"""

    def __init__(self, u, v):
        self.origin = u
        self.dest = v
        self.twin = None
        self.face = None
        self.next_hedge = None
        self.segment = Segment(u.p, v.p)

    def previous_hedge(self):
        return self.twin.next_hedge

    def origin(self):
        return self.origin

    def twin(self):
        return self.twin

    def next_hedge(self):
        return self.next_hedge

    def face(self):
        return self.face

    def add_twin(self, hedge):
        self.twin = hedge
        hedge.twin = self

    def add_face(self, face):
        self.face = face

    def add_next_hedge(self, hedge):
        self.next_hedge = hedge

    def update_origin(self, vertex):
        if isinstance(vertex, Point):
            vertex = Vertex(vertex)

        self.origin.p = vertex.p
        self.segment.init = vertex.p

        self.twin.dest.p = vertex.p
        self.twin.segment.to = vertex.p

    def update_dest(self, vertex):
        if isinstance(vertex, Point):
            vertex = Vertex(vertex)

        self.dest.p = vertex.p
        self.segment.to = vertex.p

        self.twin.origin.p = vertex.p
        self.twin.segment.init = vertex.p

    def __str__(self):
        return f'<Hedge, '               +\
               f'origin: {self.origin}, ' +\
               f'twin: {self.twin}, '     +\
               f'face: {self.face}, '     +\
               f'next_hedge: {self.next_hedge}>'

class Face():
    """Implementa uma face de uma DCEL"""

    def __init__(self):
         self.hedge = None

    def hedge(self):
        return self.hedge

    def add_hedge(self, hedge):
        self.hedge = hedge

    def __str__(self):
        return f'<Face, hedge: {self.hedge}>'

class DCEL():
    """Implementa uma Double-Connected Edge List"""

    def __init__(self):
        self.vertices = []
        self.hedges = []
        self.faces = []

    def add_vertex(self, vertex):
        if isinstance(vertex, Point):
            vertex = Vertex(vertex)
        vertex.p.plot('red', 5)
        self.vertices.append(vertex)
        return vertex

    def add_hedge(self, hedge):
        self.hedges.append(hedge)

    def add_face(self, face):
        self.faces.append(face)

    def __str__(self):
        return  '<DCEL:' +\
                '\n  vertices: ' + ', '.join([str(v) for v in self.vertices]) +\
                '\n  hedges: '   + ', '.join([str(h) for h in self.hedges])   +\
                '\n  faces: '    + ', '.join([str(f) for f in self.faces]) + '\n  >'


if __name__=='__main__':
    v = Vertex(2,3)
    u = Vertex(4, 5)
    h = Hedge(v, u)
    f = Face()
    dcel = DCEL()
    dcel.add_vertex(v)
    dcel.add_vertex(u)
    dcel.add_hedge(h)
    dcel.add_face(f)
    print(dcel)
