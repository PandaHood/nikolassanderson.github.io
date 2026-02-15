---
layout: page
title: Online Certifable SLAM
nav: true
nav_order: 3
---

# Online Certifiable Estimation with Cert CFS

**Date** 2026-02-14  
**Tags** robotics, SLAM, factor graphs, online estimation, certifiable estimation, concurrent smoothing, SDP


> **What this post is about**  
> Online SLAM needs two things that fight each other. Fast updates and global consistency.  
> Local smoothing is fast but can get stuck with no warning. Certifiable estimation can verify correctness but is usually too expensive to run all the time.  
> Cert CFS combines them by keeping the fast estimator unchanged and adding a certifiable long horizon smoother in the delayed back end.

---

## Why online SLAM still fails in practice

Factor graphs are a great modeling language for SLAM. Each sensor measurement becomes a factor. The graph stays sparse. Incremental solvers exploit that structure to update in real time.

The weak point is still local optimization. Most back ends solve a nonconvex objective with a local method. When the trajectory is well initialized and the measurements behave, the result is excellent. When initialization is poor, or the problem has symmetries, or loop closures arrive late, the solver can settle into a bad local minimum. The estimate can look stable while still being wrong.

What is missing is a simple signal that answers a basic question.

Is the current solution globally consistent

That is what a certificate gives. A certificate is not another heuristic score. It is a test that can verify global optimality for a relaxed problem, and in many regimes that relaxed problem matches the original one.

---

## Why certifiable estimation has stayed offline

Certifiably correct estimation builds a convex relaxation, often an SDP, that provides a global lower bound. When the relaxation is tight, the optimizer recovers the global optimum and the certificate confirms it.

The issue is cost. Generic SDP solvers are heavy at robotics scale. Even specialized certifiable solvers are usually run in batch. That makes them hard to use inside an online pipeline that is driven by sensor rate timing.

So the real challenge becomes system design.

How do you get certificates without breaking real time behavior

---

## A concurrency trick that makes room for certification

Concurrent Filtering and Smoothing is a clean idea. It splits the full estimation problem into two branches.

- A high rate branch that tracks the recent states and updates quickly
- A delayed branch that works on long horizon consistency

The two branches do not share the whole state. They share a small separator set. The separator acts like the interface between the fast and slow sides. Each side summarizes its influence on the separator and exchanges only that summary during synchronization.

This matters because it gives a safe place to run slower computation. The slow branch can be expensive as long as the fast branch stays responsive.

That observation is the opening for certifiable estimation.

---

## The main move in Cert CFS

Cert CFS replaces the slow local smoother in a concurrent architecture with a certifiable smoother.

The fast estimator stays the same. It keeps producing real time updates.

The delayed back end changes. Instead of running a standard long horizon local solve, it periodically runs a certifiable optimization procedure and produces a certified solution when the certificate test passes.

The communication rule stays simple. The filter and certifiable smoother communicate only through separator summaries. That preserves asynchronous updates and keeps the system modular.

This design is attractive because it does not require rewriting the front end. It adds a second back end that can correct failures and can tell you when it has produced a globally consistent result.

---

## What the certifiable smoother is doing

The certifiable back end is built on a standard certifiable chain.

First it expresses the long horizon subproblem as a QCQP. This covers common geometric estimation blocks in SLAM.

Then it applies Shor relaxation to lift the QCQP into an SDP. The SDP provides a global lower bound.

To make the SDP solvable at scale, it uses Burer Monteiro factorization. The decision matrix becomes a low rank product. This reduces memory and computation while preserving positive semidefiniteness by construction.

The solve itself runs as a Riemannian Staircase procedure.

- Choose a rank
- Optimize on the lifted manifold
- Form a certificate matrix from the KKT conditions
- Check the smallest eigenvalue
- If the test fails, increase rank and continue

The key point is that the back end can return more than an estimate.

It can return an estimate with an a posteriori certificate when the test passes.

When the test fails, it also reveals negative curvature information that helps the staircase escape.

---

## How the two branches stay consistent

Between synchronization events, the fast and slow branches can be temporarily inconsistent. That is expected in concurrent smoothing.

Synchronization restores agreement by exchanging only separator information.

- The filter sends its current separator potential to the certifiable smoother
- The certifiable smoother sends its separator summary back

After synchronization, the combined result matches the joint posterior implied by all measurements under the concurrent factorization.

In other words, the system gets global consistency without requiring the fast branch to wait.

---

## What changes in behavior when something goes wrong

A standard local back end can fail silently. It can accept a poor initialization and converge to a bad basin. The user sees a smooth trajectory and has no strong indicator of global correctness.

Cert CFS adds a different mode.

When the certifiable back end succeeds, it can certify the solution and provide a verified long horizon correction. That correction flows back through the separator summary and improves the online estimate.

When the certifiable back end does not certify, it can keep working at a higher rank while the filter continues operating. The system does not freeze. It simply has not yet produced a certified correction.

That changes the story from silent failure to detectable failure with a recovery path.

---

## What the evaluation shows

The framework is evaluated in two styles.

### Simulated online streaming on benchmark graphs

The setup streams measurements sequentially at a fixed rate. Each method processes the same measurement order. Variables are initialized through odometry chaining to mimic online practice.

Baselines include full horizon smoothing, fixed lag smoothing, and a concurrent method that uses a local optimizer in the slow branch.

Across pose graph and range aided datasets, Cert CFS reduces trajectory error relative to the local online baselines. The plots track RMSE over time and show how errors evolve during the run.

{% include figure.html path="assets/img/benchmarkplot1.png" class="img-fluid rounded z-depth-1" %}

{% include figure.html path="assets/img/benchmarkplot2.png" class="img-fluid rounded z-depth-1" %}

Timing is also reported. The filter side stays real time. The smoother side is slower, as expected, and runs asynchronously. A useful detail is that the per iteration timing can be labeled by the certified rank achieved. That shows how often low rank solves certify and when the staircase needs to climb.

### Integration into a lidar inertial SLAM system

The second test integrates the framework into a modern lidar inertial mapping pipeline. The experiment intentionally induces a failure mode by degrading odometry behavior through a parameter mismatch. In that regime, a purely local smoothing back end struggles to recover.

The certifiable back end is able to produce a correction that local smoothing cannot. That is the system level value. It is not only a better objective value. It is a recovery mechanism when the online pipeline drifts into a bad basin.

{% include figure.html path="assets/img/dliom.png" class="img-fluid rounded z-depth-1" %}

---

## What to take away

Cert CFS is a framework change more than a new factor.

It keeps the normal online estimator. It keeps the concurrency idea. It adds a certifiable long horizon solver in the place where extra computation is allowed.

The significance is practical.

- Real time behavior stays intact because the filter is unchanged
- Long horizon consistency improves because the slow branch can certify and correct
- Failure becomes detectable because certification is an explicit test
- Recovery becomes possible because the staircase provides a principled try harder mechanism

For systems that need reliability, the certificate is a strong form of feedback. It says when the back end has truly solved the long horizon problem, not just converged somewhere.


