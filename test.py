from controller import Controller
from quad_model import Model
from traj_planner import Traj_Planner
import numpy as np
import matplotlib.pyplot as plt

def conf_u(u):
        for i in range(3):
            u[i]=(u[i]-5)/10

        return u

controller=Controller()
quad=Model()
traj=Traj_Planner()


p0=[2,1,4,0]
v0=[1,2,1,0]
pf=[5,-5,0,0]
vf=[5,5,0,0]
T=5
dt=.01
N=int(T/dt)
t=np.linspace(0,T,N)
traj.find_traj(x_initial=p0,x_final=pf,v_initial=v0,v_final=vf,T=T)

traj.save_data()
traj.find_traj(x_initial=p0,x_final=pf,v_initial=v0,v_final=vf,T=T)

traj.save_data()
traj.data_to_picle()

state_list=np.zeros((N,12))
state_list[0,:]=[p0[0],p0[1],p0[2],v0[0],v0[1],v0[2],0,0,p0[3],0,0,v0[3]]
traj_list=np.zeros((N,8))
traj_list[0,:]=[p0[0],p0[1],p0[2],p0[3],v0[0],v0[1],v0[2],v0[3]]

quad.reset(state_list[0,:])

for i in range(1,N):
    vel_ref=traj.get_vel(t[i])
    pose_ref=traj.get_target(t[i])

    target=[vel_ref[0]*np.cos(pose_ref[3])+vel_ref[1]*np.sin(pose_ref[3]),-vel_ref[0]*np.sin(pose_ref[3])+vel_ref[1]*np.cos(pose_ref[3]),vel_ref[2],pose_ref[3]]
    traj_all=[pose_ref[0],pose_ref[1],pose_ref[2],pose_ref[3],vel_ref[0]*np.cos(pose_ref[3])+vel_ref[1]*np.sin(pose_ref[3]),-vel_ref[0]*np.sin(pose_ref[3])+vel_ref[1]*np.cos(pose_ref[3]),vel_ref[2],vel_ref[3]]
    traj_list[i,:]=traj_all
    states=quad.x
    u=controller.run_controller(x=states[3:12],x_t=target)
    x=quad.run_model(u=conf_u(u))
    state_list[i,:]=x


figure, axis = plt.subplots(2, 2)

axis[0, 0].plot(t,traj_list[:,0],t,state_list[:,0])
axis[0, 0].legend(['traj','real'])
axis[0, 0].set_title("X")

axis[0, 1].plot(t,traj_list[:,1],t,state_list[:,1])
axis[0, 1].legend(['traj','real'])
axis[0, 1].set_title("Y")

axis[1, 0].plot(t,traj_list[:,2],t,state_list[:,2])
axis[1, 0].legend(['traj','real'])
axis[1, 0].set_title("Z")

axis[1, 1].plot(t,traj_list[:,3],t,state_list[:,8])
axis[1, 1].legend(['traj','real'])
axis[1, 1].set_title("Psi")


plt.show()

figure, axis = plt.subplots(2, 2)

axis[0, 0].plot(t,traj_list[:,4],t,state_list[:,3])
axis[0, 0].legend(['traj','real'])
axis[0, 0].set_title("Vx")

axis[0, 1].plot(t,traj_list[:,5],t,state_list[:,4])
axis[0, 1].legend(['traj','real'])
axis[0, 1].set_title("Vy")

axis[1, 0].plot(t,traj_list[:,6],t,state_list[:,5])
axis[1, 0].legend(['traj','real'])
axis[1, 0].set_title("Vz")

axis[1, 1].plot(t,traj_list[:,7],t,state_list[:,11])
axis[1, 1].set_title("r")
axis[1, 1].legend(['traj','real'])


plt.show()




