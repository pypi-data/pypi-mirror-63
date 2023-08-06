import random
def start(self,min=0,max=1,maxdate=10):
	restart(min,max,maxdate)
def restart(min=0,max=1,maxdate=10):	
	_min_=min
	_max_=max
	_maxdate_=maxdate
	_data_=[]
	_Interval_=(_max_-_min_)/_maxdate_
	for i in range(maxdate):
		_data_.append(float("%2.3f"%(i*_Interval_)))
	ans=_data_[random.randint(0,len(_data_))]
def guess(self,data):
	if type(data) == type(_data_[0]):
		if data in _data_:

			if data!=ans:
				_data_.remove(data)
				_Interval_=float("%2.3f"%((_max_-_min_)/len(_data_)))
			return _Interval_
	return None