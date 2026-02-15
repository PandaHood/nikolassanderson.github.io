---
layout: page
title: Research
permalink: /research/
description: Visual demonstrations of algorithms and field deployments
nav: true
nav_order: 3
---

**My research** develops algorithms and systems that enable robots to
explore and monitor challenging environments, with a particular focus on
underwater environments. I work on the tools that will allow
future robots to autonomously study and understand the natural world.

For a complete list of my publications, see my
[Google Scholar profile](https://scholar.google.com/citations?user=Ym3SpKgAAAAJ).
Below are some quick highlights from recent projects.

## Certifiably Correct Navigation

Two major challenge in robotic deployments stem from modern localization
systems. Current localization techniques are not only brittle in the face of
real-world conditions, but they often fail silently without any indication and
thus no ability to recover. Our work in certifiable navigation aims to address
these challenges by developing algorithms that not only are capable of
guaranteeing optimal performance under certain conditions, but also provide
certificates of correctness that can be used to detect failures and trigger
recovery behaviors.

Below you can see our CORA algorithm (a certifiably correct solver) in action on
several real-world datasets.
We are randomly initializing each instance -- a scenario that breaks existing state-of-the-art
solvers -- and showing that regardless of initialization, our approach returns a **certifiably**
correct estimate of the robot trajectories.

To add to the excitement, we can do all of this **faster** than
the existing methods.


<!-- Results from the Plaza dataset -->
<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/plaza1_solution.gif" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/plaza2_solution.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>

<!-- Results from other Range-Aided Problems -->
<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/tiers_solution.gif" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/goats_solution.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Four different benchmark data sets that our solver (CORA) is solving. Each
    of these is randomly initialized and the solver progressively "untangles"
    them and finds the globally optimal solution.
</div>


<div class="row mt-3">
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/cora_runtime_speedup.png" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-6 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/rotating_spectrahedron.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    <bf>Left:</bf>
    Runtime speedup our method gets over GTSAM, a state-of-the-art solver for robot navigation problems.
    Right:
    A fun animation of the spectrahedron, a geometric object closely related to
    the tools used in certifiably correct optimization.
</div>

## Large-Scale Multi-Robot Navigation

This is a collection of experiments set up to showcase the benefits of certifiably correct navigation in
complex, multi-agent localization problems. We built three sensor payloads, each with a camera (for visual odometry) and ultra-widebad radio (to get distance measurements between the different payloads). The
goal was to see if we can use the payloads own (noisy) motion and the inter-agent distance measurements
to (a) correct for the error in the odometry and (b) obtain a globally consistent estimate for all of the
payload's trajectories.

Technologies like this are critical for large-scale mapping and observation
settings, where many agents will need to be deployed and globally consistent
representations will need to be constructed from their distributed observations.

<!-- side-by-side gifs of the three payloads -->
<div class="row mt-3">
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam1.gif" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam2.gif" class="img-fluid rounded z-depth-1" %}
    </div>
    <div class="col-sm-4 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cam3.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    The image stream captured by the three different payloads.
</div>

<!-- the odometries computed from the cameras -->
<div class="row mt-3">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_all_odometries.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    An overlay of trajectory estimates given by visual odometry (VO). Notice the substantial drift given by the VO systems.
</div>

<!-- CORA solving the SLAM problem -->
<div class="row mt-3">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/mit_outdoor_cora_solution.gif" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="caption">
    Our solver fusing all of the information to obtain a globally consistent and
    certifiably correct estimate of the three trajectories.
</div>

## Marine Robotics

Some experiments done in the Charles River in Cambridge, MA on a particularly
pleasant day. Featuring an autonomous kayak (the jetyak) and my wonderful
collaborator, Brendan O'Neill.

<div class="row mt-3">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/alan_brendan_river_experiments.jpg" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
<div class="row mt-3">
    <div class="col-sm-12 mt-3 mt-md-0">
        {% include figure.html path="assets/img/new_imgs/brendan_on_river_experiments.png" class="img-fluid rounded z-depth-1" %}
    </div>
</div>
