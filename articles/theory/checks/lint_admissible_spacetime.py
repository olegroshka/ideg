#!/usr/bin/env python
"""
AR-024 equation lint for
  articles/theory/admissible_spacetime_and_statistical_general_relativity.md

Every displayed equation in the article that is mechanically checkable is
re-derived here from scratch (sympy for identities, numpy Monte Carlo for
risk claims). Curvature tensors are computed from the metric components;
nothing is quoted from a textbook formula.

Run (the Windows console is cp1252, so force UTF-8 or keep ASCII):
    PYTHONIOENCODING=utf-8 python lint_admissible_spacetime.py

Output tags: PASS = article's equation reproduced; FAIL = article's
equation contradicted; INFO = context or a conceptual point made precise.
ASCII-only output on purpose.
"""
import sympy as sp
import numpy as np

RESULTS = []


def report(tag, name, ok=None, detail=""):
    status = {True: "PASS", False: "FAIL", None: "INFO"}[ok]
    RESULTS.append((tag, status, name))
    print(f"[{tag}] {status}: {name}")
    for line in detail.strip("\n").splitlines():
        print("        " + line)
    print()


# ---------------------------------------------------------------------------
# Coordinate tensor helpers (generic metric, no assumptions)
# Riemann convention:  R^r_{s mu nu} = d_mu G^r_{nu s} - d_nu G^r_{mu s}
#                                     + G^r_{mu l} G^l_{nu s} - G^r_{nu l} G^l_{mu s}
# Ricci:               R_{s nu} = R^r_{s r nu}
# With this convention the unit sphere has R_ij = +g_ij (checked in C16).
# ---------------------------------------------------------------------------
def christoffel(g, xs):
    n = len(xs)
    ginv = g.inv()
    return [[[sp.simplify(sum(ginv[k, l] * (sp.diff(g[j, l], xs[i]) + sp.diff(g[i, l], xs[j])
                                            - sp.diff(g[i, j], xs[l])) for l in range(n)) / 2)
              for j in range(n)] for i in range(n)] for k in range(n)]


def ricci(g, xs, G):
    n = len(xs)
    R = sp.zeros(n, n)
    for s in range(n):
        for nu in range(n):
            val = 0
            for r in range(n):
                val += sp.diff(G[r][nu][s], xs[r]) - sp.diff(G[r][r][s], xs[nu])
                for l in range(n):
                    val += G[r][r][l] * G[l][nu][s] - G[r][nu][l] * G[l][r][s]
            R[s, nu] = sp.simplify(val)
    return R


def hessian_cov(f, xs, G):
    n = len(xs)
    return sp.Matrix(n, n, lambda i, j: sp.diff(f, xs[i], xs[j])
                     - sum(G[k][i][j] * sp.diff(f, xs[k]) for k in range(n)))


def div_sym2(T_up, xs, G):
    """covariant divergence nabla_j T^{ij} of a symmetric (2,0) tensor"""
    n = len(xs)
    return sp.Matrix(n, 1, lambda i, _: sum(sp.diff(T_up[i, j], xs[j]) for j in range(n))
                     + sum(G[i][j][k] * T_up[k, j] for j in range(n) for k in range(n))
                     + sum(G[j][j][k] * T_up[i, k] for j in range(n) for k in range(n)))


# ===========================================================================
print("=" * 78)
print("AR-024 EQUATION LINT -- admissible_spacetime_and_statistical_general_relativity.md")
print("=" * 78 + "\n")

# ---- C1: Weyl tensor component count (Part II, 2.1) ------------------------
rows = []
all_ok = True
for d in range(1, 7):
    D = d + 1
    art = sp.Rational((d + 1) * d * (d - 1) * (d - 2), 12)
    std = sp.Rational(D * (D + 1) * (D + 2) * (D - 3), 12) if D >= 3 else sp.Integer(0)
    rows.append(f"d={d} (D={D}): article formula -> {str(art):>3},  standard D(D+1)(D+2)(D-3)/12 -> {str(std):>3}")
    if d >= 2 and art != std:
        all_ok = False
report("C1", "Weyl components N(d) = (d+1)d(d-1)(d-2)/12 with N(3)=10", all_ok,
       "\n".join(rows) + "\nArticle's own formula gives N(3)=2, not the 10 it states; the\n"
       "qualitative claim (N=0 at d=2, N>0 for d>=3) survives, the formula does not.")

# ---- C5: E||X||^2 = ||theta||^2 + d  (Part II, 2.2) -------------------------
th, z = sp.symbols('theta z', real=True)
E_Xi2 = sp.integrate((th + z) ** 2 * sp.exp(-z ** 2 / 2) / sp.sqrt(2 * sp.pi), (z, -sp.oo, sp.oo))
report("C5", "E||X||^2 = ||theta||^2 + d for X ~ N(theta, I_d)", sp.simplify(E_Xi2 - (th ** 2 + 1)) == 0,
       f"per coordinate E[X_i^2] = {sp.simplify(E_Xi2)}; summing d coordinates gives ||theta||^2 + d.")

# ---- C6: Bessel radial drift (d-1)/(2R)  (Part II, 2.2) --------------------
rows = []
ok = True
for n in (2, 3, 4, 5):
    xs = sp.symbols(f'x1:{n+1}', real=True)
    r = sp.sqrt(sum(v ** 2 for v in xs))
    lap_r = sp.simplify(sum(sp.diff(r, v, 2) for v in xs))
    drift = sp.simplify(lap_r / 2)          # Ito: d r(X) has drift (1/2) Laplacian r
    target = sp.Rational(n - 1, 2) / r
    ok &= sp.simplify(drift - target) == 0
    rows.append(f"d={n}: (1/2) Lap|x| = {drift}")
report("C6", "radial Ito drift dR = dW + (d-1)/(2R) dt", ok, "\n".join(rows))

# ---- C7: Green's function r^{2-d} harmonic for d>=3, ln r for d=2 ----------
rows = []
ok = True
for n in (3, 4, 5):
    xs = sp.symbols(f'x1:{n+1}', real=True)
    r = sp.sqrt(sum(v ** 2 for v in xs))
    lap = sp.simplify(sum(sp.diff(r ** (2 - n), v, 2) for v in xs))
    ok &= lap == 0
    rows.append(f"d={n}: Lap r^(2-d) = {lap}")
x1, x2 = sp.symbols('x1 x2', real=True)
lnr = sp.log(sp.sqrt(x1 ** 2 + x2 ** 2))
lap2 = sp.simplify(sp.diff(lnr, x1, 2) + sp.diff(lnr, x2, 2))
ok &= lap2 == 0
rows.append(f"d=2: Lap ln r = {lap2}")
report("C7", "Phi_Green ~ 1/r^(d-2) is harmonic off the origin (d>=3); ln r in d=2", ok, "\n".join(rows))

# ---- C8: the real kernel: 2 Lap Phi - |grad Phi|^2 = -4 Lap(e^{-Phi/2}) / e^{-Phi/2} ----
xs = sp.symbols('x1:4', real=True)
Phi = sp.Function('Phi')(*xs)
lapPhi = sum(sp.diff(Phi, v, 2) for v in xs)
gradPhi2 = sum(sp.diff(Phi, v) ** 2 for v in xs)
sqrt_psi = sp.exp(-Phi / 2)
lhs = 2 * lapPhi - gradPhi2
rhs = -4 * sum(sp.diff(sqrt_psi, v, 2) for v in xs) / sqrt_psi
report("C8", "Komaki-form integrand 2 Lap Phi - |dPhi|^2 == -4 Lap(sqrt psi)/sqrt psi, psi = e^{-Phi}",
       sp.simplify(lhs - rhs) == 0,
       "So '2 Lap Phi - |dPhi|^2 >= 0' is exactly 'sqrt(psi) superharmonic': the George-Liang-Xu /\n"
       "Komaki sufficient condition, and the Stein (1981) 4 Lap sqrt(m)/sqrt(m) risk term, in one line.\n"
       "This identity is the article's genuine kernel (flat-metric check; the Laplace-Beltrami\n"
       "version is the same computation with Lap_g).")

# ---- C10: SIGN of the Phi-dependent risk term, against Komaki (2006) eq. (3)-(5) ----
# Komaki, Ann. Statist. 34(2) 808-819, eq. (3) (flat model, skewness T_i = 0 for the normal family):
#   Risk(p_f) = d/(2N) + (1/(2N^2)) g^{ij} d_i log(f/pi_J) d_j log(f/pi_J)
#               + (1/N^2) Lap log(f/pi_J) + (terms independent of f) + o(N^-2)
# and eq. (4)-(5): Risk(pi_J) - Risk(f) = (1/(2N^2))|d log(f/pi_J)|^2 - (1/N^2)(pi_J/f) Lap(f/pi_J) + o(N^-2).
# Article (Formalism 1, 1.2) writes  Risk = d/(2N) + (1/(2N^2))[K_curv + 2 Lap Phi - |dPhi|^2]  with f/pi_J = e^{-Phi}.
xs = sp.symbols('x1:4', real=True)
Phi = sp.Function('Phi')(*xs)
Nn = sp.symbols('N', positive=True)
logpsi = -Phi
lap = lambda F: sum(sp.diff(F, v, 2) for v in xs)
grad2 = lambda F: sum(sp.diff(F, v) ** 2 for v in xs)
komaki_phi_part = sp.Rational(1, 2) / Nn ** 2 * grad2(logpsi) + lap(logpsi) / Nn ** 2        # from eq. (3)
komaki_diff = sp.Rational(1, 2) / Nn ** 2 * grad2(logpsi) - sp.exp(Phi) * lap(sp.exp(-Phi)) / Nn ** 2   # eq. (4)-(5): Risk(pi_J)-Risk(f)
article_phi_part = sp.Rational(1, 2) / Nn ** 2 * (2 * lap(Phi) - grad2(Phi))
consistent_eq3_eq5 = sp.simplify(komaki_phi_part + komaki_diff) == 0            # eq.(3) Phi-part == -(Risk(pi_J)-Risk(f))
article_matches_komaki = sp.simplify(article_phi_part - komaki_phi_part) == 0
article_matches_minus = sp.simplify(article_phi_part + komaki_phi_part) == 0
report("C10", "Komaki risk expansion: Risk = d/2N + (1/2N^2)[K + 2 Lap Phi - |dPhi|^2] (article's sign)",
       bool(article_matches_komaki),
       f"Komaki eq.(3) Phi-dependent part (flat, T=0): {sp.simplify(komaki_phi_part)}\n"
       f"Komaki eq.(3) and eq.(4)-(5) mutually consistent: {consistent_eq3_eq5}\n"
       f"article's Phi-part equals Komaki's: {article_matches_komaki};  equals MINUS Komaki's: {article_matches_minus}\n"
       "So the article has the sign of the shrinkage term reversed: by Komaki (4)-(5),\n"
       "  Risk(f) = Risk(pi_J) - (1/(2N^2)) [2 Lap Phi - |dPhi|^2] + o(N^-2),\n"
       "i.e. a superharmonic sqrt(psi) LOWERS the risk (Komaki Thm 2). With the correct sign the integrated\n"
       "functional is  Int (K - |dPhi|^2) e^-Phi dV  after the C9 integration by parts: the gradient term enters\n"
       "with the OPPOSITE sign to Perelman's F = Int (R + |df|^2) e^-f dV. The 'mathematically identical to\n"
       "Perelman's F' claim fails at the sign level, and the 'K_curv proportional to scalar curvature' term is\n"
       "not stated in Komaki (2006), whose f-independent terms are left unspecified.\n"
       "VERIFIED against the source: Komaki's Section 3 conformal map  g~ = (h/pi_J)^{2/(d-2)} g  (d > 2) is\n"
       "exactly the article's Einstein-frame rescaling with h/pi_J = e^-Phi -- that part of the kernel is real.")

# ---- C9 + C2: Perelman F and the conformal 'Einstein frame' ----------------
rows = []
ok_identity = True
ok_coeff_article = True
for n in (3, 4):
    xs = sp.symbols(f'x1:{n+1}', real=True)
    Phi = sp.Function('Phi')(*xs)
    w = -Phi / (n - 2)
    g = sp.eye(n) * sp.exp(2 * w)
    G = christoffel(g, xs)
    Ric = ricci(g, xs, G)
    ginv = g.inv()
    Rs = sp.simplify(sum(ginv[i, j] * Ric[i, j] for i in range(n) for j in range(n)))
    lapPhi = sum(sp.diff(Phi, v, 2) for v in xs)
    gradPhi2 = sum(sp.diff(Phi, v) ** 2 for v in xs)
    density = sp.simplify(Rs * sp.exp(n * w))                        # R~ sqrt(g~), flat background R=0
    pointwise = sp.exp(-Phi) * (sp.Rational(2 * (n - 1), n - 2) * lapPhi - sp.Rational(n - 1, n - 2) * gradPhi2)
    ok_identity &= sp.simplify(density - pointwise) == 0
    div_term = sum(sp.diff(sp.exp(-Phi) * sp.diff(Phi, v), v) for v in xs)
    ok_identity &= sp.simplify(div_term - sp.exp(-Phi) * (lapPhi - gradPhi2)) == 0
    # e^{-Phi}|dPhi|^2_g dV  ==  |dPhi|^2_{g~} dV~
    ok_identity &= sp.simplify(sp.exp(-2 * w) * gradPhi2 * sp.exp(n * w) - sp.exp(-Phi) * gradPhi2) == 0
    c_derived = sp.Rational(n - 1, n - 2) - 1
    c_article = sp.Rational(n - 1, n - 2)
    ok_coeff_article &= (c_derived == c_article)
    rows.append(f"n={n}: R~ sqrt(g~) = e^-Phi[2(n-1)/(n-2) LapPhi - (n-1)/(n-2)|dPhi|^2] (flat bg) -> holds")
    rows.append(f"      up to a divergence: F = Int[(R + |dPhi|^2) e^-Phi dV] = Int[ R~ - c |dPhi|^2_g~ ] dV~")
    rows.append(f"      derived c = {c_derived}   article c = (d-1)/(d-2) = {c_article}")
report("C9", "Int(R + 2LapPhi - |dPhi|^2)e^-Phi = Int(R + |dPhi|^2)e^-Phi = Perelman F (up to boundary)",
       ok_identity, "divergence identity div(e^-Phi dPhi) = e^-Phi(LapPhi - |dPhi|^2) verified for n=3,4.")
report("C2", "Einstein-frame kinetic coefficient (d-1)/(d-2) in S_Einstein", ok_coeff_article,
       "\n".join(rows) + "\nCorrect coefficient is 1/(d-2) (matches the string-frame dilaton result\n"
       "4/(D-2) after Phi = 2 phi). The exponent -2/(d-2) and 'singular at d=2' are right.")

# ---- C11: pullback metric expansion (Formalism 2, 2.3) ---------------------
s2 = sp.symbols('sigma2', positive=True)
h11, h12, h13, h22, h23, h33 = sp.symbols('h11 h12 h13 h22 h23 h33', real=True)
H = sp.Matrix([[h11, h12, h13], [h12, h22, h23], [h13, h23, h33]])   # Hessian of Phi (symmetric)
J = sp.eye(3) - s2 * H                                                 # J = I - grad(Sigma dPhi), Sigma = sigma^2 I
g_int = J.T * (sp.eye(3) / s2) * J
article = (sp.eye(3) - 2 * s2 * H + s2 ** 2 * H * H) / s2
report("C11", "g_int = (1/s^2)[delta - 2 s^2 HessPhi + s^4 (HessPhi)^2]", sp.simplify(g_int - article) == sp.zeros(3, 3),
       "J^T Sigma^-1 J expanded with a symmetric Hessian; matches the article.")

# ---- C12: Jacobian eigenvalues of Y = (1 - rS^2/r^2) x  (Formalism 2, 2.4) --
rS = sp.symbols('r_S', positive=True)
xs = sp.symbols('x y z', real=True)
r = sp.sqrt(sum(v ** 2 for v in xs))
Y = sp.Matrix([(1 - rS ** 2 / r ** 2) * v for v in xs])
Jm = Y.jacobian(sp.Matrix(xs))
xv = sp.Matrix(xs)
rad = sp.simplify((xv.T * Jm * xv)[0] / r ** 2)
tv = sp.Matrix([-xs[1], xs[0], 0])                                      # orthogonal to x
tan = sp.simplify((tv.T * Jm * tv)[0] / (tv.T * tv)[0])
ok = sp.simplify(rad - (1 + rS ** 2 / r ** 2)) == 0 and sp.simplify(tan - (1 - rS ** 2 / r ** 2)) == 0
report("C12", "Jacobian of the James-Stein map: radial 1 + rS^2/r^2, tangential 1 - rS^2/r^2", ok,
       f"radial eigenvalue = {rad}\ntangential eigenvalue = {tan}\n"
       "At r = rS the TANGENTIAL eigenvalue vanishes (angular metric degenerates) while the\n"
       "radial eigenvalue is 2 (g_rr = 4/sigma^2). Part VI step 4 says the RADIAL eigenvalue\n"
       "vanishes at the horizon -- inconsistent with the article's own Formalism 2.")

# ---- C3: 'Schwarzschild-like' g_rr from Y = (1 - rS/r) x ------------------
rr = sp.symbols('r', positive=True)
Yr = (1 - rS / rr) * rr
dYr = sp.simplify(sp.diff(Yr, rr))
claim_holds = sp.simplify(dYr ** 2 - 1 / (1 - rS / rr)) == 0
report("C3", "g_rr^cov ~ (1 - rS/r)^-1 from the harmonic-coordinate map Y = (1 - rS/r) x", claim_holds,
       f"Y_r = (1 - rS/r) r = {sp.simplify(Yr)},  dY_r/dr = {dYr}  =>  pullback g_rr = {sp.simplify(dYr**2)}/sigma^2 (flat).\n"
       "No (1 - rS/r)^-1 factor arises from the stated construction; the Schwarzschild form is asserted.")

# ---- C13: ADM extrinsic curvature with beta = -grad Phi --------------------
report("C13", "K_ij = Hess Phi when d_tau h = 0, N = 1, beta = -grad Phi", True,
       "K_ij = (1/2N)(d_tau h_ij - D_i beta_j - D_j beta_i) = -(1/2)(-2 D_i D_j Phi) = D_i D_j Phi. Correct.")

# ---- C14: Hamiltonian-constraint identification is NOT an identity ---------
a = sp.symbols('a', positive=True)
xs = sp.symbols('x y z', real=True)
r2 = sum(v ** 2 for v in xs)
Phi_c = a * r2 / 2
Hc = sp.hessian(Phi_c, xs)
K = Hc.trace()
K2_minus_KK = sp.simplify(K ** 2 - (Hc * Hc).trace())
komaki_form = sp.simplify(2 * K - sum(sp.diff(Phi_c, v) ** 2 for v in xs))
report("C14", "ADM 'R + K^2 - K_ij K^ij' identified with Komaki 'R + 2 Lap Phi - |dPhi|^2'", False,
       f"flat slice, Phi = a r^2/2:  K^2 - K_ij K^ij = {K2_minus_KK}   vs   2 Lap Phi - |dPhi|^2 = {komaki_form}\n"
       "Different degree in a and different r-dependence: the two expressions are not related by any\n"
       "identity (one is quadratic in second derivatives, the other linear in Lap Phi). Formalism 3's\n"
       "constraint identification is an analogy, not a derivation.")

# ---- C15: Bochner/Reilly integrated identity (flat case) -------------------
xs = sp.symbols('x y z', real=True)
Phi = sp.Function('Phi')(*xs)
Hm = sp.hessian(Phi, xs)
lapPhi = Hm.trace()
gradv = sp.Matrix([sp.diff(Phi, v) for v in xs])
vec = lapPhi * gradv - Hm * gradv
divv = sum(sp.diff(vec[i], xs[i]) for i in range(3))
report("C15", "Int (K^2 - K_ij K^ij) dV = Int Ric(dPhi,dPhi) dV (flat case: pure divergence)",
       sp.simplify(divv - (lapPhi ** 2 - (Hm * Hm).trace())) == 0,
       "Verified pointwise: (Lap Phi)^2 - |Hess Phi|^2 = div(Lap Phi dPhi - Hess Phi . dPhi) when Ric = 0.\n"
       "The article's integrated Bochner statement is correct; it does not rescue C14, because the\n"
       "integrand it produces (R + Ric(dPhi,dPhi), unweighted) is still not the e^-Phi-weighted Komaki one.")

# ---- C16: momentum-constraint Ricci identity sign, on the unit 2-sphere ----
th_, ph_ = sp.symbols('theta phi', real=True)
xs = (th_, ph_)
g = sp.Matrix([[1, 0], [0, sp.sin(th_) ** 2]])
G = christoffel(g, xs)
Ric = ricci(g, xs, G)
convention_ok = sp.simplify(Ric - g) == sp.zeros(2, 2)          # unit S^2: Ric = +g in this convention
f = sp.Function('f')(th_, ph_)
Hcov = hessian_cov(f, xs, G)
ginv = g.inv()
T_up = ginv * Hcov * ginv                                           # (Hess f)^{ij}
lapf = sp.simplify((ginv * Hcov).trace())
lhs = sp.simplify(div_sym2(T_up, xs, G) - ginv * sp.Matrix([sp.diff(lapf, v) for v in xs]))   # D_j(D^i D^j f - g^{ij} Lap f)
rhs = sp.simplify(ginv * Ric * ginv * sp.Matrix([sp.diff(f, v) for v in xs]))                 # R^{ij} D_j f
sign_plus = sp.simplify(lhs - rhs) == sp.zeros(2, 1)
sign_minus = sp.simplify(lhs + rhs) == sp.zeros(2, 1)
report("C16", "Momentum constraint: D_j(D^i D^j Phi - h^ij Lap Phi) = -R^ij D_j Phi (article's sign)",
       bool(sign_minus and not sign_plus),
       f"Riemann convention check (unit S^2 has Ric = +g): {convention_ok}\n"
       f"D_j(D^i D^j f - g^ij Lap f) == +R^ij D_j f : {sign_plus}\n"
       f"D_j(D^i D^j f - g^ij Lap f) == -R^ij D_j f : {sign_minus}\n"
       "With the standard (positive-curvature-sphere) convention the sign is PLUS. The article's minus is\n"
       "a convention-level error; it inverts the direction of the claimed 'information momentum flux'.")

# ---- C20: Tweedie's formula, Gaussian-Gaussian case (1-D) ------------------
x, mu, tau, sg = sp.symbols('x mu tau sigma', real=True, positive=True)
m = sp.exp(-(x - mu) ** 2 / (2 * (sg ** 2 + tau ** 2))) / sp.sqrt(2 * sp.pi * (sg ** 2 + tau ** 2))
tweedie = x + sg ** 2 * sp.diff(sp.log(m), x)
post_mean = (tau ** 2 * x + sg ** 2 * mu) / (tau ** 2 + sg ** 2)
report("C20", "Tweedie: E[theta|X] = X + Sigma grad ln m(X)", sp.simplify(tweedie - post_mean) == 0,
       "Gaussian prior N(mu, tau^2), noise N(0, sigma^2): the formula reproduces the posterior mean.")

# ---- C21: Stein's identity E[(X - theta) f(X)] = sigma^2 E[f'(X)] (1-D) ---
zz = sp.symbols('z', real=True)
ok = True
for fexpr in (zz ** 2, zz ** 3, sp.sin(zz)):
    Xv = th + sg * zz
    lhs_e = sp.integrate((Xv - th) * fexpr.subs(zz, Xv) * sp.exp(-zz ** 2 / 2) / sp.sqrt(2 * sp.pi), (zz, -sp.oo, sp.oo))
    rhs_e = sg ** 2 * sp.integrate(sp.diff(fexpr, zz).subs(zz, Xv) * sp.exp(-zz ** 2 / 2) / sp.sqrt(2 * sp.pi), (zz, -sp.oo, sp.oo))
    ok &= sp.simplify(lhs_e - rhs_e) == 0
report("C21", "Stein's identity E[(X_i - theta_i) f(X)] = Sigma_ij E[d_j f]", ok,
       "checked for f = x^2, x^3, sin x with X ~ N(theta, sigma^2).")

# ---- C4 / C23: Monte Carlo risk of MLE, JS, JS+ (Part II 2.1, Part VI) -----
rng = np.random.default_rng(20261023)
nsamp = 400_000
rows = []
for d in (1, 2, 3, 5, 10):
    for theta_norm in (0.0, 2.0):
        theta = np.zeros(d)
        theta[0] = theta_norm
        X = theta + rng.standard_normal((nsamp, d))
        n2 = np.sum(X ** 2, axis=1)
        risk_mle = np.mean(np.sum((X - theta) ** 2, axis=1))
        fac = 1 - (d - 2) / n2
        risk_js = np.mean(np.sum((fac[:, None] * X - theta) ** 2, axis=1))
        risk_jsp = np.mean(np.sum((np.maximum(fac, 0)[:, None] * X - theta) ** 2, axis=1))
        note = "   <- textbook: exactly 2 for d>=3" if (d >= 3 and theta_norm == 0) else ""
        rows.append(f"d={d:>2} |theta|={theta_norm:.0f}: R(MLE)={risk_mle:6.3f}  R(JS)={risk_js:11.3f}  R(JS+)={risk_jsp:6.3f}{note}")
report("C4", "James-Stein dominates MLE for d>=3 (R(JS) = d - (d-2)^2 E[1/|X|^2] < d); JS+ dominates JS", None,
       "\n".join(rows) + "\n"
       "Monte Carlo, 4e5 samples. d>=3: JS and JS+ beat MLE at every theta tested, JS+ <= JS (Baranchik).\n"
       "d=1: the (d-2) factor is negative and E[1/X^2] is infinite -- the formula is meaningless there.\n"
       "d=2: factor is 0, JS == MLE.  The per-step risk GAP is bounded (at most d-2); Part VI's\n"
       "'cumulative KL risk diverges linearly' is a bounded constant gap per step, i.e. strict domination,\n"
       "not an instability. R(JS, theta=0) = 2 for all d>=3 is the textbook value and is reproduced.")

# ---- A1: the dimension in Stein's theorem is PARAMETER dimension -----------
X3 = rng.standard_normal((nsamp, 3))            # three independent 1-D 'particles', theta = 0
n2 = np.sum(X3 ** 2, axis=1)
risk_js_3x1 = np.mean(np.sum(((1 - 1 / n2)[:, None] * X3) ** 2, axis=1))
report("A1", "Stein threshold is on the number of jointly estimated parameters, not on spatial dimension", None,
       f"Three particles in ONE spatial dimension (parameter dim = 3): R(JS) = {risk_js_3x1:.3f} < 3 = R(MLE).\n"
       "Any realistic observer estimates K*d >> 3 parameters, so inadmissibility of the flat estimator\n"
       "holds in every spatial dimension d >= 1. The 'd >= 3 coincidence' with Weyl curvature requires the\n"
       "unstated modeling assumption 'one particle, position only'. Adversarial checklist items 2 and 13.")

# ---- C22: the owner's 'horn' visual -- Fisher geometry of the Gaussian location-scale family ----
# (from the 2026-10-23 side exchange: ds^2 = (d sigma^2 + |d mu|^2)/sigma^2, 'constant negative curvature',
#  horn = surface of revolution about the precision axis u = -ln sigma)
mu_, xx = sp.symbols('mu x', real=True)
sg_ = sp.symbols('sigma', positive=True)
logp = -sp.log(sg_) - (xx - mu_) ** 2 / (2 * sg_ ** 2) - sp.log(sp.sqrt(2 * sp.pi))
pdf = sp.exp(logp)
params = (mu_, sg_)
gF = sp.Matrix(2, 2, lambda i, j: sp.simplify(sp.integrate(sp.diff(logp, params[i]) * sp.diff(logp, params[j]) * pdf,
                                                            (xx, -sp.oo, sp.oo))))
E_, G_ = gF[0, 0], gF[1, 1]
# Gaussian curvature of an orthogonal metric E du^2 + G dv^2:
#   K = -1/(2 sqrt(EG)) [ d_u( G_u / sqrt(EG) ) + d_v( E_v / sqrt(EG) ) ]
u_, v_ = mu_, sg_
K_fisher = sp.simplify(-1 / (2 * sp.sqrt(E_ * G_)) * (sp.diff(sp.diff(G_, u_) / sp.sqrt(E_ * G_), u_)
                                                     + sp.diff(sp.diff(E_, v_) / sp.sqrt(E_ * G_), v_)))
# the pasted formula (no factor 2 on d sigma^2)
E2, G2 = 1 / sg_ ** 2, 1 / sg_ ** 2
K_pasted = sp.simplify(-1 / (2 * sp.sqrt(E2 * G2)) * (sp.diff(sp.diff(G2, u_) / sp.sqrt(E2 * G2), u_)
                                                     + sp.diff(sp.diff(E2, v_) / sp.sqrt(E2 * G2), v_)))
report("C22", "Horn visual: Fisher metric of N(mu, sigma^2) is hyperbolic; location family alone is flat", None,
       f"Fisher metric of N(mu, sigma^2): g = diag({gF[0,0]}, {gF[1,1]})  (off-diagonal {gF[0,1]})\n"
       f"  => ds^2 = (d mu^2 + 2 d sigma^2)/sigma^2, Gaussian curvature K = {K_fisher} (constant, negative).\n"
       f"  The pasted ds^2 = (d sigma^2 + d mu^2)/sigma^2 omits the factor 2 and has K = {K_pasted}.\n"
       "  The horn (pseudosphere / cusp) is a legitimate picture of THIS manifold: thin throat = sigma -> inf\n"
       "  (zero precision), flare = high precision; the axial coordinate u = -ln sigma ~ (1/2) ln N is a clock\n"
       "  given by the observation count -- an EXTERNAL clock (NC-010), made visible by the picture.\n"
       "  But the article's Stein setting X ~ N(theta, I_d) has sigma KNOWN: its Fisher manifold is the flat\n"
       "  location family (g = I/sigma^2, K = 0). The article's curvature comes from the prior Phi\n"
       "  (Bakry-Emery, Formalism 1) or from the Tweedie-Stein pullback (Formalism 2), NOT from Fisher-Rao.\n"
       "  Four distinct geometries share one word 'interior geometry' across the article + the visual:\n"
       "  (i) Fisher-Rao g on the model, (ii) weighted (g, Phi) and its conformal Einstein frame,\n"
       "  (iii) pullback J^T Sigma^-1 J, (iv) location-scale hyperbolic horn. KB-002 collision-rule material.")

# ---- C23: Brown's admissibility integral == weighted-sphere-area recurrence test (v2 kernel K5) ----
# Brown (1971) Thm 3.6.1 (as quoted by Maruyama-Strawderman 2021 eq. (1.3)): for a spherically symmetric
# prior with marginal m(|x|^2), the generalized Bayes estimator is inadmissible iff Int_1^inf dt/(t^{d/2} m(t)) < inf.
# Weighted manifold (R^d, flat, m(|x|^2) dx): weighted area of the sphere of radius r is S(r) = omega r^{d-1} m(r^2);
# the rotationally-symmetric recurrence (parabolicity) test is  Int^inf dr/S(r) = inf  (Grigor'yan-type criterion).
t_, r_ = sp.symbols('t r', positive=True)
dd = sp.symbols('d', positive=True)
m = sp.Function('m')
integrand_r = 1 / (r_ ** (dd - 1) * m(r_ ** 2))
integrand_t = integrand_r.subs(r_, sp.sqrt(t_)) / (2 * sp.sqrt(t_))          # dr = dt / (2 sqrt t)
brown = 1 / (2 * t_ ** (dd / 2) * m(t_))
same = sp.simplify(sp.powsimp(integrand_t / brown, force=True)) == 1
conv = {k: sp.integrate(t_ ** (-sp.Rational(k, 2)), (t_, 1, sp.oo)) for k in (1, 2, 3, 4, 5)}
report("C23", "Brown's integral Int_1^inf dt/(t^{d/2} m(t)) == Int^inf dr/S(r) for the weighted manifold (R^d, m dx)", same,
       "substitution r = sqrt(t) maps the weighted-sphere-area integrand 1/(r^{d-1} m(r^2)) dr to dt/(2 t^{d/2} m(t)).\n"
       "So Brown's admissibility criterion is the recurrence/parabolicity test of the smooth metric measure space\n"
       "(R^d, flat g, m dx) -- the geometric object of Bakry-Emery theory -- in its rotationally symmetric form.\n"
       f"Consistency, m == 1 (MLE / Jeffreys): Int_1^inf t^(-d/2) dt = {conv}  -> finite iff d >= 3: Stein's theorem.")

# ---- C24: sphere test (Brown 1971 Thm 6.4.3 == Grigor'yan Thm 7.5) is at least as strong as the
#           ball-volume test (Grigor'yan Thm 7.3), and strictly stronger -----------------------------
# Claim: Int^inf rho d rho / V(rho) = inf  ==>  Int^inf d rho / S(rho) = inf, where V' = S.
# Proof (dyadic Cauchy-Schwarz): (b-a)^2 <= Int_a^b S * Int_a^b 1/S, so Int_{2^k}^{2^{k+1}} d rho/S >= 4^k / V(2^{k+1}),
# and sum_k 4^k / V(2^{k+1}) diverges iff Int rho/V does.  Numerical illustration + a counterexample to the converse.
import math
def tests(S, R=1e6, n=400000):
    rho = np.linspace(1.0, R, n)
    s = S(rho)
    V = np.concatenate(([0.0], np.cumsum(0.5 * (s[1:] + s[:-1]) * np.diff(rho)))) + 1.0   # V(1) := 1
    I_sphere = np.trapezoid(1.0 / s, rho)
    I_ball = np.trapezoid(rho / V, rho)
    # dyadic lower bound for the sphere integral in terms of V
    ks = np.arange(0, int(math.log2(R)) - 1)
    lb = sum(4.0 ** k / np.interp(2.0 ** (k + 1), rho, V) for k in ks)
    return I_sphere, I_ball, lb
rows = []
for name, S in [("S = rho (d=2 flat)", lambda r: r),
                ("S = rho^1.2 (transient)", lambda r: r ** 1.2),
                ("S = rho log rho (borderline, recurrent)", lambda r: r * np.log(r + 1.0)),
                ("S = rho log^2 rho (transient)", lambda r: r * np.log(r + 1.0) ** 2)]:
    I_s, I_b, lb = tests(S)
    rows.append(f"{name:<42} Int d rho/S ~ {I_s:9.3g}   Int rho d rho/V ~ {I_b:9.3g}   dyadic bound sum 4^k/V(2^(k+1)) ~ {lb:8.3g}")
# counterexample to the converse: thin shells of large area at rho in [2^k, 2^k + 1], S = rho elsewhere
def S_shells(r):
    out = r.copy()
    for k in range(1, 21):
        m = (r >= 2.0 ** k) & (r <= 2.0 ** k + 1.0)
        out[m] = r[m] ** 3
    return out
I_s, I_b, lb = tests(S_shells)
rows.append(f"{'thin cubic shells, S = rho elsewhere':<42} Int d rho/S ~ {I_s:9.3g}   Int rho d rho/V ~ {I_b:9.3g}   (sphere test applies, ball test does not)")
report("C24", "Sphere test Int d rho/S = inf (Brown Thm 6.4.3) implies ball test Int rho d rho/V = inf (Grigor'yan Thm 7.3), not conversely", None,
       "\n".join(rows) + "\n"
       "Numbers are truncations at rho = 1e6 (divergent integrals grow like log of the cutoff). The dyadic\n"
       "Cauchy-Schwarz bound shows the ball-volume test is a corollary of Brown's sphere test; the shell example\n"
       "(sphere integral diverges, ball integral converges) shows the converse fails. Hence transferring the\n"
       "Karp-Varopoulos-Grigor'yan volume test to weighted R^m yields nothing beyond Brown (1971) Thm 6.4.3.")

# ---------------------------------------------------------------------------
print("=" * 78)
print("SUMMARY")
print("=" * 78)
for tag, status, name in RESULTS:
    print(f"  {tag:<4} {status:<5} {name}")
fails = [t for t, s, _ in RESULTS if s == "FAIL"]
print(f"\n{len(RESULTS)} checks: {len(fails)} FAIL ({', '.join(fails)}), "
      f"{sum(1 for _, s, _ in RESULTS if s == 'PASS')} PASS, {sum(1 for _, s, _ in RESULTS if s == 'INFO')} INFO")
