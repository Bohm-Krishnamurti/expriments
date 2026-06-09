# Phase 3a — Candidate theoretical contributions (SELECTION GATE)

Status: drafted from the construct definitions in the program brief (DBR, HSS, SL as ratios
whose measurand is human governance effort; IDI as a structural predictor of surviving
governance burden). The agenda file with the full formal framework was not supplied, so each
candidate states its own primitives from scratch. Once the agenda is available, the chosen
candidate must be reconciled with its notation and any results it already contains.

Shared primitives (used by all candidates, specialized per candidate):
- A work unit (task) w in a task space W, characterized by at least two structural
  coordinates: context specificity k(w) >= 0 (how much tacit, principal-held information the
  task requires) and verification cost structure v(w) (cost for the principal to check an
  output against intent).
- An agent with capability a in [0, infinity); reliability p(a, w) in [0, 1], increasing and
  concave in a, decreasing in k(w).
- Human governance effort under delegation G(w, a) = s(w) + m(w, a) + (1 - p(a, w)) r(w),
  where s is specification effort (communicating intent and context), m is monitoring and
  verification effort, r is remediation effort on failure.
- Direct-performance cost h(w) > 0: the human cost of doing w without the agent.
- DBR(w, a) = G(w, a) / h(w). Delegation is burden-reducing iff DBR < 1.

---

## T1. Delegability threshold with comparative statics (the workhorse result)

Primitives: as shared, with p(a, w) = q(a) * e^{-lambda k(w)} or any p increasing in a,
decreasing in k, with lim_{a->inf} p(a, w) = pbar(w) <= 1; s(w) = sigma(k(w)) increasing.

Assumptions: (A1) G is continuous, decreasing in a (more capable agents need no more
governance, holding w fixed); (A2) G(w, 0) > h(w) (delegating to a useless agent is dearer
than doing the work); (A3) lim_{a->inf} G(w, a) < h(w) for w in a nonempty subset W_D of W.

Claim: For each w there is a unique threshold a*(w) in (0, inf] with DBR(w, a) < 1 iff
a > a*(w); a* is increasing in context specificity k(w), decreasing in the principal's
verification efficiency, and increasing in remediation cost r(w). The delegable set W_D(a)
= {w : a > a*(w)} expands monotonically in a, ordered by an index of (k, v, r) — which is
exactly the IDI: the structural coordinates that determine where w sits in the expansion
order.

Proof apparatus: single-crossing / monotone comparative statics (Milgrom-Shannon style);
clean, short, no fixed points. This is the result that makes IDI a theorem rather than a
dashboard: IDI is the order statistic the threshold map induces on W.

Answers "isn't this just X": partially — a referee can say this is task-based automation
(Acemoglu-Restrepo) with governance cost relabeled. The defense is that the threshold is
driven by governance terms (s, m, r) absent from the task-based model, but the structure is
familiar. Provability: 9/10. Differentiation: 6/10.

## T2. Positivity / no-full-automation result (the striking result)

Primitives: as shared, plus an information-theoretic floor: completing w to the principal's
intent requires I(w) bits of principal-held context (k(w) proportional to I(w)), and
communication of context costs the principal at least c > 0 per bit regardless of agent
capability; verification of an output against intent requires effort bounded below by a
function of the intent's description length whenever the principal's trust in p is itself
learned from monitoring.

Assumptions: (B1) capability does not transfer principal-held context: p(a, w) depends on a
and on the context actually communicated, and no a substitutes for uncommunicated bits;
(B2) either intent is tacit (I(w) > 0) or the principal's estimate of p must be maintained
by positive-rate sampling (trust is not free); (B3) failure cost r(w) > 0.

Claim: For every w with I(w) > 0, lim inf_{a->inf} G(w, a) >= c * I(w) > 0. Structural
delegation cost is bounded away from zero as capability grows; full automation of governance
is impossible for context-specific work, and the surviving burden is exactly the
specification term — which is what IDI is built to predict. Corollary: HSS composition
shifts toward specification and away from remediation as a grows.

Proof apparatus: a reduction argument (if G could fall below c*I(w), the agent's output
distribution is measurable with respect to less than I(w) bits of context, contradicting the
definition of I(w) as the intent's conditional description length). Needs care to avoid
smuggling the conclusion into assumption B1 — B1 does real work and must be defended as a
modeling claim about what capability is.

Answers "isn't this just X": strongly — no antecedent in TCE, agency, or task-based models
asserts a capability-invariant floor on governance cost. Risk: the result is only as strong
as B1, and a referee will attack exactly there. Provability: 6/10 (the information-theoretic
floor must be stated carefully). Differentiation: 9/10.

## T3. Separation result: delegation cost is a distinct order (the positioning result)

Primitives: three cost functionals on the same task space: transaction cost TC(w)
(Williamson: asset specificity, frequency, uncertainty governing make-vs-buy), agency cost
AC(w) (Jensen-Meckling / Holmstrom: incentive misalignment under hidden action), and
delegation cost DC(w, a) = G(w, a) as above, evaluated with an aligned, incentive-free agent
(the AI has no utility function over outcomes, so AC-style residual loss is zero by
construction).

Assumptions: (C1) TC depends on relationship-specific investment and opportunism, neither of
which DC contains; (C2) AC is zero when the agent's objective coincides with the principal's;
(C3) DC depends on (k, v, r), which vary independently of the TC and AC drivers across W
(a richness condition on the task space).

Claim: The orders induced on W by TC, AC, and DC are pairwise non-nested: there exist
w1, w2 with TC(w1) < TC(w2) and DC(w1) > DC(w2), and there exists w with AC(w) = 0 and
DC(w, a) > 0 for all a. So a work unit can be cheap to contract over and dear to delegate,
and delegation cost survives perfect incentive alignment. Construction is explicit
(two-by-two family of tasks crossing high/low asset specificity with high/low context
specificity).

Proof apparatus: explicit counterexample plus a small proposition that the richness
condition is generic. Easiest proof in the set; the work is in making the construction
economically meaningful rather than contrived.

Answers "isn't this just X": this IS the answer to "isn't this just X" — it is the
differentiation argument stated as a theorem. Weakness: separation results can read as
defensive rather than productive; strongest when paired with T1 so the paper both builds
the object and separates it. Provability: 9/10. Differentiation: 8/10 (but by design).

## T4. Burden-composition comparative statics (the empirical bridge)

Primitives: as shared; decompose G into G_s (specification), G_m (monitoring), G_r
(remediation); HSS_j = G_j / G.

Assumptions: (D1) p(a, w) increasing in a with p -> pbar(w); (D2) monitoring effort chosen
optimally by the principal against a posterior over p maintained by sampling (a simple
inspection-game or bandit-monitoring structure); (D3) s independent of a.

Claim: Along any capability ladder, remediation share G_r/G falls monotonically, optimal
monitoring falls but at rate bounded below by the trust-maintenance constraint, and
specification share rises toward 1 (or toward the floor of T2 if combined). Hence the
testable prediction the Phase 1/2 proxies need: agent-observable failure signals should
diverge from headline success rate exactly where verification, not error rate, dominates.

Proof apparatus: envelope theorem plus monotone statics on the principal's monitoring
problem. Moderate difficulty. This candidate is the one the empirical phase can actually
touch, since its statics are about observable composition, not about human-effort levels.

Answers "isn't this just X": moderate — closest neighbor is Aghion-Tirole on monitoring and
delegation, and the differentiation must be argued (their tradeoff is information vs
initiative; here it is trust maintenance vs verification cost). Provability: 7/10.
Differentiation: 7/10.

---

## Ranking (provability x differentiation, per the gate's criterion)

1. T3 separation (clean proof, directly answers the central objection; pairs naturally with T1)
2. T1 threshold (cleanest proof, builds the construct; weakest standalone differentiation)
3. T4 composition statics (the only candidate the permitted empirics can test; medium on both)
4. T2 positivity floor (highest upside, highest assumption risk; B1 will draw fire)

Recommended package if one paper must carry one result: T1 as the model's main proposition
with T3 as the differentiation theorem (T3 is short enough to be the second result without
bloating the paper), or T2 alone if the goal is the boldest claim. The choice is the user's.
