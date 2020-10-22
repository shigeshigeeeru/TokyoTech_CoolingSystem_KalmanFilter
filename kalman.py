
import numpy as np
import matplotlib.pyplot as plt

from scipy.stats import norm
import matplotlib.pyplot as plt

def getT(adc):
	R25 = 10.
	Rext= 10.
	B= 3173.
	T0= 273.15+27.0
	r=adc/1024.
	R=Rext * (1. -r)/r
	T = 1./(np.log(R/R25)/B + 1./T0)
	return T-273.15

#x_pre = np.array([1,2],[3,4])
filename = 'test.txt'

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
sigma_w=np.sqrt(100.0) #depends on adc flucuation
sigma_v=1.0 #depends on system noise
#y_before=0
#y_after=0
y=[]
t=[]
T_raw=0.
T_guess=0.

total=0.
ave=0.
sum2jou=0.
n=30
STEP=100

dist = \
np.random.normal(
		loc = 0, #mean
		scale = 1, #sigma
		size = STEP, #sample size
)#random number using gaussian pdf.

f= open("meas_30.txt")
for i in range(100):
    contents = f.readline()
    y.append(float(contents))
    t.append(i)
    total = total + y[i]
f.close()
ave = total/100.
for i in range(100):
    sum2jou = sum2jou + (y[i]-ave)**2
sigma = np.sqrt(sum2jou/(100.-1.))
#print('whole')
#print(sigma)
sigma_w = sigma
x_post[0] = y[0]
#y.pop(0)
#with open(filename , 'a') as file_object:	
with open(filename , 'w') as file_object:#new file
    for i in range(99):
        ###PREPARE DATA###
        #t.append(i+1)
        #y.append(y[i]+dist[i])
        #print(t[i],y[i])
        total=0.
        ave=0.
        sum2jou=0. 
        for j in range(n):
                total = total + y[i-j]
        ave=total/float(n)
        
        for j in range(n):
                sum2jou = sum2jou + (y[i-j] - ave)**2
        sigma = np.sqrt(sum2jou/(float(n)-1.))
        #print(sigma)

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
        
        T_ave = getT(ave)
        T_raw = getT(y[i])
        T_guess = getT(x_post[i])
        #print(t[i],y[i],x_post[i],ave,T_raw,T_guess,T_ave)
        #data_list = str(t[i]) + ' ' + str(y[i]) + ' ' + str(x_post[i]) + ' ' +  str(gain[i]) + '\n'
        data_list = str(t[i]) + ' ' + str(T_raw) + ' ' + str(T_guess) + ' ' + str(T_ave) + '\n'
        file_object.write(data_list)
file_object.close()
#plt.plot(t,y,color='r')
#plt.xlim(0,STEP)
