
# persistent random walk tutorial  
########################################################################
# run the persistent random walk on a 1D lattice  
#
# create a movie of the position probability distribution evolving in time	
#
# notes:
# probability alpha to continue moving in same direction as previous time step
# particle speed fixed to 1 (random walk on integer lattice)
######################################################################## 	

#import
import numpy as np
import math as m



#set the constant parameters

T=100  #number of time steps in random walk trajectory

N=10000  #number of trajectories in ensemble

alpha=0.97 #persistence level

print("T =",T)
print("N =",N)
print("alpha =",alpha)


x_0=0.0 #initial position


#randomly select initial velocity
v_0=np.random.rand(N,1)-0.5

for n in range (N):
	if v_0[n] < 0:
		v_0[n] = -1.0
	else: 
		v_0[n] = 1.0
	
#print("v_0 =",v_0)


#initialize arrays that will hold random walk trajectories

x_vals=np.zeros((N, T),dtype=float)  #position trajectory
v_vals=np.zeros((N, 1),dtype=float)	 #velocity trajectory

x_vals[:,0]=x_0
v_vals=v_0
					


#initialize array that will hold position probability distribution

Nx=2*(T-1)+1  #number of sites within range of random walk 
Px=np.zeros((Nx, T),dtype=float)  #probability distribution 

#array of possible position values
xP=np.zeros(Nx,dtype=float) 
for i in range (Nx):
	xP[i]=-1.0*(T-1)+i
	
	

for t in range (T-1):

	print("t =",t)
		
	#print("v_vals =\n",v_vals)
	#print("x_vals =\n",x_vals)
	
	#update probability distribution
	for n in range(N):
		ix = int(x_vals[n,t]+T-1)
		Px[ix,t]=Px[ix,t]+1.0/N
		
	#print("Px[:,t] =\n",Px[:,t])
					
	#update position
	for n in range(N):			
		x_vals[n,t+1]=x_vals[n,t]+v_vals[n,0]
			
	#update velocity	
	p=np.random.rand(N,1)
	#print("p =\n",p)
		
	for n in range (N):
		if p[n] > alpha:
			v_vals[n] = -1.0*v_vals[n,0]
	
		
#print("x_vals =\n",x_vals)




#create animation of the position probability distribution time evolution 
print("animating...")

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

x0 = []
y0 = []

fig, ax = plt.subplots()

def animate(i):
	ax.clear()
			
	for n in range(Nx):
		x0=xP[n]
		y0=Px[n,i]
		
		if y0 > 0:
			plt.xlabel("Position, x")
			plt.ylabel("Probability, P(x)")
			ax.plot(x0, y0, 'or')
		
	ax.set_xlim([-T,T])	
	
	if i < 98:
		ax.set_ylim([0,1])	
	else: 
		ax.set_ylim([0,0.1])


T_f=T-1
ani = FuncAnimation(fig, animate, frames = T_f, interval = 10)
	
writervideo = animation.FFMpegWriter(fps=10)
ani.save('1DPRW_Pxn_test_1.mp4', writer=writervideo)




	
		

print("Fin")
