---
title: Setting up f1tenth_gym_ros with 4 cars
short_title: Multi-Car Simulation
layout: page
section: race
---

IROS 2026 races four cars on the track at the same time, so it is worth practising against more
than one opponent well before you travel. Multi-car support is on the
[`dev-humble` branch of f1tenth_gym_ros](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-humble).

<video src="images/Roboracer/four_car_sim.mp4" poster="images/Roboracer/four_car_sim.jpg"
	autoplay muted loop playsinline controls preload="metadata"
	style="width: 100%; max-width: 900px; height: auto; display: block; margin: 1em auto 2em;">
	Your browser does not support embedded video.
	<a href="images/Roboracer/four_car_sim.mp4">Download the clip</a> instead.
</video>

# Number of cars

Set the number of cars with `num_agent`, either in `config/sim.yaml` or directly at launch:

```
ros2 launch f1tenth_gym_ros gym_bridge_launch.py num_agent:=4
```

# Driving the opponents

The first car is the ego, the rest are opponents. Each opponent gets its own topics
(`/opp_drive`, `/opp_drive2`, ...), and **a car only moves when you publish to its drive topic** —
an opponent you never command will simply sit on the grid.

# Start poses

Every car needs a start pose in the config (`sx1`/`sy1`/`stheta1`, ...). The shipped `sim.yaml`
already defines four, so `num_agent:=4` works out of the box. Define more poses to run more cars.

# Full documentation

Full instructions are in the
[repository README](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-humble#readme).
