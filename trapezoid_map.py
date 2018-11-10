__author__ = "Jonathan Schenk, Ray Dodds"

import line, trap, node

def trap_map(bounding_box, lines):
    #MAKE BOUNDING BOX INTO 4 POINT FOR THE CORNERS
    top = line.Line(bounding_box[0], bounding_box[1])
    bottom = line.Line(bounding_box[2], bounding_box[3])
    t = trap.Trap(top, bottom, bounding_box[0][0], bounding_box[0][1])
    root = node.TrapNode(t)

    for line in lines:
        add_line(root, line)

def add_lines(root, line):
    pt1_node = locate_point(root, line.start)
    pt2_node = locate_point(root, line.end)
    pt1_trap = pt1_node.trap
    pt2_trap = pt2_node.trap

    if pt1_trap == pt2_trap:
        handle_one(root, pt1_node, line)
    else:
        handle_many(root, pt1_node, pt2_node, line)

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
