---
layout: page
title: Research
nav: true
nav_order: 1
---

My research develops algorithms and systems that enable robots to explore and monitor challenging environments. Among the topics I have worked on certifably correct estimation, acclerating robotic perception, large-scale data collections, and high-speed off-road robotics. 


## Accelerating Robotics Perception

{% include figure.html path="assets/img/Sparse.png" class="img-fluid rounded z-depth-1" %}

Our approach exploits separability in opti-
mization problem to perform variable projection and analytically eliminate a subset of variables (reducing problem size and improving conditioning), while preserving the efficiency of the original problem’s sparsity structure. Our approach can be applied as a one-time preprocessing step before passing the problem to a standard iterative solver.

## Certifably Correct SLAM on Factor-graphs

We show that the factor graph and certifiable estimation paradigms, which have thus far been treated as essentially independent in the literature, can be naturally synthesized into a unified framework for certifiable factor graph optimization that combines the ease of use of the former with the strong performance guarantees of the latter. The key insight enabling our synthesis is that the core mathematical constructions used to develop certifiable estimators (Shor's relaxation and Burer-Monteiro factorization) inherit a factor graph structure from the original problem: applying these transformations to a QCQP-representable estimation task with an associated factor graph model yields a lifted problem with identical factor graph connectivity whose constituent variables and factors are simple one-to-one algebraic transformations (lifts) of those appearing in the original QCQP's factor graph. This correspondence enables the Riemannian Staircase methodology for certifiable estimation to be easily instantiated and deployed using the same mature, highly-performant factor graph libraries and workflows already ubiquitously employed throughout robotics and computer vision. Experimental evaluation on a variety of pose graph optimization, landmark SLAM, and range-aided SLAM benchmarks demonstrates that our certifiable factor graph optimization methodology enables the implementation of certifiable estimators that are functionally equivalent to current state-of-the-art hand-designed, problem-specific methods, while dramatically reducing the required implementation effort from the order of months to hours. 

{% include figure.html path="assets/img/certi-fgo.png" class="img-fluid rounded z-depth-1" %}

Overview of our framework for certifiable factor graph optimization. Starting from a factor graph model of a QCQP-representable estimation problem
(left), we construct Shor’s semidefinite relaxation and solve it using the Riemannian Staircase meta-algorithm (right). In each iteration of the Staircase, we apply
local optimization to a Burer-Monteiro-factored instance of the relaxation to recover a first-order stationary point Y ⋆. We then test whether Y ⋆ determines
an optimal SDP solution Z⋆ = Y ⋆Y ⋆T using the certificate matrix S: if S ⪰ 0, then Z⋆ is certified optimal and the algorithm returns the symmetric factor
Y ⋆; otherwise, the factorization dimension p is increased, and optimization resumes at the next level. Crucially, Shor’s relaxation and all of its associated
Burer-Monteiro factorizations are parameterized by the same data matrices {Qk } and {Am} that define the original QCQP; in particular, this implies that
each of the BM-factored SDP relaxations inherits a factor graph representation whose variables and factors are simple one-to-one algebraic transformations
(lifts) of those appearing in the input graph. This enables us to automatically instantiate and locally optimize the BM-factored SDP relaxations appearing in
each level of the Riemannian Staircase directly from the input factor graph using existing factor graph software libraries. Our approach thus preserves the
modeling convenience and computational efficiency of current state-of-the-art factor graph-based software libraries and workflows while additionally providing
the robustness and global optimality guarantees of certifiable estimation


{% include figure.html path="assets/img/Plaza2-CORA.gif" class="img-fluid rounded z-depth-1" %}

We can recover globally optimial solutions from random initalizations using the certifable factor-graph framework.


## NEUROAM Large-Scale Heterogeneous Data Collection

This paper presents the Northeastern University Robotic Observation and Mapping (NeuROAM) dataset, a large-scale, multi-modal, multi-robot dataset designed to facilitate research in multi-robot perception in dynamic, communication- constrained settings. NeuROAM includes data collected simultaneously from multiple heterogeneous robot platforms, including wheeled and legged robots with different motion patterns and dynamics, operating in semi-urban outdoor and indoor environments on a college campus. These environments are highly dynamic, with varying lighting conditions and substantial pedestrian traffic. The dataset features multi-modal sensing, including stereo RGB cameras, inertial measurement units (IMU), and LiDAR, and detailed inter-robot communication monitoring, which supports analysis of real-world communication patterns and the development of algorithms that explicitly account for communication constraints.

{% include figure.html path="assets/img/teaser_new.png" class="img-fluid rounded z-depth-1" %}

The NeuROAM dataset is collected simultaneously using five heterogeneous platforms on the Northeastern University campus in Boston. It includes kilometer-scale outdoor trajectories as well as indoor trajectories spanning multiple buildings and floors. The dataset presents a wide range of challenging scenarios for localization, mapping, and communication, including but not limited to: (1) elevator and basement, (2) degenerate stairways and bridges, (3) long traversal on irregular staircases, (4) reflective building flooring, (5) large glass surfaces, (6) highly dynamic scenes, and (7) nearly identical floor plans across levels.


{% include figure.html path="assets/img/payload_screenshot.png" class="img-fluid rounded z-depth-1" %}

Each robot platform was equipped with a custom sensor payload including an Ouster LiDAR, stereo RGB cameras, a VectorNav IMU, a Doodle Labs long-range radio, and a GPS receiver. Each payload carried identical hardware, with exception to the LiDAR model: two payloads used 128-beam Ouster sensors (OS1-128) on the Go2W and AgileX Hunter platforms, while the remaining robots carried 32-beam sensors (OS1-32).


{% include figure.html path="assets/img/PAYLOAD_LAYERS.jpg" class="img-fluid rounded z-depth-1" %}

Side view of the different levels within the payload (left). Isometric view of the different levels (right)


## F1-Fifth

Not much to say, it goes fast!

{% include figure.html path="assets/img/F1-fith.jpg" class="img-fluid rounded z-depth-1" %}




