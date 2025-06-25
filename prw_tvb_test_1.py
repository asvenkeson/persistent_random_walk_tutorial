
# persistent random walk tutorial  
########################################################################
# testing basic setup for persistent random walk dynamics on 2D lattice
#
# persistent random walk model based on reference: 
# Optimizing Persistent Random Searches
# PRL 108, 088103 (2012)
# 
#
# notes:
# 2D square lattice 
# infinite lattice ; no boundary conditions
# particle speed fixed to 1 (random walk on integer lattice)
######################################################################## 	

#import
import numpy as np
import math as m



#set constant parameters

N=6 #total number of time steps in random walk trajectory  
print("N =",N)

p1=0.4 #probability to step forward
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
#print("R_f =\n",R_f)

R_b=-R_f # rotation by pi / reverse direction
#print("R_b =\n",R_b)

R_l=np.zeros((2, 2), dtype=float)  # rotation to left by pi/2
R_l[0][1]=-1
R_l[1][0]=1
#print("R_l =\n",R_l)

R_r=np.zeros((2, 2), dtype=float)  # rotation to right by pi/2
R_r=-R_l
#print("R_r =\n",R_r)


#define velocity vectors for 2D lattice

#positive x direction
V_xp=np.zeros(2, dtype=float)   
V_xp[0]=1
V_xp[1]=0
#print("V_xp =\n",V_xp)

#negative x direction
V_xn=-V_xp   
#print("V_xn =\n",V_xn)

#positive y direction
V_yp=np.zeros(2, dtype=float)   
V_yp[0]=0
V_yp[1]=1
#print("V_yp =\n",V_yp)

#negative y direction
V_yn=-V_yp   
#print("V_yn =\n",V_yn)

'''
#test rotation matrix on velocity vector
Y=R_r @ V_yp
print("Y =\n",Y)
'''


#define arrays to hold random walk trajectory information

t_vals=np.linspace(0, N-1, N) #array of time values

r_vals=np.zeros((2, N), dtype=float)  #position trajectory r=(x, y)

v_vals=np.zeros((2, N), dtype=float)  #velocity trajectory v=(v_x, v_y)

#select initial velocity
v_vals[:,0]=V_yn

print("v_vals =\n",v_vals)


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
	print("r_vals =\n",r_vals)
	




#output data to a text file

output=open('prw2D_A.txt','w')

for n in range (N):
	output.write(str(t_vals[n]))
	output.write('    ')
	output.write(str(r_vals[0][n]))
	output.write('    ')
	output.write(str(r_vals[1][n]))		
	output.write('\n')

output.close()




print("Fin")
