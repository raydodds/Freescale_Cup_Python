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

class SegNode(Node):
	def __init__(self, parent, line, left=None, right=None):
		self = Node(parent, left, right)
		self.line = line


class TrapNode(Node):
	def __init__(self, parent, trap):
		self = Node(parent)
		self.trap = trap
