import math

class Node():
    """Implementa um nó"""
    def __init__(self, key):
        self.key = key
        self.circle_event = None
        self.left = None
        self.right = None

def get_x_breakpoint(points, line_y):
    """ Calcula a coordenada x do breakpoint dado a tupla de pontos
    e a posição y da linha de varredura
    """
    p_i, p_j = points

    a = p_i.y - p_j.y
    b = 2 * (p_j.y*p_i.x - p_i.y * p_j.x)
    c = p_i.y * (p_j.x**2 + p_j.y**2)  \
        - p_j.y * (p_i.x**2 + p_i.y**2)\
        + line_y**2 * (p_j.y - p_i.y)

    roots = []
    delta = b**2 - 4*a*c
    if delta < 0:
        print('sem solução')
    elif delta != 0:
        roots += [(-b + math.sqrt(delta))/(2*a)]

    roots += [(-b - math.sqrt(delta))/(2*a)]

    if len(roots) == 1 or p_i.x <= roots[0] <= p_j.x:
        return roots[0]

    return roots[1]

class BST():
    """Implementa uma árvore de busca balanceada"""

    def __init__(self):
        self.root = None

    def is_empty(self):
        """Testa se a árvore está vazia"""
        return self.root is None

    def get(self, point):
        """Busca a folha da árvore do arco acima do ponto"""
        node = self._get(self.root, point)
        if node is None:
            return None
        return (node.key, node.circle_event)

    def _get(self, node, point):
        if node is None:
            raise NameError('None node given')

        if not isinstance(node.key, tuple):
            return node

        x_breakpoint = get_x_breakpoint(node.key, point.y)
        if point.x < x_breakpoint:
            return self._get(node.left, point)
        return self._get(node.right, point)

    def put(self, point):
        """Insere um ponto na árvore"""
        self.root = self._put(self.root, point)

    def _put(self, node, point):
        if node is None:
            return  Node(point)

        x_breakpoint = get_x_breakpoint(node.key, point.y)
        if point.x < x_breakpoint:
            node.left = self._put(node.left, point)
        else:
            node.right = self._put(node.right, point)

        return node
