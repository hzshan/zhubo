import matplotlib.pyplot as plt#载入需要的python包
import numpy as np
# Basic simulation Properties
dt     = 10E-6;     # 10 us timestep #用10微秒作为模拟实验的空间分辨率
# Basic Cell Properties
Cm     = 100E-12;   # Membrane Capacitance = 100 pF #规定细胞膜电容为100 pF
v_init = -90E-3;    # Initial membrane potential -90 mV #规定t=0时的细胞膜两侧电压差为-90mV
Gk     = 5E-9       # 5 nS conductance #规定静息状态下的漏电导为5nS
Ek     = -90E-3     # Reversal potential of -90 mV #规定静息状态下开放通道的平衡电位为-90mV
 
# Injected Current step
current_magnitude = 100E-12; # 100 pA #向细胞注射100pA的电流
 
#Injected current, 0.2 seconds of 0 current, 0.3 seconds of some current,
#and 0.5 seconds of no current
i_inj = np.concatenate( (np.zeros([round(0.2/dt),1]),
                         current_magnitude*np.ones([round(0.3/dt), 1]),
                         np.zeros([round(0.5/dt), 1])) )#向细胞注射0.3秒的电流
 
#Preallocate the voltage output
v_out = np.zeros(np.size(i_inj)) #预留出电压的向量
 
#The real computational meat
for t in range(np.size(v_out)):
    if t == 0:
        v_out[t] = v_init; #At the first time step, set voltage to the initial condition
    else:
        i_ion = Gk * (v_out[t-1] - Ek)  #Calculate the current through ion channels 计算每小短时间内通过漏通道的电流
        i_cap = i_inj[t] - i_ion;       #Calculate what i is 总电流是漏电流和注射电流的和
        dv = i_cap/Cm * dt;     #Calculate dv, using our favourite equation 总电流给电容充电
        v_out[t] = v_out[t-1] + dv;     #add dv on to our last known voltage 更新电容器两边的电压
v_out = v_out*1E3

#Make the graph
t_vec = np.linspace(0, 1, np.size(v_out))
plt.plot(t_vec, v_out)
plt.xlabel('Time (s)')
plt.ylabel('Membrane Potential (V)')
plt.show()
