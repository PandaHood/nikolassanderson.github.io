---
layout: page
title: Sparse Variable Projection
nav: true
nav_order: 2
---


**Date** February 12 2026  
**Tags** robotics, SLAM, SfM, nonlinear least squares, variable projection, sparsity, separability

{% include figure.html path="assets/img/Sparse.png" class="img-fluid rounded z-depth-1" %}
> **What this post is about**  
> Large perception back ends already exploit sparsity. This work pushes a second lever that is often sitting unused. Separability.  
> The goal is simple. Eliminate the easy variables in closed form, keep the hard variables for the optimizer, and do it in a way that still scales on real graphs.

---

## Why this matters

Modern perception pipelines end up solving huge nonlinear least squares problems. SLAM, structure from motion, sensor network localization. The variable counts can get massive and the solver is often the slowest part of the system.

Sparsity is the usual scaling story. Each measurement touches a few variables, so the Jacobians are sparse and the linear algebra stays tractable. That part is well understood and widely implemented.

There is another kind of structure that shows up all the time but is less consistently exploited. Many problems have a split where some variables are constrained and hard to optimize, while others appear linearly in the residuals and are easy to solve once the hard variables are fixed. Think of poses versus landmarks, or poses versus auxiliary direction variables used to model certain measurements.

When a variable appears linearly, there is often a closed form best value. Variable projection takes advantage of that. It removes the linear variables and produces a reduced problem over only the constrained variables. The reduced problem is smaller and often better conditioned, so it can converge faster.

So why is variable projection not the default in robotics back ends

A big reason is gauge symmetry. Many perception objectives do not change under a global shift or global rotation. That invariance creates rank deficiency in the cost structure. Standard variable projection routes can stumble here, or they end up forming dense reduced matrices that destroy the sparsity benefits.

---

## The usual route to variable projection

The classical picture is simple.

You write the least squares cost, linearize if needed, and form normal equations. If a block of variables is linear and unconstrained, you can eliminate it. The Schur complement is the common tool. It gives a reduced system in the remaining variables.

The pain point is also familiar.

The Schur complement is often dense even when the original system is sparse. Forming it explicitly costs memory and time. In large graphs, it can erase the benefit of eliminating variables in the first place.

That is the gap this work tries to close.

The approach aims to do variable projection while preserving the efficiency of the original sparse problem. The key is to avoid forming the dense reduced matrix and instead apply it implicitly as an operator.

---

## What changes in this work

The method targets a broad class of perception problems where the residuals are linear in the variables. In that setting the cost is globally quadratic, so the reduction can be done once as preprocessing and then reused.

The variables are partitioned into two groups.

- Constrained variables that are difficult to optimize, such as rotations
- Unconstrained variables that are easy to eliminate in closed form

The reduction eliminates the unconstrained group and creates a reduced quadratic cost over the constrained group.

The important promise is that the reduced problem is represented by a matrix free operator. You can evaluate cost, gradients, and Hessian vector products of the reduced problem without ever forming a dense Schur complement. You keep sparse operations and triangular solves, which can plug into standard iterative solvers.

---
{% include figure.html path="assets/img/Schur.png" class="img-fluid rounded z-depth-1" %}


## A simple checklist for when it applies

There is a clean set of conditions that can be checked before running anything.

- There is a set of unconstrained variables that you want to eliminate
- The cost residuals are linear functions
- The Jacobian block for the variables to be eliminated has a specific graph structure that enables a sparse basis construction

If those conditions hold, the method builds the operator once and then reuses it inside an iterative solver loop.

If conditions only partially hold, the work discusses extensions and the trade offs, especially when some residuals are not linear.

---

## The main technical idea

The reduced cost involves a Schur complement term that contains a pseudoinverse. That pseudoinverse is what makes the naive operator dense and expensive.

The method replaces that pseudoinverse pathway with an exact reformulation based on a CR decomposition.

Then it uses a graph view of the Jacobian block for the unconstrained variables. Many perception problems have residuals that depend on pairwise differences of unconstrained variables. In those cases, the Jacobian block behaves like an incidence matrix of a connected graph.

That graph fact matters because removing one column of an incidence matrix yields a basis for the column space. With that choice, the inner matrix becomes a reduced graph Laplacian. It is positive definite and sparse, so it admits a sparse Cholesky factorization.

After that, applying the reduced operator becomes a short sequence of steps.

- Sparse matrix products
- Two sparse triangular solves with the Cholesky factors
- Another sparse product

No dense Schur complement. No explicit pseudoinverse. And the sparsity pattern stays close to the original problem structure.

{% include figure.html path="assets/img/varpro-sparsity.png" class="img-fluid rounded z-depth-1" %}

---

## What you get in practice

The reduction shrinks the problem size, often improves conditioning, and keeps the solver scalable.

A practical detail I like is that the variable projection step is a one time preprocessing pass. After that, the reduced operator integrates into iterative nonlinear least squares solvers that already rely on matrix vector products and preconditioned conjugate gradients.

That makes the method feel less like a new solver and more like a new backend option.

---

{% include figure.html path="assets/img/iteration.png" class="img-fluid rounded z-depth-1" %}


## Results you can read at a glance

The experiments cover multiple standard problem families.

- pose graph optimization
- range aided SLAM
- sensor network localization
- structure from motion

Across synthetic and real benchmarks, the reduced formulation consistently improves runtime while maintaining accuracy. The strongest gains show up when there are many more unconstrained variables than constrained ones, a common pattern in structure from motion where there are huge numbers of points.

{% include figure.html path="assets/img/varpro-convergence.png" class="img-fluid rounded z-depth-1" %}

A final practical win is memory. Avoiding dense reduced matrices and avoiding direct factorizations helps on large instances where memory becomes the bottleneck.

---

## Links

### Preprint

[![arXiv 2512.07969](https://img.shields.io/badge/arXiv-2512.07969-b31b1b.svg)](https://arxiv.org/abs/2512.07969)  
[Read on arXiv](https://arxiv.org/abs/2512.07969)  
[Download PDF](https://arxiv.org/pdf/2512.07969.pdf)

<iframe
  src="https://arxiv.org/pdf/2512.07969.pdf"
  width="100%"
  height="650"
  style="border:1px solid #e5e7eb; border-radius:12px;"
  loading="lazy">
</iframe>

---

### Open source code

[![GitHub UMich RobotExploration](https://img.shields.io/badge/GitHub-UMich--RobotExploration-181717.svg)](https://github.com/UMich-RobotExploration)  
[View the GitHub org](https://github.com/UMich-RobotExploration)

<iframe
  src="https://ghbtns.com/github-btn.html?user=UMich-RobotExploration&type=follow&count=true"
  frameborder="0"
  scrolling="0"
  width="210"
  height="20"
  title="GitHub follow button">
</iframe>


---

## Closing thought

The headline is not that variable projection is new. The headline is that variable projection can be made to fit the modern factor graph scaling story.

The method keeps the sparsity benefits of the original problem, avoids forming dense reduced matrices, and handles gauge induced rank deficiency with a clean graph based construction.

If your perception backend has a large set of linear unconstrained variables, this is a strong candidate for a faster drop in solve without rewriting the whole solver stack.
