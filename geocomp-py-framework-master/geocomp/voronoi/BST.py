import math

class Node():
    """Implementa um nó interno"""
    def __init__(self, left_point, right_point):
        self.p_i = left_point
        self.p_j = right_point
        right = left = hedge = None

    def __repr__(self):
        return f'<Node: {self.p_i}, {self.p_j}>'

class Leaf():
    """Implementa uma folha"""
    def __init__(self, point):
        self.point = point
        self.event = None

    def __repr__(self):
        return f'<Leaf: {self.point}>'

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
        """Substitui a folha da árvore pela subárvore com três folhas"""
        new_tree = Node(leaf.point, point)
        new_node = Node(point, leaf.point)
        new_leaf = Leaf(point)

        print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', Leaf(leaf.point) == leaf)

        new_tree.left, new_tree.right = Leaf(leaf.point), new_node
        new_node.left, new_node.right = new_leaf, Leaf(leaf.point)

        def insert_tree(node, new_tree, point):
            if isinstance(node, Leaf):
                return new_tree
            x_breakpoint = get_x_breakpoint(node, point.y)
            if point.x < x_breakpoint:
                node.left = insert_tree(node.left, new_tree, point)
            else:
                node.right = insert_tree(node.right, new_tree, point)
            return node

        self.root = insert_tree(self.root, new_tree, point)
        return new_tree, new_leaf, new_node

    def delete_min(self):
        """Remove a menor folha da árvore"""
        def inner_delete_min(node):
            if isinstance(node.left, Leaf):
                return node.right
            node.left = delete_min(node.left)
            return node
        self.root = delete_min(self.root)

    # def delete()

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
        def inner_print(node):
            if isinstance(node, Leaf):
                return node
            return f'{node} {inner_print(node.left)} {inner_print(node.right)}'
        return f'<BST: {inner_print(self.root)}>'

def get_x_breakpoint(node, line_y):
    """ Calcula a coordenada x do breakpoint dado a tupla de pontos
    e a posição y da linha de varredura
    """
    i, j = node.p_i, node.p_j

    a = i.y - j.y
    b = 2 * (j.y*i.x - i.y * j.x)
    c = i.y * (j.x**2 + j.y**2)  \
        - j.y * (i.x**2 + i.y**2)\
        + line_y**2 * (j.y - i.y)

    roots = []
    delta = b**2 - 4*a*c
    if delta < 0:
        raise NameError('Negative discriminant')
    elif delta != 0:
        roots += [(-b + math.sqrt(delta))/(2*a)]

    roots += [(-b - math.sqrt(delta))/(2*a)]

    if len(roots) == 1 or i.x <= roots[0] <= j.x:
        return roots[0]
    return roots[1]
