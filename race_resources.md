---
title: Roboracer IROS 2026 Race Resources
short_title: Race Resources
layout: page
section: race
---

All necessary information about the race e.g. rules, scoring system,
simulation environments and track data will be displayed here.

- [Rules]({% link rules.md %})
<!-- ORIENTATION_LINKS --><!-- /ORIENTATION_LINKS -->

<h3 id="competition-format">Competition Format</h3>

<p>
The IROS 2026 competition is run as a <b>multi-car (4-car) knockout competition</b>. Teams first
complete qualification time trials to determine seeding, and are then placed into a knockout bracket
in which four cars race on the track at the same time.
</p>

<p>
<b>Final rules to be updated soon.</b>
</p>

<h3 id="obstacle-avoidance">Obstacle Avoidance - Mandatory Check</h3>

<p>
<b>Every team must pass an obstacle avoidance check on site, immediately before the qualification
time trials on September 29th.</b> This is not a formality: a car that does not pass does not run
the time trials, and a team that does not run the time trials cannot compete.
</p>

<p>
<b>Obstacle avoidance must also be shown in your video demonstration, due September 12th.</b> That
video already asks you to show your car driving autonomously around a track without human
intervention; for IROS 2026 it must additionally show your car avoiding obstacles. We review these
videos and will come back to any team whose obstacle avoidance does not yet look ready, so you have
time to improve it before you travel rather than being turned away on site. The video is there to
help you pass the on-site check - it does not replace it.
</p>

<p>
<b>Please prepare for this seriously.</b> With up to four cars on the track at once, the checks are
substantially more rigorous than in a two-car format, and they cover <b>both static and dynamic
obstacles</b>. In past competitions many teams have struggled with obstacle avoidance even in the
<i>static</i> case, so treat it as a core part of your stack rather than something to bolt on at the
venue.
</p>

<p>
Pay particular attention to the <b>dynamic case, where more than one opponent may be moving on the
track at the same time</b>. Avoiding a single moving car is a very different problem from holding a
safe line with three other cars around you, and that is what you should be practising against.
</p>

<p>
<b>More details to come.</b>
</p>

<h3 id="track-surface">Track Surface</h3>

<p>
The racing surface is the <b>bare exhibition hall floor</b>. Teams should tune and
test their vehicles accordingly, in particular tire choice, suspension setup and any friction
assumptions in their control stack.
</p>

<h3 id="simulation">Simulation</h3>

<p>
<b>A multi-car (4-car) version of f1tenth_gym_ros is available now:</b>
<a href="https://github.com/cedrichld/f1tenth_gym_ros/tree/four-cars">cedrichld/f1tenth_gym_ros,
<code>four-cars</code> branch</a>. This is the recommended way to practice for the mandatory
obstacle avoidance check and for multi-car racing in sim.
</p>

<p>
Note that this is a working branch and has <b>not yet been merged into the official
<a href="https://github.com/f1tenth/f1tenth_gym_ros">f1tenth_gym_ros</a></b>, so clone the
<code>four-cars</code> branch directly for now. The released f1tenth_gym_ros supports two cars,
while the underlying <a href="https://github.com/f1tenth/f1tenth_gym">f1tenth_gym</a> already
supports multiple vehicles. We will point this link at the official repository once the change is
upstream.
</p>

<video src="images/Roboracer/four_car_sim.mp4" poster="images/Roboracer/four_car_sim.jpg"
	autoplay muted loop playsinline controls preload="metadata"
	style="width: 100%; max-width: 900px; height: auto; display: block; margin: 1em auto 0;">
	Your browser does not support embedded video.
	<a href="images/Roboracer/four_car_sim.mp4">Download the clip</a> instead.
</video>

<p style="text-align: center; font-size: 0.8rem;">
<i>Four cars running in the <code>four-cars</code> branch of f1tenth_gym_ros.</i>
</p>
