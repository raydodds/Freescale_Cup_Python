#
#	line.py
#	A Line class
#

__author__ = "Ray Dodds, Jonathan Schenk"

class Line:
	def __init__(self, start, end):
		# Make sure the line is aligned left to right
		if( start[0] < end[0] ):
			self.start = start
			self.end = end
		else:
			self.start = end
			self.end = start
		
		# y = ax-b
		self.a = (end[1]-start[1])/(end[0]-start[0])

		# b = ax - y
		self.b = self.a*start[0] - start[1]

	def __repr__(self):
		rep = str(self.a)+"*x"

		if(self.b > 0):
			rep += "-"+str(self.b)
		else:
			rep += "+"+str(self.b)

		return rep

	# Find where two lines intersect
	def intersect(self, other):
		if(self.a == other.a):
			# Lines are parallel
			return None
		x = (self.b-other.b)/(self.a-other.a)
		y = self.a*x-self.b

		return (x,y)

	# Get the y for a given x
	def yAt(self, x):
		return self.a*x-self.b

	# Get the x for a given y
	def xAt(self, y):
		return (y+self.b)/(self.a)

	# Check if a point is within the x range of the line
	def in_x(self, point):
		return not ( self.start[0] > point[0] or self.end[0] < point[0] )

	# Check if a point is within the y range of the line
	def in_y(self, point):
		return not ( self.start[1] > point[1] or self.end[1] < point[1] )


