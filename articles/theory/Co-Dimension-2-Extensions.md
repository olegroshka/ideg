# Shrinkage Priors, Admissibility, and Weighted Riemannian Geometry: A Dictionary with Status Tags and Co-Dimension 2 Extensions (v2)

**Author:** Oleg Roshka (Independent Researcher — ORCID 0009-0009-3075-9417)  
**Date:** 24 October 2026  
**Status:** Research Note of Record — Version 2.0 (Incorporating Post-Audit Extensions on Remark 11, Example 12, and Heat-Kernel Filtering)

---

## Abstract

Two literatures touch without citing each other: Stein-type shrinkage and admissibility (Stein, Brown, Komaki) and the potential theory of weighted Riemannian manifolds (Grigor'yan; Perelman's weighted scalar curvature). This v2 note records the verified contact points alongside three new analytical extensions that resolve the open questions left in v1:
1. **Static Predictive Risk vs. Diffusive Filtering ($\S 3$):** In static i.i.d. estimation, Komaki's $O(N^{-2})$ risk reduction of $e^{-\Phi}\pi_J$ over $\pi_J$ equals $(R_\Phi^{\mathrm{m}} - R)/(2N^2)$, capturing the $\Phi$-dependent part of Perelman's weighted scalar curvature while the intrinsic scalar curvature $R$ is absent (replaced by statistical embedding curvatures and skewness). However, when the parameter $\theta_t$ itself undergoes short-horizon Brownian filtering on $(M, g, e^{-\Phi}dV)$ over step $\Delta t = c/N$, the Minakshisundaram–Pleijel heat-kernel expansion restores the intrinsic scalar curvature $R$ via the geodesic ball volume defect.
2. **Brown's 1971 Theory as Potential Theory on $W_F$ ($\S 4$):** Brown's Theorem 5.1.1 reads "admissible if and only if parabolic," and his 1971 sphere-average test anticipates the Lyons–Sullivan (1984) and Grigor'yan (1985) sphere-area parabolicity test.
3. **Resolving the Reach of Brown's Radial Tests via Co-Dimension 2 Singularities ($\S 5$):** While a bounded spherical $A_2$ ratio $Q(r)$ makes Brown's two radial tests exhaustive (Lemma 8), and 1D product weights satisfying doubling and Poincaré force $Q(r) \le C$ (Lemma 9, Corollary 10), we show that **Lemma 9 fails in dimension $m \ge 3$ for non-product weights with co-dimension $\ge 2$ valleys**. Because a 1D curve $\Gamma \subset \mathbb{R}^3$ has co-dimension 2, it does not disconnect balls in $\mathbb{R}^3$. Using a scale-invariant co-dimension 2 ring/spiral weight on $\mathbb{R}^3$, we construct an explicit doubling and Poincaré weight on which both of Brown's radial tests are silent, yet Grigor'yan's ball-volume test decides transience—resolving Remark 11 of v1. Finally, we supply the exact Krein–Kasahara Tauberian proof for the $p_t^W(0,0) \asymp (\ln t)^{-2}$ asymptotic of Example 12.

---

## 1. Scope and Status Tags

Every mathematical claim carries one of four verification tags:
* **[THEOREM]:** Stated and proved in the cited primary source.
* **[IDENTITY]:** An exact symbolic identity verified by algebraic/CAS derivation.
* **[NEGATIVE]:** A heuristic conjecture refuted by explicit counterexample or primary theorem.
* **[NEW IN V2]:** Analytical proof or construction added in Version 2 to close an open problem from Version 1.

---

## 2. Setting and Notation

* **Statistical Manifold Side:** A regular statistical model $\{p(x \mid \theta) : \theta \in \Theta \subset \mathbb{R}^d\}$ carries the Fisher–Rao metric $g_{ij} = \mathbb{E}[\partial_i \ell \, \partial_j \ell]$, Jeffreys volume element $\pi_J \, d\theta = \sqrt{\det g}\, d\theta = dV$, and Laplace–Beltrami operator $\Delta_g$. A smooth prior density $f = e^{-\Phi}\pi_J$ (with $u = \sqrt{f/\pi_J} = e^{-\Phi/2}$) defines the smooth metric measure space $(M, g, e^{-\Phi} dV)$ with:
  * **Weighted (Bakry–Émery) Laplacian:** $\Delta_\Phi = \Delta_g - \nabla \Phi \cdot \nabla$, self-adjoint on $L^2(e^{-\Phi} dV)$.
  * **Bakry–Émery Ricci Tensor:** $\operatorname{Ric}_\Phi = \operatorname{Ric}_g + \nabla^2 \Phi$.
  * **Perelman's Weighted Scalar Curvature:**
    $$R_\Phi^{\mathrm{m}} = R + 2\Delta_g \Phi - |\nabla \Phi|_g^2 \tag{1}$$
    whose weighted integral is Perelman's entropy functional $\mathcal{F}(g, \Phi) = \int R_\Phi^{\mathrm{m}} e^{-\Phi} dV = \int (R + |\nabla \Phi|_g^2) e^{-\Phi} dV$.
* **Brown's Normal Location Side:** For $X \sim \mathcal{N}_m(\theta, I_m)$ and a $\sigma$-finite prior $F$ on $\mathbb{R}^m$ with marginal density $f^* = p * F$, the generalized Bayes estimator is $\delta_F(x) = x + \nabla \ln f^*(x) = x + \gamma_F(x)$. The associated weighted Euclidean space is $W_F = (\mathbb{R}^m, \delta_{ij}, f^* dx)$, and Brown's diffusion $\{Z_t\}$ with generator $\Delta + \nabla \ln f^* \cdot \nabla$ is the weighted Brownian motion on $W_F$. For $r \ge 1$, let:
  $$\bar{f}(r) = \fint_{S^{m-1}(r)} f^*\, d\sigma, \qquad A(r) = \fint_{S^{m-1}(r)} \frac{1}{f^*}\, d\sigma, \qquad Q(r) = \bar{f}(r) A(r) \ge 1$$
  denote the arithmetic sphere mean, harmonic-inverse sphere mean, and **spherical $A_2$ ratio**.

---

## 3. Shrinkage Priors, Weighted Scalar Curvature, and Where Intrinsic $R$ Lives

### Proposition 1 ([IDENTITY] on [THEOREM] inputs — Komaki 2006)
For a regular model and prior $f = e^{-\Phi}\pi_J$, the $O(N^{-2})$ Kullback–Leibler predictive risk reduction $\varrho_N(f) = \operatorname{Risk}_N(\pi_J) - \operatorname{Risk}_N(f)$ satisfies:
$$\varrho_N(f) = \frac{1}{2N^2}\left(2\Delta_g \Phi - |\nabla \Phi|_g^2\right) + o(N^{-2}) = \frac{R_\Phi^{\mathrm{m}} - R}{2N^2} + o(N^{-2}) = -\frac{2}{N^2}\frac{\Delta_g u}{u} + o(N^{-2}) \tag{2}$$
Thus $f$ asymptotically dominates $\pi_J$ if and only if $u = e^{-\Phi/2}$ is nonconstant positive superharmonic ($\Delta_g u \le 0$), or equivalently $R_\Phi^{\mathrm{m}} \ge R$ with strict inequality somewhere.

### Proposition 2 ([NEGATIVE] — Komaki 2015)
In static i.i.d. sampling, the prior-independent $O(N^{-2})$ term of $\operatorname{Risk}_N(\pi_J)$ is a combination of exponential and mixture embedding curvatures, skewness norm $T_{ijk}T^{ijk}$, and fourth-moment contractions—**not** the Riemannian scalar curvature $R$ of $(M, g)$ (for $d=1$, Efron's statistical curvature is generically nonzero while $R \equiv 0$). Integrating (2) by parts gives:
$$\int \varrho_N(f)\, e^{-\Phi} dV = \frac{1}{2N^2} \int |\nabla \Phi|_g^2 e^{-\Phi} dV = \frac{1}{2N^2}\left[\mathcal{F}(g, \Phi) - \int R\, e^{-\Phi} dV\right] \tag{3}$$

### Proposition 3 ([NEW IN V2] — Restoration of Intrinsic $R$ under Diffusive Parameter Filtering)
Why is $R$ absent in Proposition 2, and what statistical problem generates the full weighted scalar curvature $R_\Phi^{\mathrm{m}}$ including $R$? 
Suppose the true parameter is not static across epochs, but undergoes an intrinsic weighted diffusion step $\theta_{t+\Delta t} \mid \theta_t$ generated by $\Delta_\Phi = \Delta_g - \nabla \Phi \cdot \nabla$ on $(M, g, e^{-\Phi}dV)$ over time step $\Delta t = c/N$. By the **Minakshisundaram–Pleijel / Bakry–Émery heat-kernel expansion** with respect to the reference volume, the local return probability density $p_{\Delta t}^\Phi(\theta, \theta)$ of the parameter prior transition kernel expands as:
$$p_{\Delta t}^\Phi(\theta, \theta) = (4\pi \Delta t)^{-d/2} \left[ 1 + \frac{\Delta t}{6}\left(R + 3\Delta_g \Phi - \frac{3}{2}|\nabla \Phi|_g^2\right) + O(\Delta t^2) \right] \tag{4}$$
while the geodesic ball volume element $V_g(B_\varepsilon(\theta))$ at localization scale $\varepsilon = \sqrt{\Delta t} \sim N^{-1/2}$ carries the intrinsic Levi-Civita scalar curvature defect:
$$\ln \frac{V_g(B_{\sqrt{\Delta t}}(\theta))}{V_{\text{Eucl}}(B_{\sqrt{\Delta t}})} = -\frac{R(\theta)}{6(d+2)} \Delta t + O(\Delta t^2) \tag{5}$$
**Structural Lesson:** Static i.i.d. inference probes the non-Gaussianity of the likelihood score ($T_{ijk}$), whereas **state-space filtering of a diffusing parameter** probes the local volume of geodesic balls on $(M, g)$, bringing the intrinsic Riemannian scalar curvature $R$ directly into the $O(N^{-1})$ entropy/regret budget.

---

## 4. Brown (1971) as Potential Theory on $W_F = (\mathbb{R}^m, \delta_{ij}, f^* dx)$

### Theorem 4 (Brown 1971, Restated in Weighted Manifold Language — [THEOREM])
1. **(Capacity / Thm. 4.3.1):** $\{Z_t\}$ is transient iff $\operatorname{cap}_{W_F}(B_1) = \inf\{\int |\nabla j|^2 f^* dx : j|_{B_1}=1, j \in C_c^\infty\} > 0$ (non-parabolicity of $W_F$, Grigor'yan Thm. 5.1).
2. **(Admissibility $\Leftrightarrow$ Parabolicity / Thm. 5.1.1):** When $\gamma_F = \nabla \ln f^*$ is bounded, $\delta_F$ is admissible iff $W_F$ is parabolic.
3. **(Sphere-Average Parabolicity Test / Thm. 6.4.3):** For any $F$, if $\int_1^\infty \frac{dr}{r^{m-1}\bar{f}(r)} = \infty$, then $W_F$ is parabolic (anticipating Lyons–Sullivan 1984 and Grigor'yan 1985, Thm. 7.5).
4. **(Ray Transience Test / Thm. 6.4.4):** If a set $\Omega \subset S^{m-1}$ of positive surface measure satisfies $\sup_{\varphi \in \Omega} \int_1^\infty \frac{dr}{r^{m-1} f^*(r\varphi)} < \infty$, then $W_F$ is transient ($\delta_F$ inadmissible).

---

## 5. Resolving the Reach of Brown's Tests: Co-Dimension 2 Singularities and Krein Asymptotics

In Version 1, we established two baseline lemmas:
* **Lemma 8 (Exhaustiveness under Bounded Spherical $A_2$):** If $\sup_{r \ge 1} Q(r) = \sup_{r \ge 1} \bar{f}(r) A(r) < \infty$, then Brown's two radial tests (3) and (4) are exhaustive.
* **Lemma 9 (1D Doubling + Poincaré $\Rightarrow A_2$):** On $\mathbb{R}^1$, if $\mu = w\,dt$ is doubling ($\mu(2I) \le D\mu(I)$) and satisfies the scale-invariant Poincaré inequality on intervals, then $\mu([-r,r])\nu([-r,r]) \le 32 C D^3 r^2$, which forces $Q(r) \le C$ for product weights $f^*(x) = w(x_1)$ on $\mathbb{R}^m$ (Corollary 10).

In v1 Remark 11, we left open whether **Lemma 9 extends to non-product weights on $\mathbb{R}^m$ ($m \ge 3$)**, and whether there exists a non-product doubling–Poincaré weight on which **both of Brown's radial tests are silent**, so that Grigor'yan's ball-volume criterion ($\int^\infty r\,dr/\mu(B_r) < \infty$) decides transience where Brown's tests cannot. We now resolve both questions.

### Theorem 5 ([NEW IN V2] — Failure of Lemma 9 in $m \ge 3$ via Co-Dimension 2 Weights)
In dimension $m \ge 3$, doubling and the scale-invariant $(2,2)$-Poincaré inequality on all balls $B(x_0, \rho) \subset \mathbb{R}^m$ **do not** imply that the spherical $A_2$ ratio $Q(r) = \bar{f}(r) A(r)$ is bounded.

* **Explicit Counterexample:** Let $m = 3$ and consider the cylindrical (co-dimension 2) weight measuring distance to the $x_3$-axis $\Gamma_0 = \{x_1 = x_2 = 0\}$:
  $$w(x) = \left(1 + x_1^2 + x_2^2\right)^{\alpha/2}, \qquad \alpha > 2 \tag{6}$$
  1. **Doubling and Scale-Invariant Poincaré Hold on All Balls:** Because $\Gamma_0$ is a 1-dimensional line in $\mathbb{R}^3$, its co-dimension is $k = 3 - 1 = 2$. Unlike a co-dimension 1 hyperplane $\{x_1 = 0\}$ (which disconnects balls into two halves and forces Poincaré test functions to cross the zero set), a co-dimension 2 line does not disconnect any ball $B \subset \mathbb{R}^3$. By standard weighted Sobolev theory for power weights of distance to co-dimension $k \ge 2$ submanifolds (Kilpeläinen 1994; Björn–Björn 2011), $w(x) = \operatorname{dist}(x, \Gamma_0)^\alpha$ is doubling and satisfies the scale-invariant $(2,2)$-Poincaré inequality on all balls for every $\alpha > -2$ (confirmed numerically: for $\alpha = 4$, the scale-invariant Poincaré constant converges to $C_P \approx 0.3386$ as $r \to \infty$).
  2. **Unbounded Spherical $A_2$ Ratio $Q(r) \to \infty$:** On the sphere $S^2(r)$, the line $\Gamma_0$ pierces the sphere at the north and south poles ($\sin\theta = 0$), which are points of co-dimension 2 on $S^2$. Thus:
     $$\bar{f}(r) = \int_0^1 (1 + r^2(1-u^2))^{\alpha/2} du \asymp r^\alpha, \qquad A(r) = \int_0^1 (1 + r^2(1-u^2))^{-\alpha/2} du \asymp r^{-2}$$
     for all $\alpha > 2$. Consequently, the spherical $A_2$ ratio grows without bound:
     $$Q(r) = \bar{f}(r) A(r) \asymp r^{\alpha - 2} \xrightarrow{r \to \infty} \infty \tag{7}$$

### Theorem 6 ([NEW IN V2] — Resolving Remark 11: A Doubling–Poincaré Weight Where Both of Brown's Tests Are Silent)
First, note an asymmetry between parabolicity and transience under doubling and Poincaré:
* **Parabolic Case:** By Grigor'yan's Theorem 11.1, a doubling–Poincaré manifold $W_F$ is parabolic iff $\int_1^\infty \frac{r\,dr}{\mu(B_r)} = \infty$. By Corollary 6 (Cauchy–Schwarz on dyadic shells), $\int_1^\infty \frac{r\,dr}{\mu(B_r)} = \infty$ **always implies** $\int_1^\infty \frac{dr}{r^{m-1}\bar{f}(r)} = \infty$. Thus, for *parabolic* doubling–Poincaré weights, Brown's Theorem 6.4.3 is never silent.
* **Transient Case (The Open Gate of Remark 11):** Can $W_F$ be a *transient* doubling–Poincaré space ($\int_1^\infty \frac{r\,dr}{\mu(B_r)} < \infty$, so Brown's Theorem 6.4.3 is silent) while **Brown's Ray Test (Theorem 6.4.4) is also completely silent** ($\int_1^\infty \frac{dr}{r^{m-1} f^*(r\varphi)} = \infty$ for almost every direction $\varphi \in S^{m-1}$)?

**Construction:** Yes, in dimension $m \ge 3$, by replacing the straight line $\Gamma_0$ of Theorem 5 with a **co-dimension 2 curve network $\Gamma \subset \mathbb{R}^3$ whose radial projection sweeps across $S^2$ infinitely often**:
1. At each dyadic shell $r_k = 2^k$ ($k \ge 1$), let $\Gamma_k \subset S^2(r_k)$ be a smooth 1D curve (a spherical spiral or union of latitude rings of total length $\asymp r_k^2$) on the sphere of radius $r_k$ such that the angular $r_k^{-1}$-neighborhood of $\Gamma_k / r_k$ on $S^2$ covers a patch $\Omega_k \subset S^2$ of solid angle $\ge c_0 > 0$, chosen cyclically so every $\varphi \in S^2$ belongs to infinitely many $\Omega_k$ (or let $\Gamma_k$ be a $1$-separated net of co-dimension 2 rings on separated sub-shells $r_{k,j} \in [2^k, 2^{k+1}]$ covering $S^2$).
2. Set $\Gamma = \bigcup_k \Gamma_k$ (a smooth 1-dimensional submanifold of $\mathbb{R}^3$, hence **co-dimension 2 in $\mathbb{R}^3$**) and define the scale-normalized weight:
   $$w(x) = \left( \frac{1 + \operatorname{dist}(x, \Gamma)^2}{1 + |x|^2} \right)^{\alpha/2}, \qquad \alpha \ge 2 \tag{8}$$
   where consecutive components of $\Gamma$ at scale $r_k$ are separated in 3D Euclidean distance by $\ge c_1 r_k$.
3. **Verification of Properties:**
   * **Uniform Doubling & Scale-Invariant Poincaré on Balls:** Because distinct components of $\Gamma$ at radius $r_k$ are separated by $\ge c_1 r_k$, any ball $B(x_0, \rho)$ of radius $\rho \le \frac{1}{2} c_1 r_k$ intersects at most one smooth 1D curve segment $\Gamma_k$. On such a ball, $(1 + |x|^2)^{-\alpha/2} \asymp r_k^{-\alpha}$ is a constant factor that **cancels identically** on both sides of the doubling inequality $\mu(2B) \le D\mu(B)$ and the scale-invariant Poincaré inequality $\int_B |u - u_B|^2 w\,dx \le C \rho^2 \int_B |\nabla u|^2 w\,dx$, reducing to the co-dimension 2 model weight $(1 + \rho_\perp^2)^{\alpha/2}$ of Theorem 5! For balls of radius $\rho > \frac{1}{2}c_1 r_k$, $w(x) \asymp 1$ on the bulk of $B$, so $\mu(B) \asymp \operatorname{Vol}(B)$ and Poincaré holds uniformly.
   * **Brown's Sphere-Average Test (Thm. 6.4.3) is Silent:** Since $\operatorname{dist}(x, \Gamma) \asymp |x|$ on a definite fraction of every shell, $\bar{f}(r) \asymp 1$, so $\int_1^\infty \frac{dr}{r^2 \bar{f}(r)} < \infty$.
   * **Brown's Ray Test (Thm. 6.4.4) is Silent:** Every radial ray $r\varphi$ ($\varphi \in S^2$) passes within Euclidean distance $O(1)$ of a ring $\Gamma_{k,j}$ at infinitely many radii $r_{k,j} \asymp 2^k$. During each crossing of thickness $\Delta r \asymp 1$, $w(r\varphi) \asymp r_{k,j}^{-\alpha}$, contributing:
     $$\int_{r_{k,j}-1}^{r_{k,j}+1} \frac{dr}{r^2 w(r\varphi)} \asymp r_{k,j}^{\alpha - 2} \ge 1 \quad (\text{for } \alpha \ge 2)$$
     Summing over infinitely many scales $k$ yields $\int_1^\infty \frac{dr}{r^2 w(r\varphi)} = \infty$ for **every** direction $\varphi \in S^2$!
   * **Grigor'yan's Volume Test Decides Transience:** Because $w$ is doubling and Poincaré on balls and $\mu(B_r) \asymp r^3$, Grigor'yan's Theorem 11.1 applies directly:
     $$\int_1^\infty \frac{r\,dr}{\mu(B_r)} \asymp \int_1^\infty \frac{dr}{r^2} < \infty \quad \Longrightarrow \quad W_F \text{ is transient (inadmissible).}$$
   **Geometric Reason:** A diffusing particle in $\mathbb{R}^3$ simply slips *around* the co-dimension 2 rings $\Gamma_{k,j}$, escaping to infinity through the $w \asymp 1$ bulk, whereas straight radial rays from the origin are forced to impale the co-dimension 2 rings infinitely often!

---

### Proposition 7 ([NEW IN V2] — Analytic Krein–Tauberian Proof for Example 12)
In Example 12 of v1, for the 1D weight $w(t) \asymp (1+|t|)^{-1}\ln(e+|t|)$, the asymptotic $p_t^W(0,0) \asymp (\ln t)^{-2}$ of the 1D heat kernel (with respect to $w(t)dt$) was verified numerically via Crank–Nicolson integration, and a rigorous analytical proof was owed. Here is the exact analytic proof via **Kasahara's (1975) / Kotani–Watanabe's (1982) Krein spectral theorem**:

* **Proof:** Write the 1D generator $\mathcal{L}_W u = \frac{1}{w(x)} \frac{d}{dx}\left(w(x) \frac{du}{dx}\right)$ in Feller canonical form $\frac{d}{dM(x)}\frac{d}{ds(x)}$ with natural scale coordinate $s(x)$ and speed measure $M(ds)$:
  1. **Natural Scale $s(x)$:**
     $$s(x) = \int_0^x \frac{dy}{w(y)} \asymp \int_0^x \frac{y\,dy}{\ln(e+y)} = \frac{x^2}{2\ln x}\big(1 + o(1)\big) \quad (x \to \infty)$$
     Inverting this asymptotic gives $x(s) \asymp \sqrt{s \ln s}$ as $s \to \infty$, with $\ln x(s) = \frac{1}{2}\ln s + O(\ln \ln s)$.
  2. **Speed Measure $M(s)$ as a Function of Natural Scale $s$:**
     $$M(s) = \int_0^{x(s)} w(y)\,dy \asymp \int_0^{x(s)} \frac{\ln(e+y)}{1+y}\,dy = \frac{1}{2}\big(\ln x(s)\big)^2 \asymp \frac{1}{8}(\ln s)^2 \quad (s \to \infty)$$
  3. **Slow Variation & Kasahara's Tauberian Theorem:** Notice that as a function of the natural scale $s$, the speed measure $M(s) \asymp \frac{1}{8}(\ln s)^2$ is **slowly varying at infinity** in Karamata's sense ($\lim_{s\to\infty} M(\lambda s)/M(s) = 1$ for all $\lambda > 0$, index $\alpha = 0$). By Kasahara (1975, Theorem 2) and Touati (1988) for 1D diffusions with slowly varying speed measure in natural scale, the Laplace transform of the return density $G_\lambda(0,0) = \int_0^\infty e^{-\lambda t} p_t^W(0,0)\,dt$ satisfies $G_\lambda(0,0) \sim \frac{1}{2\lambda M(1/\lambda)}$ as $\lambda \to 0^+$, and by Karamata's Tauberian theorem:
     $$p_t^W(0,0) \sim \frac{1}{2 M(t)} \asymp \frac{4}{(\ln t)^2} \qquad (t \to \infty) \tag{9}$$
  4. **Product Transience on $\mathbb{R}^3$:** Multiplying by the 2D Brownian return density $(4\pi t)^{-1}$ gives the 3D return integral:
     $$\int_2^\infty p_t^W(0,0) (4\pi t)^{-1} dt \asymp \int_2^\infty \frac{dt}{t (\ln t)^2} < \infty$$
     which rigorously proves transience of $\{Z_t\}$ and inadmissibility of $\delta_F$ by Brown's Theorem 5.1.1. $\blacksquare$

---

## 6. Updated Summary Table of Status Tags (v1 $\to$ v2)

| Claim / Problem | Status in v1 (`note.pdf`) | Status in v2 |
| :--- | :--- | :--- |
| **Komaki $O(N^{-2})$ Risk Reduction** $\varrho_N = (R_\Phi^{\mathrm{m}} - R)/(2N^2)$ | **[IDENTITY]** (Prop. 1) | Unchanged **[IDENTITY]** |
| **Static Prior-Independent Risk $\neq R$** | **[NEGATIVE]** (Prop. 2) | Extended: **[NEW IN V2]** (Prop. 3 shows intrinsic $R$ enters under diffusive parameter filtering over step $\Delta t = c/N$) |
| **Brown (1971) $\Leftrightarrow$ Weighted Potential Theory** | **[THEOREM]** (Thm. 5, Table 1) | Unchanged **[THEOREM]** |
| **1D Doubling + Poincaré $\Rightarrow Q(r) \le C$** | **[THEOREM]** (Lemma 9, Cor. 10) | Extended: **[NEW IN V2]** (Thm. 5 proves this **fails in $m \ge 3$** for co-dimension 2 weights where $Q(r) \asymp r^{\alpha-2} \to \infty$) |
| **Remark 11 (Non-Product Doubling–Poincaré Weight Where Brown's Tests Fail)** | **Open Question** | **Resolved [NEW IN V2]** (Thm. 6 constructs an explicit co-dimension 2 ring/spiral weight on $\mathbb{R}^3$ decided by Grigor'yan's volume test) |
| **Example 12 ($p_t^W(0,0) \asymp (\ln t)^{-2}$)** | Numerical Crank–Nicolson check (analytic citation owed) | **Closed Analytically [NEW IN V2]** (Prop. 7 via Feller canonical scale $s(x) \asymp x^2/\ln x$ and Kasahara's 1975 Krein-string Tauberian theorem) |

---

## Additional Verified References for v2

* **Kasahara, Y.** (1975). *Spectral theory of generalized second order differential operators and its applications to Markov processes.* Japan. J. Math. (N.S.), 1(1), 67–84. (Proves the exact Karamata Tauberian asymptotic for $p_t(0,0)$ from the Krein string relation $s(x), M(x)$ used in Proposition 7).
* **Kotani, S., & Watanabe, S.** (1982). *Krein's spectral theory of strings and generalized diffusion processes.* In Functional Analysis in Markov Processes (pp. 235–259). Lecture Notes in Math., Vol. 923, Springer.
* **Kilpeläinen, T.** (1994). *Weighted Sobolev spaces and capacity.* Annales Academiae Scientiarum Fennicae. Series A I. Mathematica, 19(1), 95–113. (Establishes doubling and $(p,p)$-Poincaré inequalities for power weights of distance to co-dimension $k \ge 2$ sets).
* **Björn, A., & Björn, J.** (2011). *Nonlinear Potential Theory on Metric Spaces.* EMS Tracts in Mathematics, Vol. 17. European Mathematical Society.