---
layout: page
title: multi-view SLAM visualization
description: understanding optimization through multiple perspectives
img: assets/img/new_imgs/mit_outdoor_all_odometries.gif
importance: 3
category: robotics
---

Understanding SLAM requires seeing it from multiple angles - both literally and figuratively. This project showcases how different viewpoints reveal different aspects of the optimization process, helping us debug algorithms and communicate complex concepts.

## The MIT outdoor dataset

This challenging multi-robot dataset captures the complexity of real-world SLAM:

<div class="row mt-3">
    <div class="col-sm mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_all_odometries.gif" title="All Odometry Traces" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Raw odometry from multiple robots - notice the drift accumulating over time. This is the input our SLAM algorithms must correct.
</div>

## Multiple camera perspectives

Viewing the optimization from different angles helps us understand the 3D structure of the solution:

<div class="row mt-3">
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam1.gif" title="Camera 1" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam2.gif" title="Camera 2" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam3.gif" title="Camera 3" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Three camera angles showing the same optimization process - each perspective reveals different geometric relationships in the problem.
</div>

## Comparing optimization approaches

Side-by-side comparison of our CORA algorithm versus traditional methods:

<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cora_solution.gif" title="CORA Solution" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_gtsam_solution.gif" title="GTSAM Solution" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Left: CORA converging to the global optimum. Right: GTSAM's local optimization. Both reach similar final solutions, but CORA provides guarantees.
</div>

## Urban environments

SLAM in structured urban environments presents unique challenges with buildings, symmetry, and perceptual aliasing:

<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/plaza1_solution.gif" title="Plaza 1" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/plaza2_solution.gif" title="Plaza 2" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Urban plaza scenarios with multiple loop closures - watching the algorithm recognize when it has returned to a previously visited location.
</div>

## Complex geometries

<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/tiers_solution.gif" title="Tiers Dataset" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/goats_solution.gif" title="GOATS Dataset" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Left: Multi-level environment requiring 3D reasoning. Right: Large-scale outdoor navigation from the GOATS benchmark.
</div>

## Why visualization matters

These animations are more than just pretty pictures - they're essential tools for algorithm development (spotting bugs and unexpected behaviors), performance analysis (understanding where and why algorithms struggle), communication (explaining complex optimization concepts to diverse audiences), and education (teaching students about SLAM and robotics).

By seeing optimization unfold in real-time, we gain intuition that guides the development of better algorithms.

---

*These visualizations use data from public benchmarks and our own experiments to demonstrate SLAM algorithm performance across diverse scenarios.*
