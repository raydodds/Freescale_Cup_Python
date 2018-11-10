#
#	node.py
#	Representation of nodes
#

__author__ = "Ray Dodds, Jonathan Schenk"

import line, trap

class Node(object):
	def __init__(self, parent, left=None, right=None):
		self.parent = parent
		self.left = left
		self.right = right

class PointNode(Node):
	def __init__(self, parent, point, left=None, right=None):
		self = Node(parent, left, right)
		self.point = point

    def next(self, p):
        ret = None
        if p[0] < self.point[0]:
            ret = self.left
        else:
            ret = self.right
        return ret


class SegNode(Node):
	def __init__(self, parent, line, left=None, right=None):
		self = Node(parent, left, right)
		self.line = line

    def next(self, p):
        ret = None
        if self.line.above(p):
            ret = self.left
        else:
            ret = self.right
        return ret

class TrapNode(Node):
	def __init__(self, parent, trap):
		self = Node(parent)
		self.trap = trap
