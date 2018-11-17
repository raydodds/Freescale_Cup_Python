#
#	node.py
#	Representation of nodes
#

__author__ = "Ray Dodds, Jonathan Schenk"

import line, trap

class Node(object):
	def __init__(self, parent=None, left=None, right=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right

	def replace(self, replacement):
		for p in self.parent:
			if p.left is self:
				p.left = replacement
			elif p.right is self:
				p.right = replacement

	def add_left(self, node):
		self.left = node
		node.parent.append(self)

	def add_right(self, node):
		self.right = node
		node.parent.append(self)

class PointNode(Node):
	def __init__(self, point, parent=None, left=None, right=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right
		self.point = point

	def next(self, p):
		ret = None
		if p[0] < self.point[0]:
			ret = self.left
		else:
			ret = self.right
		return ret

	def  __eq__(self, other):
		return self.point == other.point

	def __ne__(self, other):
		return self.point != other.point


class SegNode(Node):
	def __init__(self, line, parent=None, left=None, right=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right
		self.line = line

	def next(self, p):
		ret = None
		if self.line.above(p):
			ret = self.left
		else:
			ret = self.right
		return ret

	def __eq__(self, other):
		return self.line == other.line

	def __ne__(self, other):
		return self.line != other.line

	def __repr__(self):
		return 'SegNode('+str(line)+')'

class TrapNode(Node):
	def __init__(self, trap, parent=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.trap = trap
		self.trap.gnode = self

	def __repr__(self):
		return 'TrapNode('+str(self.trap)+')'	
