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

# Used for naming the trapezoids based on their order of creation
trapNum = 0

def main():
	global trapNum

	# Handle args
	if( len( sys.argv ) != 2 ):
		usage

	try:
		f=open(sys.argv[1])
	except FileNotFoundError as e:
		print("Could not find a file at "+sys.argv[1])
		exit()

	# Read in the file and make it into some lines
	numLines = int(f.readline())

	# Set up the bounding box
	box = [int(x) for x in f.readline().strip().split()]
	
	bbox = [(box[1], box[0]), (box[2], box[1]), (box[3], box[2]), (box[0], box[3])]

	lines = []

	for fline in f:
		if(len(fline) > 4):
			s = [int(x) for x in fline.strip().split()]

			new_line = l.Line((s[0], s[1]), (s[2], s[3]))

			lines += [new_line]

	# Make the trapezoids into a tree
	painTree = trap_map(bbox, lines)
	
	# Generates the matrix from the tree.
	resmat = t.traverse(painTree, lines)

	# Save the results to a file
	o = open('results.tsv', 'w+')

	for mline in resmat:
		for i in range(len(mline)):
			if(i < len(mline)-1):
				o.write(str(mline[i])+'\t')
			else:
				o.write(str(mline[i])+'\n')

	o.close()
	print("Results matrix saved to results.tsv.")

	# Promptable point location
	print("Find a point? <x> <y>")
	while( True ):
		
		inline = input('pt> ').strip()

		if(inline.lower() in ('', 'exit', 'q', 'stop')):
			print("Finished.")
			exit()
		
		x, y, *leftovers = [int(x) for x in inline.split()]

		path = locate_route(painTree, (x,y))

		print(path)



	



	

def usage():
	print("Usage: ./trapezoid_map.py <linefile>")
	exit()

def trap_map(bounding_box, lines):
	global trapNum
	#MAKE BOUNDING BOX INTO 4 POINT FOR THE CORNERS
	top = l.Line(bounding_box[0], bounding_box[1])
	bottom = l.Line(bounding_box[2], bounding_box[3])
	t = trap.Trap(top, bottom, bounding_box[0], bounding_box[2])
	root = node.TrapNode(t, name='T'+str(trapNum))
	trapNum += 1
		

	for i in range(len(lines)):
		root = add_line(root, lines[i], i)

	return root

def add_line(root, line, lindex):
	pt1_node = locate_point(root, line.start)
	pt2_node = locate_point(root, line.end)

	pt1_trap = pt1_node.trap
	pt2_trap = pt2_node.trap

	if pt1_trap == pt2_trap or pt1_trap.right_pt == line.end:
		return handle_one(root, pt1_node, line, lindex)
	elif pt1_trap.left_pt == line.start:
		return handle_one(root, pt2_node, line, lindex)
	else:
		return handle_many(root, pt1_node, pt2_node, line, lindex)

#returns trapezoid the point is located in
def locate_point(root, p):
	curr = root
	while not isinstance(curr, node.TrapNode):
		curr = curr.next(p)
	return curr

#returns a string of names from the root to the pointed node
def locate_route(root, p, path=''):
	curr = root
	while not isinstance(curr, node.TrapNode):
		path += '->'+curr.name
		curr = curr.next(p)
	path += '->'+curr.name
	return path 


def handle_one(root, pt1_node, line, lindex):
	global trapNum
	t = pt1_node.trap

	left = trap.Trap(t.top, t.bottom, t.left_pt, line.start)
	#left.parent.append(t.parent)
	right = trap.Trap(t.top, t.bottom, line.end, t.right_pt)
	#right.parent.append(t.parent)
	top = trap.Trap(t.top, line, line.start, line.end)
	#top.parent.append(t.parent)
	bottom = trap.Trap(line, t.bottom, line.start, line.end)
	#bottom.parent.append(t.parent)

	new_root = node.PointNode(line.start, lindex, name='P'+str(lindex))
	x = node.PointNode(line.end, lindex, name='Q'+str(lindex))
	y = node.SegNode(line, lindex, name='S'+str(lindex))

	if(left.left_pt[0] == left.right_pt[0] and left.left_pt[1] == left.right_pt[1]):
		right.set_neighbors(top, right.topright_n, bottom, right.bottomright_n)
		top.set_neighbors(t.topleft_n, right, None, None)
		bottom.set_neighbors(t.topleft_n, right, None, None)

		if t.topleft_n is not None:
			if t.topleft_n.topright_n == t:
				t.topleft_n.topright_n = top
			else:
				t.topleft_n.bottomright_n = bottom
		if t.bottomleft_n is not None:
			if t.bottomleft_n.topright_n == t:
				t.bottomleft_n.topright_n = top
			else:
				t.bottomleft_n.bottomright_n = bottom
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
		new_root = x
		new_root.add_right(node.TrapNode(right, name='T'+str(trapNum)))
		trapNum += 1

		y.add_left(node.TrapNode(top, name='T'+str(trapNum)))
		trapNum += 1
		y.add_right(node.TrapNode(bottom, name='T'+str(trapNum)))
		trapNum += 1
		new_root.add_left(y)
		
	elif(right.left_pt[0] == right.right_pt[0] and right.left_pt[1] == right.right_pt[1]):
		left.set_neighbors(left.topleft_n, top, left.bottomleft_n, bottom)
		top.set_neighbors(left, t.topright_n, None, None)
		bottom.set_neighbors(left, t.bottomright_n, None, None)

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
				t.topright_n.topleft_n = top
			else:
				t.topright_n.bottomleft_n = top
		if t.bottomright_n is not None:
			if t.bottomright_n.topleft_n == t:
				t.bottomright_n.topleft_n = bottom
			else:
				t.bottomright_n.bottomleft_n = bottom
		# Make a mini tree
		new_root.add_left(node.TrapNode(left, name='T'+str(trapNum)))
		trapNum += 1

		y.add_left(node.TrapNode(top, name='T'+str(trapNum)))
		trapNum += 1
		y.add_right(node.TrapNode(bottom, name='T'+str(trapNum)))
		trapNum += 1
		new_root.add_right(y)

	else:
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
		new_root.add_left(node.TrapNode(left, name='T'+str(trapNum)))
		trapNum += 1

		x.add_right(node.TrapNode(right, name='T'+str(trapNum)))
		trapNum += 1
		new_root.add_right(x)

		y.add_left(node.TrapNode(top, name='T'+str(trapNum)))
		trapNum += 1
		y.add_right(node.TrapNode(bottom, name='T'+str(trapNum)))
		trapNum += 1
		x.add_left(y)

	if root is pt1_node:
		return new_root
	else:
		pt1_node.replace(new_root)
		return root

def handle_many(root, pt1_node, pt2_node, line, lindex):
	global trapNum
	inbetween_traps = get_intersected_traps(root, line)
	#print(inbetween_traps)

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
	new_left = node.PointNode(line.start, lindex, name='P'+str(lindex))
	lnew_split = node.SegNode(line, lindex, name='S'+str(lindex))
	rnew_split = node.SegNode(line, lindex, name='S'+str(lindex))
	new_left.add_left(node.TrapNode(left, name='T'+str(trapNum)))
	trapNum += 1
	new_left.add_right(lnew_split)
	top_node = node.TrapNode(continuous_top, name='T'+str(trapNum))
	trapNum += 1
	lnew_split.add_left(top_node)
	top_node.parent.append(rnew_split)
	bottom_node = node.TrapNode(continuous_bottom, name='T'+str(trapNum))
	trapNum += 1
	lnew_split.add_right(bottom_node)
	bottom_node.parent.append(rnew_split)

	# Use a tangled web of references to replace this trapezoid with the subtree
	l_trap.gnode.replace(new_left)

	mnew_split = node.SegNode(line, lindex, name='S'+str(lindex))
	curr_trap = None
	prev_trap = None
	for i in range(1, len(inbetween_traps)):
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
			top_node = node.TrapNode(continuous_top, name='T'+str(trapNum))
			trapNum += 1

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
			bottom_node = node.TrapNode(continuous_bottom, name='T'+str(trapNum))
			trapNum += 1

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

		if(curr_trap == inbetween_traps[-1]):
			break

		mnew_split = node.SegNode(line, lindex, name='S'+str(lindex))
		mnew_split.add_left(top_node)
		mnew_split.add_right(bottom_node)
		curr_trap.gnode.replace(mnew_split)

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
	new_right = node.PointNode(line.end, lindex, name='Q'+str(lindex))
	top_node = node.TrapNode(continuous_top, name='T'+str(trapNum))
	trapNum += 1
	rnew_split.add_left(top_node)
	top_node.parent.append(lnew_split)
	top_node.parent.append(mnew_split)
	bottom_node = node.TrapNode(continuous_bottom, name='T'+str(trapNum))
	trapNum += 1
	rnew_split.add_right(bottom_node)
	bottom_node.parent.append(lnew_split)
	bottom_node.parent.append(mnew_split)
	new_right.add_left(rnew_split)
	new_right.add_right(node.TrapNode(right, name='T'+str(trapNum)))
	trapNum += 1

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
