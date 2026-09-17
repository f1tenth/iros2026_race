---
title: Setting up f1tenth_gym_ros with 4 cars
short_title: Multi-Car Simulation
layout: page
section: race
---

IROS 2026 races up to four cars on the track at the same time, so it is worth practising against
more than one opponent well before you travel. The simulator has moved to ROS 2 Jazzy: multi-car
support is on the [`dev-jazzy` branch of f1tenth_gym_ros](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-jazzy),
which runs the [`dev-jax` branch of f1tenth_gym](https://github.com/f1tenth/f1tenth_gym/tree/dev-jax),
the JAX rewrite of the gym. Still on Ubuntu 22.04 / ROS 2 Humble? Use the `dev-humble` branches
of both repositories instead; everything below applies, except that the launch argument there is
still spelled `num_agent`.

<video src="images/Roboracer/four_car_sim.mp4" poster="images/Roboracer/four_car_sim.jpg"
	autoplay muted loop playsinline controls preload="metadata"
	style="width: 100%; max-width: 900px; height: auto; display: block; margin: 1em auto 2em;">
	Your browser does not support embedded video.
	<a href="images/Roboracer/four_car_sim.mp4">Download the clip</a> instead.
</video>

# Installing

The bridge needs Ubuntu 24.04 with ROS 2 Jazzy (natively, recommended) or Docker with
[Foxglove](https://app.foxglove.dev) in your browser. The gym lives inside the bridge's clone and is
installed into a virtual environment that can see the system ROS packages:

```
mkdir -p ~/sim_ws/src && cd ~/sim_ws/src
git clone -b dev-jazzy https://github.com/f1tenth/f1tenth_gym_ros.git
git clone -b dev-jax https://github.com/f1tenth/f1tenth_gym.git f1tenth_gym_ros/f1tenth_gym
python3 -m venv --system-site-packages ~/sim_ws/.venv && source ~/sim_ws/.venv/bin/activate
pip install -e ~/sim_ws/src/f1tenth_gym_ros/f1tenth_gym
cd ~/sim_ws && rosdep install -i --from-path src --rosdistro jazzy -y && colcon build --symlink-install
```

The [README](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-jazzy#installation) has the
complete step-by-step list (system packages, the Docker route, a FAQ for the usual errors).

# Number of cars

Set the number of cars with `num_agents`, either in `config/sim.yaml` or directly at launch:

```
ros2 launch f1tenth_gym_ros gym_bridge_launch.py num_agents:=4
```

Note the plural: the old `num_agent` spelling is refused at launch with a message rather than
silently running a single car.

# Driving the opponents

The first car is the ego, the rest are opponents. Each opponent gets its own topics
(`/opp_drive`, `/opp_drive2`, `/opp_drive3`, and likewise `/opp_scan`, `/opp_scan2`, ...,
`/opp_racecar/odom`, `/opp_racecar2/odom`, ...), and **a car only moves when you publish to its
drive topic** — an opponent you never command will simply sit on the grid. Every car also
publishes `collision`, `lap_count` and `lap_time` topics under its namespace, so you can score a
practice race without any extra tooling.

# Start poses

Every car needs a start pose in the config (`sx1`/`sy1`/`stheta1`, ...); the bridge refuses to
start and names the missing parameters otherwise. The shipped `sim.yaml` lines up eight cars on
the Levine map, so anything up to `num_agents:=8` works out of the box. Poses refer to
`base_link`, the rear axle, as on the real car.

# Visualisation

Foxglove opens automatically in the browser (`open_foxglove:=false` to stop that, e.g. in a
container). The shipped layout `config/foxglove/gym_bridge_foxglove.json` draws all eight cars
plus a lap counter and lap timer for the ego. RViz still works with `config/rviz/gym_bridge.rviz`.

# Training with reinforcement learning

For learning-based approaches, use `f1tenth_gym` on `dev-jax` directly, without ROS. It is
natively multi-agent (`step` takes a `(num_agents, 2)` action array), runs its physics in JAX and
batches many environments on a GPU, and ships a PureJaxRL-style PPO example
(`examples/jax_ppo_training.py`). Gymnasium wrappers flatten it to the single-agent `Box` spaces
that Stable-Baselines3 and CleanRL expect, with an optional SBX adapter.

```
git clone -b dev-jax https://github.com/f1tenth/f1tenth_gym.git && cd f1tenth_gym
uv sync --frozen            # add --no-group gpu on a machine without CUDA
uv run python examples/waypoint_follow.py
```

The [RL guide](https://f1tenth-gym.readthedocs.io/en/latest/rl.html) covers the batch API and the
wrappers. Note that the ROS bridge pins its physics to the CPU; a GPU only matters for your own
training code.

# Full documentation

- [f1tenth_gym_ros README (`dev-jazzy`)](https://github.com/f1tenth/f1tenth_gym_ros/tree/dev-jazzy#readme)
- [f1tenth_gym README (`dev-jax`)](https://github.com/f1tenth/f1tenth_gym/tree/dev-jax#readme) and
  [documentation](https://f1tenth-gym.readthedocs.io/en/latest/)
- On the car itself, the matching driver stack is the
  [`jazzy-devel` branch of f1tenth_system](https://github.com/f1tenth/f1tenth_system/tree/jazzy-devel).

Bugs or problems with any of them: please open a GitHub issue on the repository concerned.
