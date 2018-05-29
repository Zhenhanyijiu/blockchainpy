class Screen(object):
	@property
	def width(self):
		return self._width
	@width.setter
	def width(self,v):
		if not isinstance(v,int):
			raise ValueError('width must be integer')
		if v<0 or v==0:
			raise ValueError('width must be larger than 0')
		self._width=v
	@property
	def height(self):
		return self._height
	@height.setter
	def height(self,v):
		if not isinstance(v,int):
			raise ValueError("height must be integer")
		if v<0 or v==0:
			raise ValueError('height must be larger than 0')
		self._height=v
	@property
	def resolution(self):
		return (self._width,self._height)

s=Screen()
s.width=46
print(s.width)
s.height=100
print(s.height)
print(s.resolution)
#print(dir(s))