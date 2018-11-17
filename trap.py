#
#	trap.py
#	A representation of trapezoids in 2d space
#

__author__ = "Ray Dodds, Jonathan Schenk"

import line

class Trap:
	# Top line, bottom line, left bounding point, right bounding point
	def __init__(self, top, bottom, left_pt=None, right_pt=None):
		if(left_pt is None and right_pt is None):
			return None

		self.topleft_n = None
		self.topright_n = None
		self.bottomleft_n = None
		self.bottomright_n = None

		self.gnode = None

		# (x,y)
		self.left_pt = left_pt
		self.right_pt = right_pt
		if( left_pt != None and right_pt != None ):
			if( left_pt[0] > right_pt[0]):
				self.left_pt = right_pt
				self.right_pt = left_pt

		# line.Line
		self.top = top
		self.bottom = bottom

		self.corners = []

		#left side
		if(left_pt is not None):
			x = self.left_pt[0]
			tl = (x, self.top.yAt(x))
			bl = (x, self.bottom.yAt(x))
			self.corners += [tl]
			if(tl != bl):
				self.corners += [bl]
		# right side
		if(right_pt is not None):
			x = self.right_pt[0]
			tr = (x, self.top.yAt(x))
			br = (x, self.bottom.yAt(x))
			self.corners += [tr]
			if( tr != br ):
				self.corners += [br]

	def set_neighbors(self,tl,tr,bl,br):
		self.topleft_n = tl
		self.topright_n = tr
		self.bottomleft_n = bl
		self.bottomright_n = br

	def __repr__(self):
		return 'Trap('+str(self.corners)+')'

def tests():

	pt0 = (0,0)
	pt1 = (0,1)
	pt2 = (1,1)
	pt3 = (1,0)
	pt4 = (0,2)
	pt5 = (2,2)
	pt6 = (2,0)

	l0 = line.Line(pt0, pt3)
	l1 = line.Line(pt1, pt2)

	t0 = Trap(l1, l0, pt0, pt3)
	print(l1, l0)
	print(t0)
	

if( __name__ == '__main__' ):
	tests()
