
class Node():
    def __init__(self, element):
        self.element = element
        self.children = []

class Tree():
    def __init__(self, root=None, father=None):
        self.root = Node(root)
        self.father = father

    def create_node(self, element, father):
        return Tree(element, father)

    def insert(self, node, element):
        if node != self.root:
            for ele in self.root.children:
                if ele.root.element == node.element:
                    return ele.root.children.append(self.create_node(element, ele))
                else:
                    if ele.root.children:
                        ele.insert(node, element)

        return node.children.append(self.create_node(element, self))

    def get_leaves(self, tree, leaves):
        for ele in tree.root.children:
            if ele.root.children:
                ele.get_leaves(ele, leaves)
            else:
                print("Leave:", ele.root.element, ",his father:", ele.father.root.element)
                leaves.append(ele)
        return leaves

    def get_father(self):
        if self.father == None:
            return self.root.element
            
        return self.father.get_father()

    def print(self):
        print("Root: ", self.root.element)
        for ele in self.root.children:
            print("child: ", ele.root.element)
            if ele.root.children:   
                ele.sub_print(ele.root.children, 1)

    def sub_print(self, children, i):
        indent = "    "
        for ele in children:
            if not ele.root.children:
                print(indent * i, "leave: ", ele.root.element)
            else:
                print(indent * i, "child: ", ele.root.element)
                ele.sub_print(ele.root.children, i + 1)
