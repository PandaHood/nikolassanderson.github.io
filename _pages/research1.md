---
layout: page
title: Simplfying Certifiable Estimation
nav: true
nav_order: 1
---

**Date** February 10 2026  
**Tags** robotics, SLAM, factor graphs, certifiable estimation, SDP, optimization

{% include figure.html path="assets/img/certi-fgo.png" class="img-fluid rounded z-depth-1" %}

> **What this post is about**  
> The Certi FGO paper asks a simple question. Can we keep the usability and scalability of factor graphs while also gaining a reliable way to say that an answer is not just good, but truly the best possible answer. The main takeaway is that we can, as long as we lift the problem in a way that respects sparsity instead of collapsing everything into one huge dense optimization.

## Why this matters

Factor graphs are the standard tool for SLAM and state estimation because they naturally match how sensing works in robotics. Each measurement touches only a small part of the state, so each factor stays local, and the full problem ends up sparse even when the graph is very large. That sparsity is not just a mathematical detail, it is the reason we can solve problems with thousands or millions of variables using practical computation and memory.

At the same time, most of the solvers we rely on are local methods that behave well only when the landscape is kind. If the initialization is strong and the problem is well conditioned, local optimization is fast and accurate and usually good enough. But the situations where robotics gets interesting are exactly the situations where the landscape stops being kind, and local methods can converge to the wrong answer while still producing residuals that look plausible.

When that happens the system can fool itself, especially in cases with symmetries, ambiguous associations, weak excitation, or multi robot alignment where different configurations explain the data nearly equally well. A local solver can lock into a nearby stationary point and the rest of the pipeline may treat it as truth. This is why the paper pushes for a missing capability that is more than just a better optimizer.

The missing capability is a certificate that can be checked after the fact and trusted without hand waving. Instead of only returning an estimate, the backend returns an estimate plus a verifiable signal that this estimate is globally optimal for the stated problem. That signal is valuable because it can be used as a decision gate for downstream modules that need to know whether the map is trustworthy before planning, whether loop closures are consistent before accepting them, or whether a multi robot alignment step should be committed to the shared map.

## The usual route to certificates

A standard path to certifiability is to rewrite the estimation problem in a form that exposes its nonconvex structure, often as a quadratically constrained quadratic program. Then you build a convex relaxation of that problem as a semidefinite program. If the relaxation is tight, the solution of the semidefinite program encodes the global optimum of the original nonconvex problem, and the tightness itself provides the proof you wanted.

This is a clean story on paper, and it has led to a lot of insight in certifiable estimation. The catch is that generic semidefinite programming can be brutally expensive when the lifted matrix is large, because the lifted variable is a matrix whose size grows with the number of original variables. In robotics graphs that means the naive approach quickly becomes too large to be a practical backend.

So the real question is not whether semidefinite relaxations can certify things, because they can. The real question is whether we can get the same certification power without paying the dense cost that usually comes with lifting. In other words, can we keep the factor graph scaling story while still accessing the convex relaxation and its certificate.

## The key idea

The key insight in the paper is that lifting does not have to destroy structure if you do it with the factor graph in mind. The fear people often have is that once you lift, every variable interacts with every other variable, and sparsity disappears. But the factor graph tells you exactly which variables should interact, and the paper shows how to build the lifted representation so that the interaction pattern remains local.

Two ideas make this work. The first is Shor style lifting, which replaces products of variables with entries of a lifted matrix representation. The second is the Burer Monteiro factorization, which represents that lifted matrix as a low rank product, turning the convex semidefinite program into a structured nonconvex problem over a manifold.

What matters is that this nonconvex problem is not a random dense thing. It can be written as a lifted factor graph where each factor still involves only a small neighborhood, much like the original graph. The variables look different because they live on lifted manifolds, but the adjacency pattern still mirrors the original sensing pattern. This is the heart of why the approach can scale, because it preserves the same kind of locality that makes standard factor graph solvers efficient.

Once you accept that, the whole idea of certifiability shifts from being a separate solver stack to being something that can live inside the same graph based workflow. You can still talk about building factors, keeping sparsity, and running iterative optimization, while also keeping the door open to a global optimality certificate when the relaxation is tight.

## What the Certi FGO pipeline does

### Step 1 Build the lifted factor graph

You start from a standard estimation problem with poses and measurements, and you rewrite it into a quadratic form that is suitable for relaxation. Then you apply lifting so that the objective and constraints become linear in a lifted matrix variable. After that you apply a low rank factorization so that the lifted matrix is represented implicitly by smaller factors, which becomes the set of variables you actually optimize.

In many robotics problems, the rotation related parts of the state naturally map to orthonormality constraints, and in the lifted world those become blocks on Stiefel type manifolds. That sounds abstract, but the operational point is simple. Instead of optimizing directly over rotations and translations, you optimize over structured blocks that encode them in a way that lines up with the relaxed semidefinite program. Each factor in the graph becomes a lifted factor that still only touches the corresponding local blocks, so the graph remains sparse.

### Step 2 Optimize locally in the lifted space

Once the lifted graph is built, you run a local solver, but now it is a solver that respects the geometry of the lifted variables. The paper uses Riemannian optimization, which you can think of as a version of iterative descent or Gauss Newton that takes steps along the manifold rather than stepping through Euclidean space and projecting after the fact.

This step feels familiar if you have ever run a local optimizer on a factor graph, because you still accumulate local contributions and exploit sparsity. The difference is that the state lives on a product of manifolds defined by the lifted constraints, and the algorithm uses that structure to compute gradients, retractions, and updates in a consistent way. The benefit is that you are now searching in a space that is directly tied to the semidefinite relaxation, which is what makes certification possible afterward.

### Step 3 Certify

After you reach a stationary point in the lifted space, you compute a certificate object that tells you whether the point corresponds to a globally optimal solution of the original nonconvex problem. In practical terms this involves constructing a matrix whose positive semidefiniteness is the condition for global optimality under the relaxation. You then check its smallest eigenvalue, or an equivalent condition, to decide whether the certificate passes.

If the condition passes, you can report that the solution is globally optimal for the stated problem, not just locally consistent. If it fails, that does not automatically mean your solution is bad, but it means you do not have the proof. The failure could come from the relaxation not being tight at the chosen rank, or from the optimizer landing at a stationary point that does not correspond to the tight relaxed solution.

### Step 4 Increase rank and repeat using the Riemannian Staircase

If you do not get a certificate, the method gives you a principled way to try harder by increasing the rank in the Burer Monteiro factorization and continuing the optimization. This is the Riemannian Staircase idea. The intuition is that higher rank provides more expressive power, which can allow the method to reach a point that matches the tight semidefinite solution when such a tight solution exists.

This matters because it replaces a purely heuristic strategy like random restarts with something that is more structured. Instead of hoping that a different initialization finds the right basin, you expand the search space in a controlled way that is tied to the theoretical relaxation. In practice you still may need good numerics and good implementations, but the escalation mechanism is not arbitrary, and it gives you a clear knob to turn when certification fails.

{% include figure.html path="assets/img/Plaza2-CORA.gif" class="img-fluid rounded z-depth-1" %}

## What is the actual significance

One major takeaway is that certifiability can become a capability that fits into existing factor graph thinking. If your mental model is building a sparse graph, running inference, and shipping an estimate downstream, this work suggests you can keep that mental model and still add a trustworthy global optimality check. That is compelling because it lowers the barrier between theory and practice, and it makes certification feel like an interface you can call rather than an entirely separate research prototype.

Another takeaway is that structure is the whole scaling story, and the paper treats structure as the primary design constraint rather than an afterthought. The contribution is not only that lifting and low rank factorization work, but that they can be done in a way that respects the original interaction pattern. That is the difference between a method that works on toy graphs and a method that can plausibly compete with standard backends on real problems.

A third takeaway is that this creates a clean system behavior that is easy to reason about. You run estimation, then you ask whether the result is certified. If it is certified, you can proceed with higher confidence. If it is not certified, you can decide whether to escalate rank, adjust sensing assumptions, or trigger additional validation. Even when you do not get a certificate, you still get useful information because you learn that the problem instance may be ambiguous or that the relaxation is not tight under your current settings.

In autonomy settings where decisions are expensive or safety critical, that kind of explicit quality signal is valuable. It changes the conversation from trusting optimization because it usually works to trusting optimization because you can verify when it has truly succeeded. That is the difference between a backend that only produces numbers and a backend that produces numbers plus a guarantee when the math supports it.

{% include figure.html path="assets/img/plots.png" class="img-fluid rounded z-depth-1" %}

## Closing thought

What makes Certi FGO exciting is that it treats certifiability as a workflow feature that can integrate with the way roboticists already build and debug estimation systems. The story is that you do not need to abandon factor graphs to get global guarantees. You lift the problem carefully so that sparsity survives, you optimize efficiently in the lifted space, and when the relaxation is tight you get a checkable certificate that tells you the answer is globally optimal. That combination of practical structure and principled verification is exactly what makes the approach feel like a step toward estimation backends that are not only scalable, but also trustworthy.

{% include figure.html path="assets/img/icra.PNG" class="img-fluid rounded z-depth-1" %}

<iframe
  src="https://dartmouthrobotics.github.io/icra-2025-robots-wild/spotlight-papers/icra-2025-robots-wild-16.pdf"
  width="100%"
  height="650"
  style="border:1px solid #e5e7eb; border-radius:12px;"
  loading="lazy">
</iframe>
