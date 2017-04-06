#second attempt at a more simple Kalman filter
#linear

#equation: Xk = Kk*Zk+(1-Kk)*Xk-1
#current estimation = kalman gain * measured value + (1-kalman gain) * previous estimate

class KF2:

	def __init__(self, x, y):
		
		self.Kk = 0.1 #determines how much it changes, guess based on average speed of vehicle
		self.Xk = x
		self.Xkp = x
		self.Yk = y
		self.Ykp = y
	
	#does some math and outputs estimated values
	def Kfilter(self, x, y):
 		
		self.Xk = self.Kk*x+(1-self.Kk)*self.Xkp
		self.Yk = self.Kk*y+(1-self.Kk)*self.Ykp
		self.Xkp = self.Xk
		self.Ykp = self.Yk
		return [self.Xk, self.Yk]


#testing
#KF = KF2(101.4, 34)
#print(KF.Kfilter(90, 30))
#print(KF.Kfilter(80, 30))
#print(KF.Kfilter(85, 40))
#print(KF.Kfilter(87, 45))

