# An improved delegation-cost experiment design

Proposal prepared 2026-06-10. This improves on the design in AGENDA.md Section V. It
involves human participants, so it sits outside the current program's no-human-data
boundary; it is the design the program would run with funding and IRB approval. The
improvements below come directly from what Phases 1-2 of this program found in existing
agentic-benchmark data: scoring artifacts that degenerate agents exploit, model-scaffold
confounding in every public ladder, and the absence of instrument validation in benchmark
practice.

## What the agenda's design gets right and where it is weakest

The agenda's Section V design (stratified, crossed, randomized field-lab hybrid over
conditions A-F, matched work-unit pairs, blinded evaluators, telemetry plus self-report) is
sound on sampling and on the A vs B vs C contrast. Its four weaknesses: (1) IDI dimensions
enter only as measured strata, so dimension effects on burden are identified by comparison
across heterogeneous tasks, the weakest possible identification; (2) the measurement
instrument itself is never validated — nothing plays the role the do-nothing agent plays in
benchmark auditing; (3) "capability dependence" is left to model versions that arrive over
calendar time, confounding capability with everything else that changes; (4) the time
metrics have no pre-registered attribution rules separating active governance effort from
passive waiting and from off-clock thinking.

## Design

Unit. Delegable Work Units per the agenda, but each DWU is authored in two to four
"twin" variants that differ by a minimal edit to exactly one IDI dimension: the same task
with the verification rubric supplied versus withheld (verification ease), with the
stakeholder preference memo supplied versus summarized versus absent (context
encapsulation), with reversible versus irreversible side effects in the sandbox (error
reversibility). This converts IDI dimensions from scored covariates into randomized
treatments: the burden effect of a dimension is identified within twin pairs, holding all
other task content fixed. Twin authoring is the main fixed cost and the main scientific
upgrade.

Arms. The agenda's A (human direct), B (delegate and supervise), C (autonomous then
verify), D (collaborate) are retained; E (no review) is kept only as a scoring arm, not a
deployment claim. Three arms are added:
- B0, degenerate delegate: the "agent" is a canned policy (do-nothing, or template output)
  unknown to the participant. This is the instrument-validation arm: it measures how much
  apparent supervision effort, acceptance, and quality score the pipeline produces when no
  real delegation is happening, exactly as a do-nothing agent calibrates tau-bench's reward.
  Any burden estimate is reported net of B0.
- Planted-flaw verification probes: a known fraction of arm-C outputs contain seeded,
  verifiable defects. The evaluator and supervisor false-accept rate on planted flaws is
  the direct measure of verification quality, and the time-to-catch is the price of
  verification, neither of which the agenda's design observes.
- Scaffold-split: each model tier runs under two fixed scaffolds, crossed, so model and
  scaffold effects on burden separate. Every public ladder this program examined confounds
  them.

Capability ladder by design, not by calendar. Each DWU twin set runs simultaneously against
three frozen model tiers (e.g. a 2023-class, a 2024-class, and a current frontier model)
under identical scaffolds. The capability-elasticity of each burden component (the agenda's
epsilon_D) and the structural residual are then estimated within task from a single
fielding, rather than longitudinally with drifting everything-else. Longitudinal replication
remains the validation, not the identification.

Measurement. Component times T_s, T_c, T_m, T_i, T_v, T_r, T_g are logged by an
instrumented workspace with a pre-registered event-to-component attribution table (which
UI events count as specification, which as monitoring, what idle gap closes an active
episode), validated against experience-sampling self-reports on a 10% subsample; the
attribution table is frozen before fielding, because post hoc attribution is where hidden
flexibility lives. Risk (the R term) is priced rather than narrated: evaluators accept or
reject under a proper scoring rule with real stakes, and supervisors in arm B post a bond
against later-discovered defects, giving an incentive-compatible residual-risk price the
agenda leaves unmeasured. Trust calibration (over- and under-reliance) is read off the
planted-flaw probes and occasional correct-output "catch trials" that participants
needlessly redo.

Outcomes. Primary: DBR and HSS per DWU per arm per tier, computed from logged component
times under the frozen attribution table, reported net of B0; SL at the portfolio level
from arm F. Secondary: the full agenda list. Every agent-side run also logs the
agent-observable proxy signals this program validated (steps, retries, flakiness across
k=4 repeated agent runs per DWU, failure position), so the proxy-to-burden mapping is
estimated in the same data that measures burden — closing the loop the current program can
only approach from the agent side.

Identification and analysis. Hierarchical model per the agenda's stylized equation, with
twin fixed effects: log burden component on dimension-edit indicators, tier, scaffold,
edit-by-tier interactions, worker and domain random effects. The IDI of a dimension is its
edit effect that survives at the top tier; SDC_u is the fitted asymptote, reported with the
explicit caveat that three tiers bound, not identify, a limit. All decision rules, the
attribution table, the planted-flaw rate, and the B0-netting rule are pre-registered;
group-sequential interim looks on log(DBR) with alpha spending, since cost distributions
are right-skewed and the agenda's n ~ 49 pairs per stratum will need revising upward once
sigma_d is observed rather than assumed.

Mapping layer. Each DWU is tagged at authoring time to O*NET task statements and detailed
work activities (the database is publicly downloadable), so estimates aggregate to
occupations without making O*NET the ontology — it remains the mapping layer the agenda
assigns it.

## What this buys over the agenda's design

Within-task causal identification of IDI dimensions instead of cross-task correlation; an
instrument-validation floor (B0) so delegation burden is never confused with pipeline
overhead; separation of model from scaffold; a priced rather than asserted risk term; a
direct measurement of verification quality via planted flaws; and a same-data bridge from
agent-observable proxies to measured human burden, which is the link the present
no-human-data program must leave as a labelled gap.
