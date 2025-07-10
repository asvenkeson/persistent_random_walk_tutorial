
# persistent random walk tutorial  
########################################################################
# run the persistent random walk on a finite 1D lattice 
# 
# periodic boundary conditions 
#
# save position probability distribution data to a text file 
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

alpha=0.8 #persistence level

print("T =",T)
print("N =",N)
print("alpha =",alpha)


#initialize lattice 
x_half=20  
x_min=-x_half #minimum x position on lattice 
x_max=x_half #maximum x position on lattice
Lx=x_max-x_min+1 #number of lattice sites along x direction
x_array=np.linspace(x_min, x_max, Lx)

print("x_min =",x_min)
print("x_max =",x_max)
print("Lx =",Lx)
#print("x_array =\n",x_array)


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

Px=np.zeros((Lx, T),dtype=float)  #empirical probability distribution 


#time evolution	
for t in range (T-1):

	print("t =",t)
		
#	print("v_vals =\n",v_vals)
#	print("x_vals =\n",x_vals)
	
	#update probability distribution
	for n in range(N):
		ix = int(x_vals[n,t]+x_half)
		Px[ix,t]=Px[ix,t]+1.0/N
		
#	print("Px[:,t] =\n",Px[:,t])
					
	#update position
	for n in range(N):			
		x_vals[n,t+1]=x_vals[n,t]+v_vals[n,0]

		#check boundary condition	
		if x_vals[n,t+1]>x_half:
			x_vals[n,t+1]=-x_half
		elif x_vals[n,t+1]<-x_half:
			x_vals[n,t+1]=x_half
		
			
	#update velocity	
	p=np.random.rand(N,1)
#	print("p =\n",p)
		
	for n in range (N):
		if p[n] > alpha:
			v_vals[n] = -1.0*v_vals[n,0]
	

#update probability distribution for final time step 
for n in range(N):
	ix = int(x_vals[n,T-1]+x_half)
	Px[ix,T-1]=Px[ix,T-1]+1.0/N

#print("Px[:,t] =\n",Px[:,t])
		

#print("x_vals =\n",x_vals)




'''

#save probability distribution data to a text file
output=open('prw_1D_pbc_pxn_A.txt','w')

for t in range(T):
	output.write(str(t))
	output.write('    ')
	output.write('    ')
	for n in range(Lx):
		output.write(str(Px[n,t]))
		output.write('    ')
	output.write('\n')

output.close()

'''




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
			
	for n in range(Lx):
		x0=x_array[n]
		y0=Px[n,i]
		
		if y0 > 0:
			plt.xlabel("Position, x")
			plt.ylabel("Probability, P(x)")
			ax.plot(x0, y0, 'or')
		
	ax.set_xlim([-x_half,x_half])	
	
	if i < 98:
		ax.set_ylim([0,1])	
	else: 
		ax.set_ylim([0,0.1])


T_f=T-1
ani = FuncAnimation(fig, animate, frames = T_f, interval = 10)
	
writervideo = animation.FFMpegWriter(fps=10)
ani.save('1DPRW_Pxn_test_2.mp4', writer=writervideo)




	
		

print("Fin")
