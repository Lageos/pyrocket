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
        
        
        def simulation():
            print(self.two_stage_sim)
            if self.two_stage_sim == 1:
                print("Two stage simulation.")
            else:
                print("One stage simulation.")
            return()
        
        # Create the main window widget.
        self.main_window = tk.Tk()
        self.main_window.wm_title("PyRocket")
        self.main_window.config(background = "#BDBDBD")
        
        self.leftFrame = tk.Frame(self.main_window, width=200, height = 600)
        self.leftFrame.grid(row=0, column=0, padx=10, pady=2)
        
        
        # Create a Label widget containing the
        self.Parameter_Label = tk.Label(self.leftFrame, text='PyRocket Parameters')
        self.Parameter_Label.grid(row=0, column=0, padx=10, pady=2)
        
        self.Instruct = tk.Label(self.leftFrame, text="1\n2\n2\n3\n4\n5\n6\n7\n8\n9\n")
        self.Instruct.grid(row=1, column=0, padx=10, pady=2)
        
        self.two_stage_sim = tk.IntVar()
        self.button= tk.Checkbutton(self.leftFrame, text="Two Stage Rocket", variable=self.two_stage_sim)
        self.button.grid(row=3, column=0, padx=10, pady=2)
        
        self.commandFrame = tk.Frame(self.main_window, width=200, height = 200)
        self.commandFrame.grid(row=1, column=0, padx=10, pady=2)
        
        self.start_simulation = tk.Button(self.commandFrame, text='Start Simulation', command=simulation)
        self.start_simulation.grid(row=0, column=0, padx=10, pady=2)

        self.quit_program = tk.Button(self.commandFrame, text='Quit', command=self.main_window.quit)
        self.quit_program.grid(row=1, column=0, padx=10, pady=2)
        
        # Enter the tkinter main loop.
        tk.mainloop()



# Create an instance of the MyGUI class.
pyr_gui = pyrocket_gui()

