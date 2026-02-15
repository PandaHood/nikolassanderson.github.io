---
layout: page
title: river field robotics
description: autonomous navigation in dynamic aquatic environments
img: assets/img/new_imgs/alan_brendan_river_experiments.jpg
importance: 2
category: robotics
---

Field robotics brings the challenges of the real world directly to our algorithms. River environments present unique difficulties: strong currents, variable water conditions, limited visibility, and the unpredictability of natural settings. Our work focuses on enabling robust autonomous navigation and monitoring in these dynamic freshwater ecosystems.

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/alan_brendan_river_experiments.jpg" title="River Field Work" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    On-site during river experiments, preparing autonomous systems for deployment in challenging freshwater environments.
</div>

## The challenge

Rivers are deceptively complex environments for autonomous robots:

- Dynamic flow fields: Currents vary with depth, location, and time
- Limited localization: GPS signals can be unreliable near vegetation and water
- Sensor challenges: Water clarity, reflections, and foam affect vision systems
- Safety constraints: Operating near infrastructure, wildlife, and changing water levels
- Environmental monitoring: Collecting meaningful scientific data while navigating

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/brendan_on_river_experiments.png" title="System Deployment" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Deploying and testing navigation algorithms in real river conditions - where theory meets practice.
</div>

## Our approach

Our research combines robust SLAM algorithms with adaptive control to handle the uncertainties of river navigation:

1. Multi-sensor fusion: Integrating IMU, GPS, visual odometry, and flow sensors
2. Robust state estimation: Using our CORA backend to handle noisy measurements
3. Current compensation: Adapting control strategies to flow conditions
4. Environmental mapping: Building maps for both navigation and scientific purposes

## From theory to practice

Field deployments are where we validate our algorithms against reality. The gap between simulation and real-world performance drives us to develop more robust outlier rejection methods, better uncertainty quantification, adaptive algorithms that learn from the environment, and fail-safe behaviors for unexpected situations.

Every field test provides invaluable insights that improve our algorithms for both freshwater and marine applications.

## Broader impact

This work contributes to freshwater ecosystem monitoring, climate science through understanding river dynamics, infrastructure inspection, and search and rescue operations.

---

*This research bridges the gap between cutting-edge SLAM algorithms and real-world environmental monitoring applications.*
