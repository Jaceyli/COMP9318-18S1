## import modules here 

################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b

################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    i = 0
    if x < 0:
        return -1
    else:
        start = 1
        while (start * start - x) > 1e-9 or ((start * start - x) < - 1e-9):
            start = (start + x / start) / 2.0
            i = i + 1
            # print(i, start)
        return int(start)


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    p0 = x_0 * 1.0
    for i in range(MAX_ITER):
        p = p0 - f(p0) / fprime(p0)
        # 如果小于精度值则退出迭代
        if abs(p - p0) < EPSILON:
            return p
        p0 = p

    print('已达到最大迭代次数， 但是仍然无法收敛')

################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    tree = Tree(tokens[0])
    child = tree
    parent = Tree(tokens[0])
    root = []
    for i in range(1, len(tokens)):
        if tokens[i] == '[':
            root.append(parent)
            parent = child
            i += 1
        elif tokens[i] == ']':
            i += 1
            parent = root.pop()
            continue
        else:
            child = Tree(tokens[i])
            parent.add_child(child)
    return tree

def max_depth(root): # do not change the heading of the function
    if root.children == None:
        return 1
    depth = [1]
    for child in root.children:
        depth.append(max_depth(child) + 1)
    return max(depth)