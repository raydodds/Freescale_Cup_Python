#
#	node.py
#	Representation of nodes
#

__author__ = "Ray Dodds, Jonathan Schenk"

import line, trap

class Node(object):
	def __init__(self, parent=None, left=None, right=None, name=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right
		self.name = name

	# Replaces a node, fixes connections to parents and children
	def replace(self, replacement):
		for p in self.parent:
			if p.left == self:
				p.left = replacement
			elif p.right == self:
				p.right = replacement

	# Adds a node to the left of a node
	def add_left(self, node):
		self.left = node
		node.parent.append(self)

	# Adds a node to the right of a node
	def add_right(self, node):
		self.right = node
		node.parent.append(self)

	# Comparators
	def __eq__(self, other):
		return type(self) == type(other) and self == other

	def __ne__(self, other):
		return type(self) != type(other) or (type(self) == type(other) and self != other)

class PointNode(Node):
	def __init__(self, point, lindex, parent=None, left=None, right=None, name=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right
		self.point = point
		self.lindex = lindex
		self.name = name

	# Does point location
	def next(self, p):
		ret = None
		if p[0] < self.point[0]:
			ret = self.left
		else:
			ret = self.right
		return ret

	# Comparators
	def  __eq__(self, other):
		return (type(self) == type(other)) and (self.point == other.point)

	def __ne__(self, other):
		return self.point != other.point

	def __repr__(self):
		return "PointNode("+str(self.point)+', '+str(self.lindex)+')'


class SegNode(Node):
	def __init__(self, line, lindex, parent=None, left=None, right=None, name=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.left = left
		self.right = right
		self.line = line
		self.lindex = lindex
		self.name = name

	# Does point location
	def next(self, p):
		ret = None
		if self.line.above(p):
			ret = self.left
		else:
			ret = self.right
		return ret

	# comparators
	def __eq__(self, other):
		return (type(self) == type(other)) and (self.line == other.line)

	def __ne__(self, other):
		return self.line != other.line

	def __repr__(self):
		return 'SegNode('+str(self.line)+', '+str(self.lindex)+')'

class TrapNode(Node):
	def __init__(self, trap, parent=None, name=None):
		self.parent = []
		if(parent is not None):
			self.parent.append(parent)
		self.trap = trap
		self.trap.gnode = self
		self.tindex = -1
		self.name = name

	# Comparators
	def __eq__(self, other):
		return (type(self) == type(other)) and (self.trap == other.trap)

	def __ne__(self, other):
		return self.trap != other.trap

	def __repr__(self):
		return 'TrapNode('+str(self.trap)+', '+str(self.tindex)+')'	
