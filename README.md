pyrocket
========

Small Amateur 1D Rocket Simulation Script

## What is Implemented

* Standard Atmosphere
  * Changing Temperature over Altitude
  * Changing Density over Altitude
* Thrust Curve through Interpolation
  * Custom Thrust Curves can be Implemented
* Time Dependent Drag (not in GUI)
  * Usable for: Parachutes, Separation, ...
* Time Dependent Mass (not in GUI)
* Max. Altitude Calculation
* Altitude, Velocity, Acceleration Calculation
* Ideal Separation Time Optimization (not in GUI)
* Automatic Plots
* Following Camera Angle over Time (not in GUI)
  * Dependent on distance to launchpad

##Output

### Flight

![flight](https://raw.githubusercontent.com/Lageos/pyrocket/master/flight.png)

### Rocket Properties over Time

![properties](https://raw.githubusercontent.com/Lageos/pyrocket/master/rocket_properties.png)

### Optimal Separation Time Optimization

![optim_t_sep](https://raw.githubusercontent.com/Lageos/pyrocket/master/t_sep_altitude.png)

### Autotracking Angle

![autotracking_angle](https://raw.githubusercontent.com/Lageos/pyrocket/master/autotracking.png)

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
* Parachute in GUI

## Contact
Twitter: @soegal
