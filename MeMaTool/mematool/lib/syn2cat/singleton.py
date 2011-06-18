class Singleton(type):
	'''Implements the singleton pattern
	Inside a class simply write "__metaclass__ = Singleton"
	and the class will be unique'''

	def __init__(cls, name, bases, dict):
		super(Singleton, cls).__init__(name, bases, dict)
		cls.instance = None
 
	def __call__(cls, *args, **kw):
		if cls.instance is None:
			cls.instance = super(Singleton, cls).__call__(*args, **kw)

		return cls.instance
