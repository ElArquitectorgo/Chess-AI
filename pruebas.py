from Tree import*

tree = Tree(3)
tree.insert(tree.root, 4)
tree.insert(tree.root, 5)
tree.insert(Node(4), 6)
tree.insert(Node(4), 7)

tree.insert(Node(6), 10)
tree.insert(Node(6), 11)

tree.insert(Node(5), 8)
tree.insert(Node(5), 9)

tree.print()

hojas = list()
hojas = tree.get_leaves(tree, hojas)
print(hojas)

for hoja in hojas:
	print(hoja.get_father())

for i in range(5):
	if i == 3:
		pass
	print(i)
	