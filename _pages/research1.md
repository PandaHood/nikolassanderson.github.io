---
layout: page
title: Simplfying Certifiable Estimation
nav: true
nav_order: 1
---

**Date:** 2026-02-14  
**Tags:** robotics, SLAM, factor-graphs, certifiable-estimation, SDP, optimization

 {% include figure.html path="assets/img/certi-fgo.png" class="img-fluid rounded z-depth-1" %} 
> **What this post is about:** The Certi-FGO paper asks a simple question: *can we keep the usability and scalability of factor graphs, but add a “this solution is globally optimal” certificate?*  
> The answer is **yes**, by lifting the problem the right way **without destroying factor-graph sparsity**.

---

## Why this matters

Factor graphs are the standard tool for SLAM and state estimation because they scale: each measurement becomes a small factor, sparsity falls out naturally, and we can solve huge problems quickly.

But the downside is equally familiar: most solvers we use are **local**. They converge to a nearby stationary point. When the problem is well-conditioned and initialization is good, that’s fine. When it isn’t—symmetries, poor initialization, ambiguous data association, multi-robot alignment—local solvers can converge to the wrong answer and still look “confident.”

The paper’s core motivation is to add a missing capability:

- Not just “here is a solution,” but **“here is a certificate that this solution is globally optimal.”**

That certificate changes how you can build systems. It gives you a principled *trust signal* you can use downstream (planning, mapping QA, loop-closure validation, multi-robot alignment gates).

---

## The usual route to certificates

A common way to get certifiability is to form a **convex relaxation** of the original nonconvex estimation problem (often a QCQP) as a **semidefinite program (SDP)**. If the relaxation is tight, the SDP solution corresponds to the global optimum of the original problem—so you’re done, with proof.

The obstacle: generic SDP solvers don’t scale well for large robotics graphs. If “certifiable” requires solving a giant dense SDP, it stays a theory tool, not a practical backend.

So the paper’s question becomes more specific:

> Can we get the benefits of an SDP relaxation **without giving up factor graph structure**?

---

## The key idea

The big insight is that the factor graph’s structure can survive the two transformations that usually scare people:

1. **Shor’s relaxation (lifting)**: replaces products of variables with a lifted matrix representation.
2. **Burer–Monteiro factorization (BM)**: represents that lifted matrix as a low-rank product, turning the SDP into a (structured) nonconvex problem on a manifold.

Here’s the punchline in plain terms:

- **Lifting changes what the variables look like**, but it doesn’t have to change *which variables interact*.
- If the original factor graph only couples small neighborhoods (like pose pairs), the lifted version can be built so that it *still* couples only those neighborhoods.

That means we can build a **lifted factor graph** that looks and behaves like a normal factor graph:
- small factors
- sparse structure
- scalable computation

…but with the ability to produce a **certificate**.

This is why the paper is significant: it reframes certifiable estimation as something that can live inside the factor-graph workflow, rather than replacing it with an entirely different solver stack.

---

## What the Certi-FGO pipeline does

The paper lays out a practical loop that looks like this:

### Step 1 — Build the lifted factor graph
You start with your usual estimation problem (poses, relative measurements, maybe landmarks) and rewrite it as a QCQP. Then you lift it (Shor relaxation) and apply BM factorization so the variables become *lifted blocks*.

In practice, rotation-like variables become **Stiefel-manifold blocks** (tall orthonormal matrices), and the factors become lifted versions of familiar residuals (same “two-node” structure, different variable type).

### Step 2 — Optimize locally *in the lifted space*
You run a local solver, but now it’s **Riemannian optimization** over the product of these lifted manifolds. This step is conceptually similar to “run Gauss–Newton on the graph,” just on different geometry.

### Step 3 — Certify
After optimizing, you compute a certificate object (the paper uses a certificate matrix whose PSD-ness indicates global optimality). Operationally, you check something like:

- if the smallest eigenvalue is nonnegative → **certified globally optimal**
- otherwise → not certified (either the relaxation isn’t tight at this rank, or you’re at a bad stationary point)

### Step 4 — If not certified, increase rank and try again (Riemannian Staircase)
If the certificate fails, the algorithm increases the rank of the BM factorization and continues—this is the “staircase” mechanism. The idea is that as you increase rank, you have a better chance of reaching a point that corresponds to the tight SDP solution.

**This is a big practical win:** the method has a built-in, principled “try harder” knob (rank), rather than only heuristic restarts.

---
 {% include figure.html path="assets/img/Plaza2-CORA.gif" class="img-fluid rounded z-depth-1" %} 
 ---

## What’s the actual significance?

Here’s what I take away as the “so what”:

1. **Certifiability becomes a *drop-in capability***  
   If you already think in factor graphs, Certi-FGO suggests you don’t need to abandon that ecosystem to get global guarantees.

2. **Structure is the scaling story**  
   The reason factor graphs scale is sparsity. The paper’s central contribution is showing how to keep that structure through lifting + BM, so certification doesn’t automatically imply “dense SDP pain.”

3. **A clean system-level interface**  
   From a system perspective, this gives a nice API:
   - run estimation
   - ask: “certified or not?”
   - if not, run a principled escalation (rank)

That’s exactly the kind of behavior you want in safety-critical or high-autonomy settings: don’t just output an estimate—output an estimate with a verifiable quality flag.


---

 {% include figure.html path="assets/img/plots.png" class="img-fluid rounded z-depth-1" %} 


## Closing thought

Certi-FGO is exciting because it treats certifiability as a **workflow feature**, not just a theoretical property. The paper’s story is basically: *don’t throw away factor graphs—lift them carefully so you can keep sparsity, optimize efficiently, and still certify global optimality when the relaxation is tight.*
