#!/usr/bin/python3
#
#	trapezoid_map.py
#	It does things, we swear.
#

__author__ = "Jonathan Schenk, Ray Dodds"

import line, trap, node		#Libs for representation of the lines, trapezoids,
							#and the tree.

import sys					#For handling arguments

def main():
	
	if( len( sys.argv ) != 2 ):
		usage

	try:
		f=open(sys.argv[1])
	except FileNotFoundError as e:
		print("Could not find a file at "+sys.argv[1])
		exit()

	numLines = int(f.readline())

	boundingBox = [int(x) for x in f.readline().strip().split()]

	lines = []

	for line in f:
		s = [int(x) for x in line.strip().split()]

		new_line = line.Line((s[0], s[1]), (s[2], s[3]))

		lines += [new_line]


def usage():
	print("Usage: ./trapezoid_map.py <linefile>")
	exit()

def trap_map(bounding_box, lines):
	#MAKE BOUNDING BOX INTO 4 POINT FOR THE CORNERS
	top = line.Line(bounding_box[0], bounding_box[1])
	bottom = line.Line(bounding_box[2], bounding_box[3])
	t = trap.Trap(top, bottom, bounding_box[0][0], bounding_box[0][1])
	root = node.TrapNode(t)

	for line in lines:
		root = add_line(root, line)

def add_line(root, line):
	pt1_node = locate_point(root, line.start)
	pt2_node = locate_point(root, line.end)
	pt1_trap = pt1_node.trap
	pt2_trap = pt2_node.trap

	if pt1_trap == pt2_trap:
		return handle_one(root, pt1_node, line)
	else:
		return handle_many(root, pt1_node, pt2_node, line)

#returns trapezoid the point is located in
def locate_point(root, p):
	curr = root
	while not isinstance(curr, node.TrapNode):
		curr = curr.next(p)
	return curr

def handle_one(root, pt1_node, line):
	t = pt1_node.trap

	left = trap.Trap(t.top, t.bottom, t.left_pt, line.start)
	right = trap.Trap(t.top, t.bottom, line.end, t.right_pt)
	top = trap.Trap(t.top, line, line.start, line.end)
	bottom = trap.Trap(line, t.bottom, line.start, line.end)

	left.set_neighbors(left.topleft_n, top, left.bottomleft_n, bottom)
	right.set_neighbors(top, right.topright_n, bottom, right.bottomright_n)
	top.set_neighbors(left, right, left, right)
	bottom.set_neighbors(left, right, left, right)

	# Set neighbors of neighbors. Might be incorrect.
	if t.topleft_n is not None:
		t.topleft_n.topright_n = left
		t.topleft_n.bottomright_n = left
	if t.bottomleft_n is not None:
		t.bottomleft_n.topright_n = left
		t.bottomleft_n.bottomright_n = left
	if t.topright_n is not None:
		t.topright_n.topleft_n = right
		t.topright_n.bottomleft_n = right
	if t.bottomright_n is not None:
		t.bottomright_n.topleft_n = right
		t.bottomright_n.bottomleft_n = right

	# Make a mini tree
	new_root = node.PointNode(line.start)
	new_root.left = node.TrapNode(left)

	x = node.PointNode(line.end)
	x.right = nodeTrapNode(right)
	new_root.right = x

	y = node.LineNode(line)
	y.left = node.TrapNode(top)
	y.right = node.TrapNode(bottom)
	x.left = y

	if root is pt1_node:
		return new_root
	else:
		pt1_node.replace(new_root)
		return root


# Run the main function
if __name__ == "__main__":
	main()
