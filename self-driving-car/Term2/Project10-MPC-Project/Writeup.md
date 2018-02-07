# Project - CarND-MPC Project Writeup

---

## Implementation

### The Model

The model used is a Kinematic model neglecting the complex interactions between the tires and the road. The model equations are as follow:

```c++
x[t] = x[t-1] + v[t-1] * cos(psi[t-1]) * dt
y[t] = y[t-1] + v[t-1] * sin(psi[t-1]) * dt
psi[t] = psi[t-1] + v[t-1] / Lf * delta[t-1] * dt
v[t] = v[t-1] + a[t-1] * dt
cte[t] = f(x[t-1]) - y[t-1] + v[t-1] * sin(epsi[t-1]) * dt
epsi[t] = psi[t] - psides[t-1] + v[t-1] * delta[t-1] / Lf * dt
```

Where:

- x, y : Car's position.
- psi : Car's heading direction.
- v : Car's velocity.
- cte : Cross-track error.
- epsi : Orientation error.

Those values are considered the state of the model. Lf is the distance between the car of mass and the front wheels. The other two values are the model output:

- a : Car's acceleration (throttle).
- delta : Steering angle.

The objective is to find the acceleration (a) and the steering angle(delta) in the way it will minimize an objective function that is the combination of different factors:

- Square sum of cte and epsi.
- Square sum of the difference actuators to penalize a lot of actuator's actions.
- Square sum of the difference between two consecutive actuator values to penalize sharp changes.

### The weights of each of factors have been tuned manually to obtain a successful track ride without leaving the road.

After lots of trials, I found the following weights could be successful with maximum (upto 90 mph) speed. I also found the WEIGHT_EPSI is the key paramater in order for the car not to leaving the road

```c++
const double WEIGHT_CTE = 10;
// This is a parameter not to be outside of the lane
const double WEIGHT_EPSI = 4000;
const double WEIGHT_DELTA = 5;
const double WEIGHT_A = 5;
const double WEIGHT_DIFF_DELTA = 25000;
const double WEIGHT_DIFF_A = 1;
```

### Timestep Length and Elapsed Duration (N & dt)

The number of points(N) and the time interval(dt) define the prediction horizon. The number of points impacts the controller performance as well. I tried to keep the horizon around the same time the waypoints were on the simulator. With too many points the controller starts to run slower, and some times it went wild very easily. After trying with N from 10 to 20 and dt 100 to 500 milliseconds, I decided to leave them fixed to 10 and 100 milliseconds to have a better result tuning the other parameters.

### Polynomial Fitting and MPC Preprocessing

The waypoints provided by the simulator are transformed to the car coordinate system at ./src/main.cpp. Then a 3rd-degree polynomial is fitted to the transformed waypoints. These polynomial coefficients are used to calculate the cte and epsi later on. They are used by the solver as well to create a reference trajectory.

### Model Predictive Control with Latency

To handle actuator latency, the state values are calculated using the model and the delay interval. These values are used instead of the initial one. The code implementing that could be found at ./src/main.cpp.

## Simulation

### The vehicle must successfully drive a lap around the track.

A snapshot of the simulator is:

<img src="SnapShot.png">
