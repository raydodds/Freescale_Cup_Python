#!/usr/bin/python3
#
#	trapezoid_map.py
#	It does things, we swear.
#

__author__ = "Jonathan Schenk, Ray Dodds"

import trap, node		#Libs for representation of the lines, trapezoids,
import line as l				#and the tree.

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

	box = [int(x) for x in f.readline().strip().split()]

	bbox = [(box[1], box[0]), (box[2], box[1]), (box[3], box[2]), (box[0], box[3])]

	lines = []

	for fline in f:
		if(len(fline) > 1):
			s = [int(x) for x in fline.strip().split()]

			new_line = l.Line((s[0], s[1]), (s[2], s[3]))

			lines += [new_line]
	
	painTree = trap_map(bbox, lines)

	print(painTree)
	

def usage():
	print("Usage: ./trapezoid_map.py <linefile>")
	exit()

def trap_map(bounding_box, lines):
	#MAKE BOUNDING BOX INTO 4 POINT FOR THE CORNERS
	top = l.Line(bounding_box[0], bounding_box[1])
	bottom = l.Line(bounding_box[2], bounding_box[3])
	t = trap.Trap(top, bottom, bounding_box[0], bounding_box[2])
	root = node.TrapNode(t)


	for line in lines:
		root = add_line(root, line)

	return root

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
	new_root.add_left(node.TrapNode(left))

	x = node.PointNode(line.end)
	x.add_right(node.TrapNode(right))
	new_root.add_right(x)

	y = node.SegNode(line)
	y.add_left(node.TrapNode(top))
	y.add_right(node.TrapNode(bottom))
	x.add_left(y)

	if root is pt1_node:
		return new_root
	else:
		pt1_node.replace(new_root)
		return root

def handle_many(root, pt1_node, pt2_node, line):
	inbetween_traps = get_intersected_traps(root, line)

	# Lefty boy
	l_trap = inbetween_traps[0]

	# Create sub trapezoids
	left = trap.Trap(l_trap.top, l_trap.bottom, l_trap.left_pt, line.start)
	bottom = trap.Trap(line, l_trap.bottom, line.start, l_trap.right_pt)
	top = trap.Trap(l_trap.top, line, line.start, l_trap.right_pt)

	# Set neighbors
	left.set_neighbors(l_trap.topleft_n, top, l_trap.bottomleft_n, bottom)
	bottom.set_neighbors(left, None, left, None)
	top.set_neighbors(left, None, left, None)

	# Neighbors of neighbors
	if l_trap.topleft_n is not None:
		l_trap.topleft_n.topright_n = left
		l_trap.topleft_n.bottomright_n = left

	if l_trap.bottomleft_n is not None:
		l_trap.bottomleft_n.topright_n = left
		l_trap.bottomleft_n.bottomright_n = left

	# Set up subtree
	new_left = node.PointNode(line.start)
	new_split = node.SegNode(line)
	new_left.add_left(node.TrapNode(left))
	new_left.add_right(new_split)
	new_split.add_left(node.TrapNode(top))
	new_split.add_right(node.TrapNode(bottom))

	# Use a tangled web of references to replace this trapezoid with the subtree
	l_trap.gnode.replace(new_left)

	for i in range(1, len(inbetween_traps) - 1):
		curr_trap = inbetween_traps[i]

	return root



def get_intersected_traps(root, line):
	traps = []

	s = line.start
	e = line.end

	start = locate_point(root, s).trap
	traps.append(start)
	curr = start

	while curr is not None and (curr.right_pt is not None and e[0] >= curr.right_pt[0]):
		if line.above(curr.right_pt):
			curr = curr.bottomright_n
		else:
			curr = curr.topright_n
		if curr is not None:
			traps.append(curr)

	return traps


# Run the main function
if __name__ == "__main__":
	main()
