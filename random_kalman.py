
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm
import matplotlib.pyplot as plt

filename = 'test_random.txt'

#initialize
gain=[0.]
x_pre=[0.]
P_pre=[0.]
x_post=[0.]
P_post=[1.]
#basically uesing P[0] = gamma * I

A=1.0
b=1.0
c=1.0
sigma_w=8.0 #depends on adc flucuation
sigma_v=8.0 #depends on system noise
#y_before=0
#y_after=0
y=[]
t=[]
T_raw=0.
T_guess=0.

total=0.
ave=0.
sum2jou=0.
n=10
STEP=100

dist = \
np.random.normal(
		loc = 0, #mean
		scale = 8, #sigma
		size = STEP, #sample size
)#random number using gaussian pdf.

y.append(0.)
#x_post[0] = y[0]
#with open(filename , 'a') as file_object:	
with open(filename , 'w') as file_object:#new file
			for i in range(STEP-1):
				###PREPARE DATA###
				t.append(i+1)
				y.append(y[0]+dist[i])
				#print(t[i],y[i])
				total=0.
				ave=0.
				sum2jou=0. 
				if (i > n):
					for j in range(n):
						total = total + y[i-j]
					ave=total/float(n)
				else :
					for j in range(i):
						total = total + y[i-j]
					ave=total/float(i+1)
				###PREDICTION STEP###
				x= A * x_post[i]
				x_pre.append(x)
				P= A * P_post[i] * A + sigma_v*sigma_v * b*b
				P_pre.append(P)
				###FILTALING STEP###

				g = (P_pre[i+1]*c) / (c*P_pre[i+1]*c + sigma_w*sigma_w)
				gain.append(g)
				x = x_pre[i+1] + gain[i+1] * (y[i+1] -c*x_pre[i+1])
				x_post.append(x)
				P = (1. - gain[i+1]) * P_pre[i+1]
				P_post.append(P)

				#print(t[i],y[i],x_post[i],ave,T_raw,T_guess,T_ave)
				#data_list = str(t[i]) + ' ' + str(y[i]) + ' ' + str(x_post[i]) + ' ' +  str(gain[i]) + '\n'
				data_list = str(t[i]) + ' ' + str(y[i]) + ' ' + str(x_post[i]) + ' ' + str(ave) + '\n'
				file_object.write(data_list)
			file_object.close()
#plt.plot(t,y,color='r')
#plt.xlim(0,STEP)
