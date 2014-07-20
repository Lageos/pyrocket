from __future__ import print_function, division
import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint
from scipy import interpolate
import Tkinter as tk

# tested with python 2.7.6 , matplotlib 1.3.1, numpy 1.8.0, scipy 0.13.0
# Michael Russwurm 2014
print("### pyrocket ###")

class pyrocket_gui:
    def __init__(self):
        
        self.g=9.81 #m/s^2
        inf = 1e308
        
        class k570:
            def __init__(self):
                self.m_propelant = 0.990
                self.t_thrust =  np.array([ [ -100.00 ,    0.0 ],
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
                [inf, 0.0]])
                self.f_thrust = interpolate.interp1d(self.t_thrust[:,0], self.t_thrust[:,1],kind='slinear',bounds_error=True)
                self.t_burn = 3.6
        
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
            [200000., -86.28 ],
            [inf, -86.28]])
            f_temp = interpolate.interp1d(temp[:,0], temp[:,1],kind='slinear', bounds_error=True)
            T = f_temp(h)
            return  T
            
        def rho_h(h):
            """air density in respect to altitude (interpolation of standard atmosphere)"""
            p_0 = 1013.25e2 #Pa
            p = p_0 *np.exp(-h/7990.)
            R_s = 287.058
            rho = p/(R_s*(T_norm(h)+273.15)) #
            return rho
            
        def find_nearest(array,value):
            """ find nearest value """
            index = (np.abs(array-value)).argmin()
            return index
        
        
        def simulation():
            print("## Simulation Start ##")
            # Parameters
            if self.motor_k570.get() == 1:
                motor = k570()
            cross_section =  (float(self.diameter_var.get())/1000)**2*np.pi/4.
            t_flight= float(self.flight_time_var.get())
            m_empty= float(self.mass_start_var.get())
            n = int(self.sim_steps_var.get())
            if self.parachute_sim.get() ==1: 
                cw_rocket = float(self.cw_total_var.get())
                cw_para = float(self.cw_parachute_var.get())
                t_deploy = float(self.t_deploy_parachute_var.get())
                para_cross_section = float(self.parachute_area_var.get())
                cw_t= interpolate.interp1d([-100.,inf],[(cw_rocket),(cw_rocket)],kind='linear',bounds_error=True)
                # deployment duration 0.5 s
                cw_para_t= interpolate.interp1d([-100., t_deploy-0.1, t_deploy+0.4 ,inf],[(0.0),0.0,cw_para,cw_para],kind='linear',bounds_error=True)
            else:
                para_cross_section = 0.
                cw_rocket = float(self.cw_total_var.get())
                cw_t= interpolate.interp1d([-100.,inf],[(cw_rocket),(cw_rocket)],kind='linear',bounds_error=True)
                cw_para_t= interpolate.interp1d([-100.,inf],[(0.),(0.)],kind='linear',bounds_error=True)
            m_start= m_empty + motor.m_propelant
            f_m = interpolate.interp1d([-100.,0.,motor.t_burn,inf],[(m_start),(m_start),m_start-motor.m_propelant,m_start-motor.m_propelant],kind='slinear',bounds_error=True)
            print("Simulation time:        %0.1f s" % t_flight)
            print("Steps:                  %0.2d" % n)
            print("Start mass:             %0.2f kg" % m_start)
            print("Diameter:               %0.3f m" % (float(self.diameter_var.get())/1000))
            print("Cw:                     %0.5f" % cw_rocket)
            
            def diff(x, t):
                """differential equation without separation"""
                thrust = motor.f_thrust(t)
                mass = f_m(t)
                cw = cw_t(t)
                cw_para = cw_para_t(t)                
                v = x[0]
                h = x[1]
                rho = rho_h(h)
                
                # array  x[1]= x,  x[0] =x'
                return np.array(( thrust/mass - self.g -0.5*rho*(cross_section*cw+cw_para*para_cross_section)*v**2*np.sign(v)/mass, v))
            
            ## Solution
            x_0 = np.array([0., 0.])
            t = np.linspace(0., t_flight, n)
            ## solve ode without separation
            x = odeint(diff, x_0, t)
            print("# Simulation Finished #")
            # velocity
            v = x[:,0]
            # altitude
            h = x[:,1]
            # acceleration
            a = motor.f_thrust(t)/f_m(t) - self.g -0.5*rho_h(h)*cross_section*cw_t(t)*v**2*np.sign(v)/f_m(t)
            # max. values
            a_max = np.nanmax(a)
            v_max = np.nanmax(v)
            h_max = np.nanmax(h)
            i_apogee = find_nearest(h,h_max)
            # impact element and apogee element
            i_impact = find_nearest(h[30:],0.0)
            i_apogee = find_nearest(h,h_max)
            # print values
            print("Results:")
            print("Max. Acceleration:      %4.3f m/s^2" % a_max)
            print("Max. Velocity:          %4.3f m/s" % v_max)
            print("Max. Altitude:          %4.3f m" % h_max)
            #print("Velocity after 4 m:     %4.3f m/s" % f_v_h(4.))
            #print("Velocity after 7 m:     %4.3f m/s" % f_v_h(7.))
            print ("Apogee after:          %4.3f s" % t[i_apogee])
            print ("Impact after:          %4.3f s" % t[i_impact])
              

            fig, ax = plt.subplots(3,1,sharex=True)
            ax[0].plot(t,a,label="Acceleration")
            ax[0].fill_between(t, 0, a,alpha=0.1)
            ax[0].grid()
            ax[0].legend()
            ax[0].set_ylabel("Acceleration m/s^2")
            ax[0].set_xlabel("Time s")
            ax[0].set_title("Rocket Acceleration max. %0.2f m/s^2" % a_max)
            ax[1].plot(t,v,label="Velocity")
            ax[1].fill_between(t, 0, v,alpha=0.1)
            ax[1].grid()
            ax[1].legend()
            ax[1].set_ylabel("Velocity m/s")
            ax[1].set_xlabel("Time s")
            ax[1].set_title("Rocket Velocity max. %0.2f m/s" % v_max)
            ax[2].plot(t,h,label="Altitude")
            ax[2].set_ylim([0,np.around(h_max*0.001251)*1000])
            ax[2].fill_between(t, 0, h,alpha=0.1)
            ax[2].grid()
            ax[2].legend()
            ax[2].set_ylabel("Altitude m")
            ax[2].set_xlabel("Time s")
            ax[2].set_title("Rocket Altitude max. %0.2f m" % h_max)
            fig.tight_layout()
            #with open('flight.png', 'w') as outfile:
            #    fig.canvas.print_png(outfile) 
            
            if self.autotracking_select_var.get() ==1:                
                d_ramp  = float(self.autotracking_var.get()) # distance to ramp
                phi_1 = np.degrees(np.arctan(h/d_ramp))
                phi_point = np.degrees(np.arctan(v/d_ramp))
                phi_point_max = np.nanmax(phi_point)
                fig, ax = plt.subplots(1,1)
                ax.plot(t,phi_1,label="Distance: %3.d m" % d_ramp)
                ax.grid()
                ax.legend()
                ax.set_ylim([0,90])
                ax.set_ylabel("Angle deg")
                ax.set_xlabel("Time s")
                ax.set_title("Autotracking")
                print("Max. Vel. Autotr.:     %4.3f deg/s" % phi_point_max)
                print("Max. Vel. Autotr.:     %4.3f rpm" % (phi_point_max/6))
            print (" ")      
            plt.show()
        
        # Create the main window widget.
        self.main_window = tk.Tk()
        self.main_window.wm_title("PyRocket")
        self.main_window.config(background = "#BDBDBD")
        
        self.leftFrame = tk.Frame(self.main_window, width=200, height = 600)
        self.leftFrame.grid(row=0, column=0, padx=10, pady=2)
        
        
        # Create a Label widget containing the
        self.Parameter_Label = tk.Label(self.leftFrame, text='PyRocket', font="Helvetica 12 italic")
        self.Parameter_Label.grid(row=0, column=0, padx=10, pady=2)

        
        self.flight_time_label = tk.Label(self.leftFrame, text="Flight Time")
        self.flight_time_label.grid(row=1, column=0, padx=10, pady=2)
        self.flight_time_var = tk.Entry(self.leftFrame)
        self.flight_time_var.grid(row=1, column=2)
        self.flight_time_var.insert(1,100)
        self.flight_time_unit_label = tk.Label(self.leftFrame, text="[s]")
        self.flight_time_unit_label.grid(row=1, column=3, padx=10, pady=2)
        
        self.diameter_label = tk.Label(self.leftFrame, text="Main Diameter")
        self.diameter_label.grid(row=2, column=0, padx=10, pady=2)
        self.diameter_var = tk.Entry(self.leftFrame)
        self.diameter_var.grid(row=2, column=2)
        self.diameter_var.insert(1,100)
        self.diameter_unit_label = tk.Label(self.leftFrame, text="[mm]")
        self.diameter_unit_label.grid(row=2, column=3, padx=10, pady=2)
        
        self.mass_start_label = tk.Label(self.leftFrame, text="Mass Start (excl. Propelant Mass)")
        self.mass_start_label.grid(row=3, column=0, padx=10, pady=2)
        self.mass_start_var = tk.Entry(self.leftFrame)
        self.mass_start_var.grid(row=3, column=2)
        self.mass_start_var.insert(1,10)
        self.mass_start_unit_label = tk.Label(self.leftFrame, text="[kg]")
        self.mass_start_unit_label.grid(row=3, column=3, padx=10, pady=2)

        self.cw_total_label = tk.Label(self.leftFrame, text="Cw (total rocket)")
        self.cw_total_label.grid(row=4, column=0, padx=10, pady=2)
        self.cw_total_var = tk.Entry(self.leftFrame)
        self.cw_total_var.grid(row=4, column=2)
        self.cw_total_var.insert(1,0.6)
        self.cw_total_unit_label = tk.Label(self.leftFrame, text="[1]")
        self.cw_total_unit_label.grid(row=4, column=3, padx=10, pady=2)
        
        self.sim_steps_label = tk.Label(self.leftFrame, text="Simulation Steps")
        self.sim_steps_label.grid(row=5, column=0, padx=10, pady=2)
        self.sim_steps_var = tk.Entry(self.leftFrame)
        self.sim_steps_var.grid(row=5, column=2)
        self.sim_steps_var.insert(1,10000)
        self.sim_steps_unit_label = tk.Label(self.leftFrame, text="[1]")
        self.sim_steps_unit_label.grid(row=5, column=3, padx=10, pady=2)
        
        self.motor_k570 = tk.IntVar()
        self.motor_k570_button= tk.Checkbutton(self.leftFrame, text="K570 Motor", variable=self.motor_k570)
        self.motor_k570_button.grid(row=6, column=0, padx=10, pady=2)
        self.motor_k570_button.select()
        
        self.parachute_sim = tk.IntVar()
        self.parachute_button= tk.Checkbutton(self.leftFrame, text="Parachute Simulation", variable=self.parachute_sim)
        self.parachute_button.grid(row=7, column=0, padx=10, pady=2)
        
        self.parachute_area_label = tk.Label(self.leftFrame, text="Parachute Area (projected)")
        self.parachute_area_label.grid(row=8, column=0, padx=10, pady=2)
        self.parachute_area_var = tk.Entry(self.leftFrame)
        self.parachute_area_var.grid(row=8, column=2)
        self.parachute_area_var.insert(1,5)
        self.parachute_area_unit_label = tk.Label(self.leftFrame, text="[m^2]")
        self.parachute_area_unit_label.grid(row=8, column=3, padx=10, pady=2)
        
        self.cw_parachute_label = tk.Label(self.leftFrame, text="Cw Parachute")
        self.cw_parachute_label.grid(row=9, column=0, padx=10, pady=2)
        self.cw_parachute_var = tk.Entry(self.leftFrame)
        self.cw_parachute_var.grid(row=9, column=2)
        self.cw_parachute_var.insert(1,0.8)
        self.cw_parachute_unit_label = tk.Label(self.leftFrame, text="[1]")
        self.cw_parachute_unit_label.grid(row=9, column=3, padx=10, pady=2)
        
        self.t_deploy_parachute_label = tk.Label(self.leftFrame, text="Parachute Deployment Time")
        self.t_deploy_parachute_label.grid(row=10, column=0, padx=10, pady=2)
        self.t_deploy_parachute_var = tk.Entry(self.leftFrame)
        self.t_deploy_parachute_var.grid(row=10, column=2)
        self.t_deploy_parachute_var.insert(1,20)
        self.t_deploy_parachute_unit_label = tk.Label(self.leftFrame, text="[s]")
        self.t_deploy_parachute_unit_label.grid(row=10, column=3, padx=10, pady=2)
                
        
        self.two_stage_sim = tk.IntVar()
        self.button= tk.Checkbutton(self.leftFrame, text="Two Stage Rocket", variable=self.two_stage_sim)
        self.button.grid(row=11, column=0, padx=10, pady=2)
        
        self.mass_upper_label = tk.Label(self.leftFrame, text="Mass Upper Stage (excl. Propelant Mass)")
        self.mass_upper_label.grid(row=12, column=0, padx=10, pady=2)
        self.mass_upper_var = tk.Entry(self.leftFrame)
        self.mass_upper_var.grid(row=12, column=2)
        self.mass_upper_var.insert(1,5)
        self.mass_upper_unit_label = tk.Label(self.leftFrame, text="[kg]")
        self.mass_upper_unit_label.grid(row=12, column=3, padx=10, pady=2)
        
        self.cw_upper_label = tk.Label(self.leftFrame, text="Cw (upper stage)")
        self.cw_upper_label.grid(row=13, column=0, padx=10, pady=2)
        self.cw_upper_var = tk.Entry(self.leftFrame)
        self.cw_upper_var.grid(row=13, column=2)
        self.cw_upper_var.insert(1,0.55)
        self.cw_upper_unit_label = tk.Label(self.leftFrame, text="[1]")
        self.cw_upper_unit_label.grid(row=13, column=3, padx=10, pady=2)
        
        self.motor_upper_k570 = tk.IntVar()
        self.motor_upper_k570_button= tk.Checkbutton(self.leftFrame, text="K570 Motor", variable=self.motor_upper_k570)
        self.motor_upper_k570_button.grid(row=14, column=0, padx=10, pady=2)
        self.motor_upper_k570_button.select()
        
        self.autotracking_select_var = tk.IntVar()
        self.autotracking_button= tk.Checkbutton(self.leftFrame, text="Autotracking Simulation", variable=self.autotracking_select_var)
        self.autotracking_button.grid(row=15, column=0, padx=10, pady=2)
        
        self.autotracking_label = tk.Label(self.leftFrame, text="Autotracking Distance")
        self.autotracking_label.grid(row=16, column=0, padx=10, pady=2)
        self.autotracking_var = tk.Entry(self.leftFrame)
        self.autotracking_var.grid(row=16, column=2)
        self.autotracking_var.insert(1,1000)
        self.autotracking_label = tk.Label(self.leftFrame, text="[m]")
        self.autotracking_label.grid(row=16, column=3, padx=10, pady=2)
        
        self.commandFrame = tk.Frame(self.main_window, width=200, height = 200)
        self.commandFrame.grid(row=1, column=0, padx=10, pady=2)
        
        self.start_simulation = tk.Button(self.commandFrame, text='Start Simulation', command=simulation, font="Helvetica 12 italic")
        self.start_simulation.grid(row=0, column=0, padx=10, pady=2)

        self.quit_program = tk.Button(self.commandFrame, text=' Quit ', command=self.main_window.quit)
        self.quit_program.grid(row=1, column=0, padx=10, pady=2)
        
        # Enter the tkinter main loop.
        tk.mainloop()

# Create an instance of the GUI class.
pyrocket = pyrocket_gui()

