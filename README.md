pyrocket
========

Small Amateur 1D Rocket Simulation Program

To run a simulation just execute `python pyrocket_gui.py` and change the parameters.

## What is Implemented

* Standard Atmosphere
  * Changing Temperature over Altitude
  * Changing Density over Altitude
* Thrust Curve through Interpolation
  * Custom Thrust Curves can be Implemented (through motor classes)
* Time Dependent Drag (only main chute in GUI)
  * Usable for: Parachutes, Separation, ...
* Time Dependent Mass (not in GUI)
* Max. Altitude Calculation
* Altitude, Velocity, Acceleration Calculation
* Ideal Separation Time Optimization (not in GUI)
* Automatic Plots
* Following Camera Angle over Time
  * Dependent on distance to launchpad
* Main-Parachute in GUI

##Output

See images in repository

## Future Plans

* Three Dimensional Flight
  * Vertical drift due to side wind
  * Launch ramp skew
  * Statistical considerations
* Google Earth / Maps Integration
  * Start Coordinates
  * Touch Down region
    * Ballistic Flight
    * Successfull Parachute Flight
* 2 stage in GUI
* Drogue

## Contact
Twitter: @soegal
