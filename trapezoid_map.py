#!/usr/bin/python3
#
#	trapezoid_map.py
#	It does things, we swear.
#

__author__ = "Jonathan Schenk, Ray Dodds"

import trap, node		#Libs for representation of the lines, trapezoids,
import line as l				#and the tree.

import traverse as t

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

	resmat = t.traverse(painTree, lines)

	for mline in resmat:
		for i in range(len(mline)):
			if(i < len(mline)-1):
				print(mline[i], end=',')
			else:
				print(mline[i])
	



	

def usage():
	print("Usage: ./trapezoid_map.py <linefile>")
	exit()

def trap_map(bounding_box, lines):
	#MAKE BOUNDING BOX INTO 4 POINT FOR THE CORNERS
	top = l.Line(bounding_box[0], bounding_box[1])
	bottom = l.Line(bounding_box[2], bounding_box[3])
	t = trap.Trap(top, bottom, bounding_box[0], bounding_box[2])
	root = node.TrapNode(t)


	for i in range(len(lines)):
		root = add_line(root, lines[i], i)

	return root

def add_line(root, line, lindex):
	pt1_node = locate_point(root, line.start)
	pt2_node = locate_point(root, line.end)

	pt1_trap = pt1_node.trap
	pt2_trap = pt2_node.trap

	if pt1_trap == pt2_trap:
		return handle_one(root, pt1_node, line, lindex)
	else:
		return handle_many(root, pt1_node, pt2_node, line, lindex)

#returns trapezoid the point is located in
def locate_point(root, p):
	curr = root
	while not isinstance(curr, node.TrapNode):
		curr = curr.next(p)
	return curr

def handle_one(root, pt1_node, line, lindex):
	t = pt1_node.trap

	left = trap.Trap(t.top, t.bottom, t.left_pt, line.start)
	right = trap.Trap(t.top, t.bottom, line.end, t.right_pt)
	top = trap.Trap(t.top, line, line.start, line.end)
	bottom = trap.Trap(line, t.bottom, line.start, line.end)

	left.set_neighbors(left.topleft_n, top, left.bottomleft_n, bottom)
	right.set_neighbors(top, right.topright_n, bottom, right.bottomright_n)
	top.set_neighbors(left, right, None, None)
	bottom.set_neighbors(left, right, None, None)

	# Set neighbors of neighbors. Might be incorrect.
	if t.topleft_n is not None:
		if t.topleft_n.topright_n == t:
			t.topleft_n.topright_n = left
		else:
			t.topleft_n.bottomright_n = left
	if t.bottomleft_n is not None:
		if t.bottomleft_n.topright_n == t:
			t.bottomleft_n.topright_n = left
		else:
			t.bottomleft_n.bottomright_n = left
	if t.topright_n is not None:
		if t.topright_n.topleft_n == t:
			t.topright_n.topleft_n = right
		else:
			t.topright_n.bottomleft_n = right
	if t.bottomright_n is not None:
		if t.bottomright_n.topleft_n == t:
			t.bottomright_n.topleft_n = right
		else:
			t.bottomright_n.bottomleft_n = right

	# Make a mini tree


	new_root = node.PointNode(line.start, lindex)
	new_root.add_left(node.TrapNode(left))

	x = node.PointNode(line.end, lindex)
	x.add_right(node.TrapNode(right))
	new_root.add_right(x)

	y = node.SegNode(line, lindex)
	y.add_left(node.TrapNode(top))
	y.add_right(node.TrapNode(bottom))
	x.add_left(y)

	if root is pt1_node:
		return new_root
	else:
		pt1_node.replace(new_root)
		return root

def handle_many(root, pt1_node, pt2_node, line, lindex):
	inbetween_traps = get_intersected_traps(root, line)

	# Lefty boy
	l_trap = inbetween_traps[0]

	# Create sub trapezoids
	left = trap.Trap(l_trap.top, l_trap.bottom, l_trap.left_pt, line.start)
	continuous_bottom = trap.Trap(line, l_trap.bottom, line.start, l_trap.right_pt)
	continuous_top = trap.Trap(l_trap.top, line, line.start, l_trap.right_pt)

	# Set neighbors
	left.set_neighbors(l_trap.topleft_n, continuous_top, l_trap.bottomleft_n, continuous_bottom)
	continuous_bottom.set_neighbors(left, None, None, None)
	continuous_top.set_neighbors(left, None, None, None)

	# Neighbors of neighbors
	if l_trap.topleft_n is not None:
		if l_trap.topleft_n.topright_n == l_trap:
			l_trap.topleft_n.topright_n = left
		else:
			l_trap.topleft_n.bottomright_n = left

	if l_trap.bottomleft_n is not None:
		if l_trap.bottomleft_n.topright_n == l_trap:
			l_trap.bottomleft_n.topright_n = left
		else:
 			l_trap.bottomleft_n.bottomright_n = left

	# Set up subtree
	new_left = node.PointNode(line.start, lindex)
	new_split = node.SegNode(line, lindex)
	new_left.add_left(node.TrapNode(left))
	new_left.add_right(new_split)
	top_node = node.TrapNode(continuous_top)
	new_split.add_left(top_node)
	bottom_node = node.TrapNode(continuous_bottom)
	new_split.add_right(bottom_node)

	# Use a tangled web of references to replace this trapezoid with the subtree
	l_trap.gnode.replace(new_left)

	curr_trap = None
	pre_trap = None
	for i in range(1, len(inbetween_traps) - 1):
		curr_trap = inbetween_traps[i]
		prev_trap = inbetween_traps[i-1]
		pinch_top = False

		if prev_trap.bottomright_n is not None and prev_trap.topright_n is not None:
			pinch_top = (prev_trap.bottomright_n == curr_trap)
		elif curr_trap.bottomleft_n == prev_trap or curr_trap.topleft_n == prev_trap:
			pinch_top = (curr_trap.bottomleft_n == prev_trap)

		if pinch_top:
			continuous_top.right_pt = curr_trap.left_pt
			old_top = continuous_top
			continuous_top = trap.Trap(curr_trap.top, line,\
								curr_trap.left_pt, curr_trap.right_pt)
			top_node = node.TrapNode(continuous_top)

			if curr_trap.bottomleft_n is not None and curr_trap.topleft_n is not None:
				old_top.set_neighbors(None, continuous_top, None, None)
				continuous_top.set_neighbors(curr_trap.topleft_n, None, old_top, None)
				curr_trap.topleft_n.topright_n = continuous_top
				curr_trap.topleft_n.bottomright_n = None
			else:
				old_top.bottomright_n = continuous_top
				old_top.topright_n = prev_trap.topright_n
				prev_trap.topright_n.topleft_n = old_top
				prev_trap.topright_n.bottomleft_n = None
				continuous_top.set_neighbors(old_top, None, None, None)

		else:
			continuous_bottom.right_pt = curr_trap.left_pt
			old_bottom = continuous_bottom
			continuous_bottom = trap.Trap(line, curr_trap.bottom,\
								curr_trap.left_pt, curr_trap.right_pt)
			bottom_node = node.TrapNode(continuous_bottom)

			if curr_trap.bottomleft_n is not None and curr_trap.topleft_n is not None:
				old_bottom.set_neighbors(None, continuous_bottom, None, None)
				continuous_bottom.set_neighbors(old_bottom, None, curr_trap.bottomleft_n, None)
				curr_trap.bottomleft_n.topright_n = continuous_bottom
				curr_trap.bottomleft_n.bottomright_n = None
			else:
				old_bottom.topright_n = continuous_bottom
				old_bottom.bottomright_n = prev_trap.bottomright_n
				prev_trap.bottomright_n.topleft_n = old_bottom
				prev_trap.bottomright_n.bottomleft_n = None
				continuous_bottom.set_neighbors(old_bottom, None, None, None)

		new_split = node.SegNode(line, lindex)
		new_split.add_left(top_node)
		new_split.add_right(bottom_node)
		curr_trap.gnode.replace(new_split)

	r_trap = inbetween_traps[-1]
	continuous_top.right_pt = line.end
	continuous_bottom.right_pt = line.end
	right = trap.Trap(r_trap.top, r_trap.bottom, line.end, r_trap.right_pt)

	# Set neighbors
	right.set_neighbors(continuous_top, r_trap.topright_n, continuous_bottom, r_trap.bottomright_n)
	continuous_bottom.set_neighbors(None, right, None, None)
	continuous_top.set_neighbors(None, right, None, None)

	# Neighbors of neighbors
	if r_trap.topright_n is not None:
		if r_trap.topright_n.topleft_n == r_trap:
			r_trap.topright_n.topleft_n = right
		else:
			r_trap.topright_n.bottomleft_n = right

	if r_trap.bottomright_n is not None:
		if r_trap.bottomright_n.topleft_n == r_trap:
			r_trap.bottomright_n.topleft_n = right
		else:
 			r_trap.bottomright_n.bottomleft_n = right

	# Set up subtree
	new_right = node.PointNode(line.end, lindex)
	new_split = node.SegNode(line, lindex)
	top_node = node.TrapNode(continuous_top)
	new_split.add_left(top_node)
	bottom_node = node.TrapNode(continuous_bottom)
	new_split.add_right(bottom_node)
	new_right.add_left(new_split)
	new_right.add_right(node.TrapNode(right))

	r_trap.gnode.replace(new_right)

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
