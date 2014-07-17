from __future__ import print_function, division
import matplotlib.pylab as plt
import numpy as np
from scipy.integrate import odeint
from scipy import interpolate
import Tkinter as tk

# tested with python 2.7.6 , matplotlib 1.3.1, numpy 1.8.0, scipy 0.13.0
print("### pyrocket ###")



class pyrocket_gui:
    def __init__(self):
        
        self.g=9.81 #m/s^2
        inf = 1e308
        
        def simulation():
            if self.two_stage_sim.get() == 1:
                return()
            else:
                pyrocket_one_stage()
            return()
        
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
        self.sim_steps_var.insert(1,1000)
        self.sim_steps_unit_label = tk.Label(self.leftFrame, text="[1]")
        self.sim_steps_unit_label.grid(row=5, column=3, padx=10, pady=2)
        
        self.motor_k570 = tk.IntVar()
        self.motor_k570_button= tk.Checkbutton(self.leftFrame, text="K570 Motor", variable=self.motor_k570)
        self.motor_k570_button.grid(row=6, column=0, padx=10, pady=2)
        self.motor_k570_button.select()
        
        self.two_stage_sim = tk.IntVar()
        self.button= tk.Checkbutton(self.leftFrame, text="Two Stage Rocket", variable=self.two_stage_sim)
        self.button.grid(row=7, column=0, padx=10, pady=2)
        
        self.commandFrame = tk.Frame(self.main_window, width=200, height = 200)
        self.commandFrame.grid(row=1, column=0, padx=10, pady=2)
        
        self.start_simulation = tk.Button(self.commandFrame, text='Start Simulation', command=simulation, font="Helvetica 12 italic")
        self.start_simulation.grid(row=0, column=0, padx=10, pady=2)

        self.quit_program = tk.Button(self.commandFrame, text=' Quit ', command=self.main_window.quit)
        self.quit_program.grid(row=1, column=0, padx=10, pady=2)
        
        # Motor Data
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
        
        
        def pyrocket_one_stage():
            print("# One Stage Simulation #")
            # Parameters
            motor = k570()
            cross_section =  (float(self.diameter_var.get())/1000)**2*np.pi/4.
            t_flight= float(self.flight_time_var.get())
            m_empty= float(self.mass_start_var.get())
            n = int(self.sim_steps_var.get())
            cw = float(self.cw_total_var.get())
            m_start= m_empty + motor.m_propelant
            f_m = interpolate.interp1d([-100.,0.,motor.t_burn,inf],[(m_start),(m_start),m_start-motor.m_propelant,m_start-motor.m_propelant],kind='slinear',bounds_error=True)
            
            def diff(x, t):
                """differential equation without separation"""
                thrust = motor.f_thrust(t)
                mass = f_m(t)
                v = x[0]
                h = x[1]
                rho = rho_h(h)
                
                # array  x[1]= x,  x[0] =x'
                return np.array(( thrust/mass - self.g -0.5*rho*cross_section*cw*v**2*np.sign(v)/mass, v))
            
            ## Solution
            x_0 = np.array([0., 0.])
            t = np.linspace(0., t_flight, n)
            ## solve ode without separation
            x = odeint(diff, x_0, t)
            print("Simulation Finished")
            # velocity
            v = x[:,0]
            # altitude
            h = x[:,1]
            # acceleration
            a = motor.f_thrust(t)/f_m(t) - self.g -0.5*rho_h(h)*cross_section*cw*v**2*np.sign(v)/f_m(t)
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
            print (" ")


            
        
        # Enter the tkinter main loop.
        tk.mainloop()
    
        




# Create an instance of the GUI class.
pyrocket = pyrocket_gui()

