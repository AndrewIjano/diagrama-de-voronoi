import math
from geocomp.common.point import Point

from geocomp.common import control
from geocomp.common.guiprim import *
from geocomp.common.segment import Segment

class Node():
    """Implementa um nó interno"""
    def __init__(self, left_point, right_point):
        self.p_i = left_point
        self.p_j = right_point
        self.right = self.left = self.hedge = self.father = None

    def __repr__(self):
        return f'<Node: ({int(self.p_i.x)}, {int(self.p_i.y)}), ({int(self.p_j.x)}, {int(self.p_j.y)})>'

class Leaf():
    """Implementa uma folha"""
    def __init__(self, point, pred=None, succ=None):
        self.point = point
        self.event = None
        self.pred = pred
        self.succ = succ

    def __repr__(self):
        return f'<Leaf: ({int(self.point.x)}, {int(self.point.y)})>'

class BST():
    """Implementa uma árvore de busca balanceada"""

    def __init__(self):
        self.root = None

    def is_empty(self):
        return self.root is None

    def insert(self, point):
        """Insere um arco em uma árvore vazia"""
        self.root = Leaf(point)

    def search(self, point):
        """Busca a folha do arco acima do ponto"""
        def inner_search(node, point):
            if isinstance(node, Leaf):
                return node

            x_breakpoint = get_x_breakpoint(node, point.y)
            if point.x < x_breakpoint:
                return inner_search(node.left, point)
            return inner_search(node.right, point)

        return inner_search(self.root, point)

    def split_and_insert(self, leaf, point):
        """Substitui a folha da árvore pela subárvore com três folhas:

            leaf   =>    new_tree
                        /        \\
             Leaf(leaf.point)     new_node
                                 /       \\
                               new_leaf  Leaf(leaf.point)
        """
        new_tree = Node(leaf.point, point)
        new_node = Node(point, leaf.point)
        new_leaf = Leaf(point, pred=new_tree, succ=new_node)

        new_tree.left, new_tree.right = Leaf(leaf.point, succ=new_tree), new_node
        new_node.left, new_node.right = new_leaf, Leaf(leaf.point, pred=new_node)
        new_node.right.succ = leaf.succ
        new_tree.left.pred = leaf.pred
        new_node.father = new_tree

        if leaf.pred is not None and leaf.pred.right == leaf:
            new_tree.father = leaf.pred
            leaf.pred.right = new_tree
        elif leaf.succ is not None:
            new_tree.father = leaf.succ
            leaf.succ.left = new_tree
        else:
            self.root = new_tree

        # print('split_and_insert: L_left:', new_tree.left, new_tree.left.pred, new_tree.left.succ)
        # print('split_and_insert: L_right:', new_node.right, new_node.right.pred, new_node.right.succ)
        return new_tree, new_leaf, new_node

    def remove(self, leaf):
        """Remove uma folha da árvore e devolve os dois nós internos associados
        e seu substituto
        """
        def substitute_node(node, substitute):
            if node == self.root:
                self.root = substitute    
            elif node.father.left == node:
                node.father.left = substitute
            else:
                node.father.right = substitute

        pred, succ = leaf.pred, leaf.succ
        if pred is None:
            substitute_node(succ, succ.right)
            return pred, succ, None
        if succ is None:
            substitute_node(pred, pred.left)
            return pred, succ, None

        new_node = Node(pred.p_i, succ.p_j)
        remov, subst = (pred, succ) if pred.right == leaf else (succ, pred)
        other_leaf   = remov.right  if remov.left == leaf else remov.left

        substitute_node(remov, other_leaf)
        substitute_node(subst, new_node)

        new_node.father = subst.father
        new_node.left = subst.left
        new_node.right = subst.right
        return pred, succ, new_node

    def all_leaves(self):
        """Retorna todas as folhas da árvore em ordem crescente"""
        def inner_all_leaves(node):
            if isinstance(node, Leaf):
                return [node]
            leaves = []
            leaves += inner_all_leaves(node.left)
            leaves += inner_all_leaves(node.right)
            return leaves
        return inner_all_leaves(self.root)

    def __str__(self):
        queue = [self.root]
        string = ''
        count = div = 1
        while len(queue) > 0:
            n = queue.pop(0)
            string += repr(n)
            if count % div == 0:
                count = 0
                div *= 2
                string += '\n'
            if not isinstance(n, Leaf):
                queue.append(n.left)
                queue.append(n.right)
            count += 1
        return string
        # def inner_print(node):
        #     if isinstance(node, Leaf):
        #         return node
        #     return f'{node} {inner_print(node.left)} {inner_print(node.right)}'
        # return f'<BST: {inner_print(self.root)}>'

def get_x_breakpoint(node, line_y):
    """ Calcula a coordenada x do breakpoint dado a tupla de pontos
    e a posição y da linha de varredura
    """
    i, j = node.p_i, node.p_j
    g = lambda h : lambda x : (x**2 - 2*h.x*x + h.x**2 + h.y**2- line_y**2)/(2*(h.y - line_y))
    f_i, f_j = g(i), g(j)
    points_i = [Point(x/10, f_i(x/10)) for x in range(-100, 100)]
    points_j = [Point(x/10, f_j(x/10)) for x in range(-100, 100)]

    for p in points_i: p.plot(color='cyan', radius=1)
    for p in points_j: p.plot(color='yellow', radius=1)

    a = j.y - i.y
    b = 2 * (j.x*i.y - i.x*j.y + line_y * (i.x - j.x))
    c = (j.y - line_y) * (i.x**2 + i.y**2 - line_y**2)\
        - (j.x**2 + j.y**2 - line_y**2) * (i.y - line_y)

    roots = []
    delta = b**2 - 4*a*c
    if delta < 0:
        raise NameError('Negative discriminant')
    elif delta != 0:
        roots += [(-b + math.sqrt(delta))/(2*a)]

    roots += [(-b - math.sqrt(delta))/(2*a)]
    print(roots)
    i.hilight(color='cyan')
    j.hilight(color='yellow')
    id_1 = control.plot_vert_line(roots[0], color='blue')
    id_2 = control.plot_vert_line(roots[1], color='red')

    control.sleep()
    control.thaw_update()
    control.update()

    control.plot_delete(id_1)
    control.plot_delete(id_2)
    i.unhilight()
    j.unhilight()
    for p in points_i: p.unplot()
    for p in points_j: p.unplot()

    if len(roots) == 1 or i.x <= roots[0] <= j.x:
        return roots[0]
    return roots[1]
