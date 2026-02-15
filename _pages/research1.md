---
layout: page
title: Simplfying Certifiable Estimation
nav: true
nav_order: 1
---

**Date:** 2026-02-14  
**Tags:** robotics, SLAM, factor-graphs, SDP, certifiable-estimation, optimization  

![Local vs certifiable “solve the same graph” pipeline](sandbox:/mnt/data/factorgraph_certifiable_pipeline.png)

---

## Table of contents

- [Why I care about certificates (not just good looking trajectories)](#why-i-care-about-certificates-not-just-good-looking-trajectories)
- [The key trick: the graph survives the lift](#the-key-trick-the-graph-survives-the-lift)
- [What “structure preserved” actually means in math terms](#what-structure-preserved-actually-means-in-math-terms)
- [Certi-FGO in one picture](#certi-fgo-in-one-picture)
- [What a lifted factor looks like (example)](#what-a-lifted-factor-looks-like-example)
- [A practical workflow you can actually run](#a-practical-workflow-you-can-actually-run)
- [Embedded media: a quick rabbit hole](#embedded-media-a-quick-rabbit-hole)
- [If you’re building systems: when to reach for this](#if-youre-building-systems-when-to-reach-for-this)

---

## Why I care about certificates (not just good looking trajectories)

If you’ve built a SLAM or navigation pipeline in the real world, you know the feeling: your factor graph converges fast… and occasionally converges **confidently to nonsense**. Local methods are amazing because they’re efficient and “plug-and-play,” but by design they target *a* stationary point, not *the* global solution.

Certifiable estimation flips the script: solve a convex relaxation (typically an SDP) and, when it’s tight, you get a **verifiable global optimum**—a certificate you can check after the fact. The catch is that SDPs at robotics scale are notorious: generic solvers don’t scale, and custom structure-exploiting implementations can be a whole research project.

The exciting middle ground is: **keep the factor-graph workflow, but add certifiability**.

---

## The key trick: the graph survives the lift

Here’s the central idea that makes the whole thing “feel like factor graphs again”:

> When you lift a QCQP through Shor’s relaxation and then apply Burer–Monteiro (BM) factorization, the **factor graph structure is preserved** because these transformations change the decision variables but *do not change the data matrices* that encode sparsity.

In the Certi-FGO framing, this becomes a one-to-one correspondence between original and lifted graphs: the BM-factorized problem admits a factor-graph decomposition whose **factors and variables correspond directly** to those of the original QCQP, preserving sparsity while enabling global guarantees.

---

## What “structure preserved” actually means in math terms

Most factor-graph problems we write down can be expressed (or rearranged) as a **QCQP** with block variables. A key observation: constraints usually act *per-variable* (e.g., “this rotation is orthogonal”), while measurements couple *small subsets* (e.g., odometry couples pose *i* and *j*). This induces block structure.

### 1) Constraints remain per-variable (block diagonal)

If the feasible set factors as a Cartesian product across variables, then each quadratic constraint touches only one variable block. In matrix form, that shows up as block-diagonal constraint matrices: each constraint matrix has a single nonzero block.

Concretely, the constraints can be rewritten blockwise, one block per variable.

### 2) Lifting doesn’t densify your sparsity

Shor’s relaxation replaces outer products \(XX^\top\) with a Gram matrix \(Z\), but the lifted blocks still correspond to the same variable pairs (now as \(Z_{ij}\)).

Then BM factorization writes \(Z = YY^\top\), and you can block-partition \(Y\) so each lifted block row corresponds to the original variable.

**Bottom line:** the lifted objective still decomposes into a sum of small factors over small neighborhoods, and the lifted constraints still apply per variable block.

---

## Certi-FGO in one picture

This diagram is the “storyboard” version of the whole pipeline: build a lifted factor graph, do local optimization in the lifted space, compute a certificate, and (if needed) increase rank and escape saddles (Riemannian Staircase).

![Figure: Certi-FGO overview on the Riemannian Staircase + certificates](sandbox:/mnt/data/certi_fgo_page9.png)

Two details I like in this view:

- The lifted feasible set is a **product** of per-variable manifolds \( \mathcal M^{(p)} = \mathcal M^{(p)}_1 \times \cdots \times \mathcal M^{(p)}_N \).
- The “verification” step checks the smallest eigenpair of the certificate matrix \(S\); if it’s PSD, you’re certified; otherwise increase rank and take a negative-curvature direction.

---

## What a lifted factor looks like (example)

One reason this approach is practical is that many lifted factors are “swap the variable type, keep the form.”

### Example: relative rotation factor

Start from the classic MLE-style Frobenius residual explanation of a relative rotation measurement:

- Original: \( \|R_j - R_i \tilde R_{ij}\|_F^2 \)

Then the lifted version is the same residual, but with lifted rotation variables \(Y_i, Y_j\) on a Stiefel manifold and the same measured \(\tilde R_{ij}\):

- Lifted: \( \|Y_j - Y_i \tilde R_{ij}\|_F^2 \)

That’s the “feel like factor graphs” moment: you still build a graph out of small residual factors; your optimizer still sees Jacobians and sparsity; you just changed the variable representation and wrapped it in a certifiable meta-algorithm.

---

## A practical workflow you can actually run

Here’s the mental model I use for implementing this in a robotics codebase:

1. **Model as usual**: build your factor graph (poses, landmarks, ranges, bearings, etc.).
2. **Ensure QCQP-representable pieces**: rotations, unit vectors, squared norms, etc.
3. **Lift variables**: rotations \(\to\) Stiefel blocks, translations \(\to\) higher-dimensional vectors (still unconstrained).
4. **Lift factors**: keep the same factor templates; swap in lifted variables.
5. **Run Riemannian Staircase**: local optimize, certify, and if not certified, increase rank and escape.

A simple “certify or climb” loop looks like:

```text
repeat:
  Y*  <- local-optimize lifted factor graph (rank p)
  S   <- build certificate matrix
  if min_eig(S) >= 0:
       return certified solution
  else:
       p <- p + 1
       escape along negative curvature direction
