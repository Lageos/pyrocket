pyrocket
========

Small Amateur 1D Rocket Simulation Script

# What is Implemented

* Standard Atmosphere
  * Changing Temperature over Altitude
  * Changing Density over Altitude
* Thrust Curve through Interpolation
  * Custom Thrust Curves can be Implemented
* Time Dependent Drag
  * Usable for: Parachutes, Separation, ...
* Time Dependent Mass
* Max. Altitude Calculation
* Altitude, Velocity, Acceleration Calculation
* Ideal Separation Time Optimization
* Automatic Plots
* Following Camera Angle over Time
  * Dependent on distance to launchpad

# Output

## Flight

![flight](https://raw.githubusercontent.com/Lageos/pyrocket/master/flight.png)

## Rocket Properties over Time

![properties](https://raw.githubusercontent.com/Lageos/pyrocket/master/rocket_properties.png)

## Optimal Separation Time Optimization

![optim_t_sep](https://raw.githubusercontent.com/Lageos/pyrocket/master/t_sep_altitude.png)

## Autotracking Angle

![autotracking_angle](https://raw.githubusercontent.com/Lageos/pyrocket/master/autotracking.png)
