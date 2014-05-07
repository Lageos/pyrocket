from __future__ import print_function, division
import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint, cumtrapz
from scipy import interpolate

# tested with python 2.7.6 , matplotlib 1.3.1, numpy 1.8.0, scipy 0.13.0
print("### pyrocket ###")


### Parameters ###
t_flight = 40.0 # simulation time
t_burn = 3.6
d = 103.8e-3 # diameter m
cross_section = d**2*np.pi/4.
m_propelant = 0.990 # starting propelant mass
m_start= 9.685 # wet mass (incl motor)
m_upper = 5.513 # mass upper stage
cw = 0.6 # drag coefficent overall
cw_sep = 0.55 # drag upper stage,  early sep optimal < 0.3804255 < late sep optimal
g = 9.81 # m/s^2
## Calculation Parameters
n = 1000 # number of steps for solution 1410.827 m
n_sep = 30 # number of different sep-time steps for solution of optimal sep. time
print("Simulation time:        %0.1f s" % t_flight)
print("Start mass:             %0.2f kg" % m_start)
print("Upper stage mass:       %0.2f kg" % m_upper)
print("Diameter:               %0.3f m" % d)
print("Motor:                  K570")
print("Upper Stage mass:       %0.2f kg" % m_upper)
print("Cw overall:             %0.5f" % cw)
print("Cw upper stage:         %0.5f" % cw_sep)


# Thrust Curve cessaroni K 570 from http://www.thrustcurve.org/
t_thrust =  np.array([ [ -100.00 ,    0.0 ],
    [ 0.00 ,    0.0 ],
    [0.04, 892.67 ],
    [0.50, 797.99 ],
    [1.00, 738.68 ],
    [1.50, 659.37 ],
    [2.00, 585.96 ],
    [2.50, 512.88 ],
    [2.97, 417.16 ],
    [3.20, 224.79 ],
    [3.47, 67.00 ],
    [3.59, 0.00 ],
    [t_flight+1000., 0.0]])
f_thrust = interpolate.interp1d(t_thrust[:,0], t_thrust[:,1],kind='slinear',
bounds_error=True)
fig, ax = plt.subplots(2,1, sharex=True)
ax[0].plot(np.linspace(0.,np.around(t_burn*2),100),
f_thrust(np.linspace(0.,np.around(t_burn*2),100)))
ax[0].grid()
ax[0].fill_between(np.linspace(0.,np.around(t_burn*2),100),0,
f_thrust(np.linspace(0.,np.around(t_burn*2),100)),alpha=0.1)
ax[0].set_ylabel("Thrust N")
ax[0].set_xlabel("Time s")
ax[0].set_title("Rocket Properties")


# Mass
def f_m_sep(t,t_sep):
  """mass dependent on time (interpolation)"""
  f_m_sep = interpolate.interp1d([-100.,0.,t_burn,t_sep-0.0005,t_sep,t_flight+1000.],
  [m_start,m_start,(m_start-m_propelant),(m_start-m_propelant),m_upper,m_upper],
  kind='slinear',bounds_error=True)
  return f_m_sep(t)
f_m = interpolate.interp1d([-100.,0.,t_burn,t_flight+1000.],[(m_start),(m_start),
m_start-m_propelant,m_start-m_propelant],kind='slinear',bounds_error=True)
ax[1].plot(np.linspace(0.,np.around(t_burn*2),100),
f_m(np.linspace(0.,np.around(t_burn*2),100)))
ax[1].fill_between(np.linspace(0.,np.around(t_burn*2),100),0,
f_m(np.linspace(0.,np.around(t_burn*2),100)),alpha=0.1)
ax[1].set_ylim([0,(m_start+m_propelant)*1.2])
ax[1].grid()
ax[1].set_ylabel("Mass kg")
ax[1].set_xlabel("Time s")
fig.tight_layout
with open('rocket_properties.png', 'w') as outfile:
    fig.canvas.print_png(outfile)

# C_w
# parachute calculation possible with new cw-values dependent on deployment time
# (new parameter) and cross section over time function
def f_cw_sep(t,t_sep):
  """drag (cw) dependent on time (interpolation)"""
  f_cw_sep = interpolate.interp1d([-100.,t_sep-0.0005,t_sep,t_flight+1000.],
  [cw,cw,cw_sep,cw_sep],kind='linear',bounds_error=True)
  return f_cw_sep(t)

# Temparture over Altitude
def T_norm(h):
  """temperature in respect to altitude (interpolation of standard atmosphere)"""
  temp =  np.array([[ -100000. ,    15.0 ],
  [ 0. ,    15.0 ],
  [11000., -56.5 ],
  [20000., -56.5 ],
  [32000., -44.5 ],
  [47000., -2.5 ],
  [51000., -2.5 ],
  [71000., -58.5 ],
  [84852., -86.28 ],
  [200000., -86.28 ]])
  f_temp = interpolate.interp1d(temp[:,0], temp[:,1],kind='linear', bounds_error=True)
  T = f_temp(h)
  return  T

# Density over Altitude
def rho_h(h):
  """air density in respect to altitude (interpolation of standard atmosphere)"""
  p_0 = 1013.25e2 #Pa
  p = p_0 *np.exp(-h/7990.)
  R_s = 287.058
  rho = p/(R_s*(T_norm(h)+273.15)) #
  return rho


### Functions ###
def find_nearest(array,value):
  """ find neares value """
  index = (np.abs(array-value)).argmin()
  return index

### Flight Calculation with CHANGING DENSITY ####
## Equation: a = F_ges(t,h)/m(t)-g

## Definitions
def diff(x, t):
  """differential equation without separation"""
  thrust = f_thrust(t)
  mass = f_m(t)  #### f_m
  v = x[0]
  h = x[1]
  rho = rho_h(h)
  return np.array((
                      thrust/mass - g -0.5*rho*cross_section*cw*v**2*np.sign(v)/mass,  # x[1]= x
                     v                                         # x[0] =x'
                   ))

def diff_sep(x, t, t_s):
  """differential equation without separation"""
  thrust = f_thrust(t)
  mass = f_m_sep(t,t_s)  # f_m_sep
  v = x[0]
  h = x[1]
  rho = rho_h(h)
  if t_s< (t_burn+0.001):
    t_s=t_burn+0.001
  cw = f_cw_sep(t,t_s)
  return np.array((
                      thrust/mass - g -0.5*rho*cross_section*cw*v**2*np.sign(v)/mass,  # x[1]= x
                     v                                         # x[0] =x'
                   ))

## Solution
x_0 = np.array([0., 0.])
t = np.linspace(0., t_flight, n)
## solve ode without separation
x = odeint(diff, x_0, t)
# velocity
v = x[:,0]
# altitude
h = x[:,1]
# acceleration
a = f_thrust(t)/f_m(t) - g -0.5*rho_h(h)*cross_section*cw*v**2*np.sign(v)/f_m(t)
# max altitude
h_max = np.nanmax(h)
i_apogee = find_nearest(h,h_max)

## Determine optimal separation time
h_max_sep = 0.
t_sep_range = np.linspace(t_burn+0.001,t[i_apogee+10],40)
h_max_sep_range = np.zeros(40)
for [t_separation,h_max_new_sep] in np.nditer([t_sep_range,h_max_sep_range],
op_flags=[['readwrite'],['readwrite']]):
  x_sep = odeint(diff_sep, x_0, t, (t_separation,))  # solve ode with separation
  h_sep = x_sep[:,1] # get altitude
  h_mns = np.nanmax(h_sep) # determine if new sep time gives a better max. alt.
  h_max_new_sep[...] = np.float_(h_mns)
  if h_mns > h_max_sep:
    h_max_sep = h_mns
    t_h_max_sep = t_separation

## solve ode with separation
x_sep = odeint(diff_sep, x_0, t, (t_h_max_sep,))
# altitude
h_sep = x_sep[:,1]
# velocity
v_sep = x_sep[:,0]
# acceleration
a_sep = (f_thrust(t)/f_m_sep(t,t_h_max_sep) - g -0.5*rho_h(h_sep)*cross_section*
f_cw_sep(t,t_h_max_sep)*v**2*np.sign(v_sep)/f_m_sep(t,t_h_max_sep))
f_v_h = interpolate.interp1d(h[range(np.around(n*0.1).astype(int))],
v[range(np.around(n*0.1).astype(int))],kind='cubic',bounds_error=True)

# max. values
a_max = np.nanmax(a)
v_max = np.nanmax(v)
h_max = np.nanmax(h)

# impact element and apogee element
i_impact = find_nearest(h[30:],0.0)
i_apogee = find_nearest(h,h_max)

f_a_sep= interpolate.interp1d(t,a_sep,kind='linear',bounds_error=True)
f_v_sep= interpolate.interp1d(t,v_sep,kind='linear',bounds_error=True)
f_h_sep= interpolate.interp1d(t,h_sep,kind='linear',bounds_error=True)

# max. values
a_max_sep = np.nanmax(a_sep)
v_max_sep = np.nanmax(v_sep)
h_max_sep = np.nanmax(h_sep)

# print values
print("Max. Acceleration:      %4.3f m/s^2" % a_max)
print("Max. Velocity:          %4.3f m/s" % v_max)
print("Max. Altitude:          %4.3f m" % h_max)
print("Velocity after 4 m:     %4.3f m/s" % f_v_h(4.))
print("Velocity after 7 m:     %4.3f m/s" % f_v_h(7.))
print ("Apogee after:          %4.3f s." % t[i_apogee])
print ("Impact after:          %4.3f s" % t[i_impact])
print (" ")
print("Flight with separation:")
print("Max. Acceleration sep:  %4.3f m/s^2" % a_max_sep)
print("Max. Velocity sep:      %4.3f m/s" % v_max_sep)
print("Max. Altitude sep:      %4.3f m" % h_max_sep)

### Plot
fig, ax = plt.subplots(3,1,sharex=True)
ax[0].plot(t,a,label="Acceleration")
ax[0].plot(t,a_sep,'--r',label="Acceleration sep")
ax[0].plot(t_h_max_sep, f_a_sep(t_h_max_sep),'.',label="Separation")
ax[0].fill_between(t, 0, a,alpha=0.1)
ax[0].grid()
ax[0].legend()
ax[0].set_ylabel("Acceleration m/s^2")
ax[0].set_xlabel("Time s")
ax[0].set_title("Rocket Acceleration max. %0.1f m/s^2" % a_max)
ax[1].plot(t,v,label="Velocity")
ax[1].plot(t,v_sep,'--r',label="Velocity sep")
ax[1].plot(t_h_max_sep, f_v_sep(t_h_max_sep),'.',label="Separation")
ax[1].fill_between(t, 0, v,alpha=0.1)
ax[1].grid()
ax[1].legend()
ax[1].set_ylabel("Velocity m/s")
ax[1].set_xlabel("Time s")
ax[1].set_title("Rocket Velocity max. %0.1f m/s" % v_max)
ax[2].plot(t,h,label="Altitude")
ax[2].plot(t,h_sep,'--r',label="Altitude sep")
ax[2].plot(t_h_max_sep, f_h_sep(t_h_max_sep),'.',label="Separation")
ax[2].set_ylim([0,np.around(h_max*0.0012)*1000])
ax[2].fill_between(t, 0, h,alpha=0.1)
ax[2].grid()
ax[2].legend()
ax[2].set_ylabel("Altitude m")
ax[2].set_xlabel("Time s")
ax[2].set_title("Rocket Altitude max. %0.1f m" % h_max)
fig.tight_layout()
with open('flight.png', 'w') as outfile:
    fig.canvas.print_png(outfile)

### Autotracking ###
# gimbal angle for an tracking device dependent on distance to ramp
d_ramp  = 1000 # distance to ramp
phi_1 = np.degrees(np.arctan(h/d_ramp))
phi_2 = np.degrees(np.arctan(h/2000) )
fig, ax = plt.subplots(1,1)
ax.plot(t,phi_1,label="Distance: 1000 m")
ax.plot(t,phi_2,label="Distance: 2000 m")
ax.grid()
ax.legend()
ax.set_ylim([0,90])
ax.set_ylabel("Angle deg")
ax.set_xlabel("Time s")
ax.set_title("Autotracking")
with open('autotracking.png', 'w') as outfile:
  fig.canvas.print_png(outfile)

### altitude as function over separation time plot ###
fig,ax = plt.subplots(1,1)
ax.plot(t_sep_range,h_max_sep_range,'-+',
label=("c_w=%0.2f c_wsep=%0.2f" %(cw,cw_sep)))
ax.plot(t_h_max_sep,h_max_sep,'.r')
ax.grid()
ax.legend(loc='lower center')
ax.set_ylabel("Altitude reached m")
ax.set_xlabel("Separation Time s")
ax.set_title("Altitude (max.%0.2f m with t_sep=%0.2f s)" % (h_max_sep,t_h_max_sep))
with open('t_sep_altitude.png', 'w') as outfile:
  fig.canvas.print_png(outfile)
