
# persistent random walk tutorial  
########################################################################
# testing basic setup for persistent random walk dynamics on 2D lattice 
#
# animation of the random walk trajectory ; generating video file
#
# persistent random walk model based on reference: 
# Optimizing Persistent Random Searches
# PRL 108, 088103 (2012)
# 
#
# notes:
# 2D lattice [x_min, x_min+1, ..., x_max-1, x_max] ; (similar for y direction)
# periodic boundary conditions (x_max + 1 = x_min ; x_min - 1 = x_max)   
# particle speed fixed to 1 (random walk on integer lattice)
######################################################################## 	

#import
import numpy as np
import math as m


#set constant parameters

N=25 #total number of time steps in random walk trajectory  
print("N =",N)


x_half=5  
x_min=-x_half #minimum x position on lattice 
x_max=x_half #maximum x position on lattice
Lx=x_max-x_min+1 #number of lattice sites along x direction
x_array=np.linspace(x_min, x_max, Lx)

print("x_min =",x_min)
print("x_max =",x_max)
print("Lx =",Lx)
#print("x_array =\n",x_array)


y_half=x_half #condition for square lattice  
y_min=-y_half #minimum y position on lattice 
y_max=y_half #maximum y position on lattice
Ly=y_max-y_min+1 #number of lattice sites along y direction
y_array=np.linspace(y_min, y_max, Ly)

print("y_min =",y_min)
print("y_max =",y_max)
print("Ly =",Ly)
#print("y_array =\n",y_array)


p1=0.6 #probability to step forward
p2=(1-p1)/3.0  #probability to step backward
p3=p2  #probability to step left (also probability to step right)

p_sum=p1+p2+p3+p3 #normalization check

print("p1 =",p1)
print("p2 =",p2)
print("p3 =",p3)
print("p_sum =",p_sum)

print("p1 =",p1)
print("p1+p2 =",p1+p2)
print("p1+p2+p3 =",p1+p2+p3)


#define rotation matrices that act on velocity vector [v(n+1) = R v(n) where n is the time step]
R_f=np.identity(2)  # no rotation / keep direction

R_b=-R_f # rotation by pi / reverse direction

R_l=np.zeros((2, 2), dtype=float)  # rotation to left by pi/2
R_l[0][1]=-1
R_l[1][0]=1

R_r=np.zeros((2, 2), dtype=float)  # rotation to right by pi/2
R_r=-R_l


#define velocity vectors for 2D lattice

#positive x direction
V_xp=np.zeros(2, dtype=float)   
V_xp[0]=1
V_xp[1]=0

#negative x direction
V_xn=-V_xp   

#positive y direction
V_yp=np.zeros(2, dtype=float)   
V_yp[0]=0
V_yp[1]=1

#negative y direction
V_yn=-V_yp   


#define arrays to hold random walk trajectory information

t_vals=np.linspace(0, N-1, N) #array of time values

r_vals=np.zeros((2, N), dtype=float)  #position trajectory r=(x, y)

v_vals=np.zeros((2, N), dtype=float)  #velocity trajectory v=(v_x, v_y)

#select initial velocity
v_vals[:,0]=V_xp



#time evolution
for n in range(N-1):
	print("n =",n)

	#generate random number to determine velocity direction update
	q=np.random.random()
	print("q =",q)
	
	#get rotation matrix for updating velocity
	if q < p1:  # forward
		R_matrix=R_f
	elif p1 <= q < p1+p2: # backward
		R_matrix=R_b	
	elif p1+p2 <= q < p1+p2+p3: # left
		R_matrix=R_l
	else:  # right
		R_matrix=R_r

	#update velocity
	v_vals[:,n+1]=R_matrix @ v_vals[:,n]
	print("v_vals =\n",v_vals)
	
	#update position
	r_vals[:,n+1]=r_vals[:,n] + v_vals[:,n+1]

#	print("r_vals before applying bc's =\n",r_vals)
	
	#apply periodic boundary conditions
	if r_vals[0,n+1]>x_max:
		r_vals[0,n+1]=x_min
		print("x_max boundary crossed")	
	elif r_vals[0,n+1]<x_min:
		r_vals[0,n+1]=x_max
		print("x_min boundary crossed")
		
	if r_vals[1,n+1]>y_max:
		r_vals[1,n+1]=y_min
		print("y_max boundary crossed")
	elif r_vals[1,n+1]<y_min:
		r_vals[1,n+1]=y_max
		print("y_min boundary crossed")
	
	print("r_vals =\n",r_vals)



#output data to a text file

output=open('prw2D_PBC_3_A.txt','w')

for n in range (N):
	output.write(str(t_vals[n]))
	output.write('    ')
	output.write(str(r_vals[0][n]))
	output.write('    ')
	output.write(str(r_vals[1][n]))		
	output.write('\n')

output.close()



	


#create 2D animation of random walk trajectory
print("animating...")

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

x0 = []
y0 = []

fig, ax = plt.subplots()

def animate(i):
	ax.clear()
			
	x0=r_vals[0][i]
	y0=r_vals[1][i]
		
	ax.plot(x0, y0, 'or')
		
	ax.set_xlim([x_min,x_max])
	ax.set_ylim([y_min,y_max])	


T_f=N
ani = FuncAnimation(fig, animate, frames = T_f, interval = 1000)
	
writervideo = animation.FFMpegWriter(fps=1)
ani.save('2DPRW_Test3_A.mp4', writer=writervideo)




print("Fin")
