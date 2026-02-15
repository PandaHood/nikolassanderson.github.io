---
layout: page
title: Mixed-Integer Model Predictive Control
description: Mixed-integer program to perform path-planning with model predictive control for 2-D quadrotor model
category: coursework
img: assets/img/projects/mip_control.jpg
---
<!-- links:
- icon: github
  icon_pack: fab
  name: GitHub
  url: https://github.com/alanpapalia/miqcp-planning -->

As part of MIT's course 16.413 I worked on a team to derive a model-predictive
controller for a simulated quadrotor in a non-convex planning space. I used <a
href="https://scip.zib.de/"> SCIP</a>, an open-source optimization software in
conjunction with simplified quadrotor dynamics model to perform the
path-planning subject to obstacle avoidance constraints.

Because objects could be placed arbitrarily within the environment, the planning
problem was inherently non-convex. For this reason the problem was modeled as a
mixed-integer problem.

In <a href="https://github.com/alanpapalia/miqcp-planning"> this repo</a> all of
our work is shown in a Jupyter Notebook, along with a brief explanation of some
relevant topics in optimization and a derivation of the quadrotor dynamics.

<p align="center">
    <img align="center" src="/assets/img/projects/mip_control.jpg" alt="Simulator Snapshot" width="60%" />
</p>
<div class="caption"> A snapshot of the simulator, the planner had to find a
trajectory to the other side of the square while adhering to the vehicle
dynamics. </div>
