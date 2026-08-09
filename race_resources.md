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

<h3 id="obstacle-avoidance">Obstacle Avoidance &mdash; Mandatory Check</h3>

<p>
<b>Every team must pass an obstacle avoidance check on site, immediately before the qualification
time trials on September 29th.</b> This is not a formality: a car that does not pass does
not run the time trials, and a team that does not run the time trials cannot compete. The check is
done in person at the venue and there will also be a required short video submission before the competition (September 12th).
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
<b>An updated <a href="https://github.com/f1tenth/f1tenth_gym_ros">f1tenth_gym_ros</a> supporting
multi-car (4-car) testing is coming soon.</b> It will be the recommended way to practice for the
mandatory obstacle avoidance check and for multi-car racing, so plan your preparation around it.
</p>

<p>
The currently released f1tenth_gym_ros supports two cars, while the underlying
<a href="https://github.com/f1tenth/f1tenth_gym">f1tenth_gym</a> already supports multiple vehicles.
<b>We will link the updated version here as soon as it is released</b> &mdash; please check back
shortly.
</p>
