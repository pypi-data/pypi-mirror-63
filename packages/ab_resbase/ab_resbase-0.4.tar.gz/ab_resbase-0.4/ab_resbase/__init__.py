import random
class start():
	def __init__(self,min=0,max=1,maxdate=10):
		self.restart(min,max,maxdate)
	def restart(self,min=0,max=1,maxdate=10):	
		self._min_=min
		self._max_=max
		self._maxdate_=maxdate
		self._data_=[]
		self._Interval_=(self._max_-self._min_)/self._maxdate_
		for i in range(maxdate):
			self._data_.append(float("%2.3f"%(i*self._Interval_)))
		self.ans=self._data_[random.randint(0,len(self._data_))]
	def guess(self,data):
		if type(data) == type(self._data_[0]):
			if data in self._data_:

				if data!=self.ans:
					self._data_.remove(data)
					self._Interval_=float("%2.3f"%((self._max_-self._min_)/len(self._data_)))
				return self._Interval_
		return None