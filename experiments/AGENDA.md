# Measuring Human-to-Agent Delegation Costs
A research agenda for AI economics, organizations, and policy

(Supplied by the program owner 2026-06-10. This file grounds all phases. Verbatim content
of the agenda as provided; formatting adapted to markdown.)

## Executive judgment

Capability is insufficient for economic delegation. Across domains, the binding cost often
shifts from production to specification, verification, and risk governance.

Delegation cost is a real and undermeasured economic quantity. It is not identical to model
capability, automation exposure, transaction cost, agency cost, or coordination cost, though
it overlaps with all of them. The most useful definition is:

> Delegation Cost = the human governance effort required to convert an objective into an
> acceptable outcome through an AI agent, rather than by direct human execution.

The key word is governance. Delegating work to an AI system is not just "prompting." It
includes specifying intent, supplying context, supervising execution, correcting course,
verifying outputs, repairing failures, managing risk, and accepting responsibility.

The central empirical object should not be an occupation or even a conventional task. The
best candidate unit is a Delegable Work Unit: a bounded episode of economically meaningful
work with an objective, context, constraints, tools, stakeholders, acceptance criteria, and
consequences. This unit is small enough to measure experimentally, but rich enough to
capture what humans actually delegate.

The core research claim is:

> Firms adopt agentic AI when the risk-adjusted cost of delegating work falls below the
> risk-adjusted cost of doing the work directly, not merely when AI systems become capable
> of producing plausible outputs.

This is compatible with transaction-cost economics, but it extends it. Coase's theory
explained why firms exist partly because "the operation of a market costs something";
Williamson then generalized this into governance-choice theory; Alchian and Demsetz
emphasized monitoring and metering in team production; Grossman, Hart, and Moore focused on
incomplete contracting and residual control rights. AI delegation adds a new class:
machine-mediated internal contracting under radically incomplete specification. The "agent"
has no human incentives, but it still creates agency-like problems because objectives,
context, preferences, and acceptable tradeoffs are only partially specified.

Current AI benchmarks mostly measure whether agents can complete tasks, not how much human
labor is required to make their outputs usable. GAIA, SWE-bench, WebArena, OSWorld,
tau-bench, RE-Bench, HCAST, METR's time-horizon work, and TheAgentCompany are important
because they move toward realistic agentic work, but most still treat success as an endpoint
rather than estimating the full human governance budget required to reach that endpoint in
production.

The strongest proposed construct is therefore the Delegation Burden Ratio:

DBR = (risk-adjusted human effort required under AI delegation) /
      (risk-adjusted human effort required under direct human completion)

A task is economically delegable when DBR < 1. It is highly delegable when DBR << 1. It is
capability-exposed but not economically delegable when the AI can sometimes do it, but
DBR >= 1.

## I. Literature review: where delegation cost fits

### 1. Economics

Transaction-cost economics. Coase's central move was to reject the assumption that market
exchange is frictionless. Firms exist because using the price mechanism is costly: one must
discover prices, negotiate, contract, and adapt. Williamson extended this into a
comparative-governance theory: transactions differ by uncertainty, frequency, and asset
specificity, and governance structures economize on those frictions.

AI delegation is analogous but not identical. The human is not choosing between market and
hierarchy; the human is choosing between direct execution and objective-mediated execution
by a nonhuman system. The relevant governance problem is not bargaining with another party,
but translating intent into executable form under incomplete specification.

Interpretation: delegation cost is a cousin of transaction cost, but the transaction is
cognitive and organizational rather than market exchange. The agentic equivalent of "asset
specificity" is context specificity: how much of the work depends on local, tacit, unstable,
or privileged knowledge.

Principal-agent theory. Principal-agent theory studies delegation when the agent has private
information, different incentives, and imperfect observability. Holmstrom and Milgrom's
multitask principal-agent model is especially relevant because it shows how measured and
unmeasured dimensions of work distort effort allocation.

AI agents do not have human motives in the standard incentive-theoretic sense. But they
still create agency-like problems:

Objective != Prompt != Model-inferred goal != Observed output

Thus the AI delegation problem is not moral hazard in the classic sense; it is specification
hazard plus verification hazard. The human principal must define success, observe behavior
or outputs, and intervene when the system optimizes the wrong proxy.

Team theory and information economics. Marschak and Radner's team theory is central because
it studies decentralized decision-making under common objectives but distributed
information. A team can share goals and still perform poorly if information is allocated
badly. This maps closely onto human-agent systems. The human and AI may share a nominal
objective, but the AI lacks some state information, institutional context, tacit
preferences, stakeholder history, or risk tolerance. Delegation cost therefore includes the
cost of deciding what information must be transferred and what can be safely omitted.

Incomplete contracts and property-rights theory. Grossman and Hart argue that when contracts
cannot specify every future contingency, ownership matters because it allocates residual
control rights. Hart and Moore extend this logic to firm boundaries. AI delegation is
radically incomplete contracting without a legal counterparty. The human cannot fully
specify every contingency. The "residual control right" remains with the human or
organization, unless autonomy is delegated to the agent. As autonomy rises, the key
governance question becomes: which decisions can be safely transferred to the agent, and
which must remain reserved to humans or institutions? This is where delegation cost becomes
economically fundamental. Capability alone does not answer the residual-control question.

Organizational economics and bounded rationality. Simon's bounded rationality matters
because delegation is partly an attention-allocation problem. Humans satisfice under
cognitive limits; organizations exist partly because they structure attention, routines,
authority, and decision premises. Delegating to AI can reduce execution effort while
increasing supervisory attention. That is the AI version of Bainbridge's "ironies of
automation": automation may remove routine execution while leaving humans responsible for
rare, difficult, high-stakes exceptions.

Conclusion from economics: delegation cost resembles transaction cost, agency cost, team
coordination cost, and incomplete-contracting cost, but it is not reducible to any one of
them. It is best treated as a governance cost of machine-mediated production.

### 2. Management and organizational theory

Management research adds three ideas that economics often abstracts away: tacit knowledge,
attention, and organizational embedding. Szulanski's work on "internal stickiness" shows
that even within firms, transferring best practices is difficult; major barriers include
absorptive capacity, causal ambiguity, and recipient-side knowledge limitations. Argote and
Ingram frame knowledge transfer as a basis of competitive advantage precisely because
knowledge is embedded in people, tools, routines, and interactions. Brown and Duguid's
communities-of-practice work emphasizes that formal job descriptions often miss how people
actually work.

These findings matter because AI delegation is often treated as if work can be converted
into text instructions. In reality, delegability depends on how much relevant knowledge is
explicit, stable, codified, localizable, and verifiable rather than tacit, socially
embedded, evolving, or contested.

Nonaka's tacit-explicit knowledge framework is relevant but should not be accepted
uncritically. The useful point is that much organizational knowledge is not initially
available as clean instructions. Carlile's work on knowledge boundaries is especially
useful: syntactic boundaries require common language, semantic boundaries require common
meaning, and pragmatic boundaries require reconciling different interests and consequences.

Implication: AI delegation cost will be lowest when the work crosses only syntactic
boundaries and highest when it crosses pragmatic boundaries involving stakeholders,
incentives, responsibility, and contested meanings.

### 3. Human-computer interaction and human factors

Bainbridge's "Ironies of Automation" argues that automation may expand rather than eliminate
operator problems, especially when humans are left responsible for abnormal conditions
without enough practice or situational awareness. Parasuraman, Sheridan, and Wickens
classify automation by function: information acquisition, information analysis, decision
selection, and action implementation; they explicitly note that automation changes human
activity and can impose new coordination demands.

Trust research is central. Lee and See argue that trust governs reliance when complexity
prevents full understanding of the automated system. Automation bias and complacency
research shows that humans may over-rely on automated advice, while algorithm-aversion work
shows that humans may under-rely after observing errors. This means delegation cost is not
just time. It includes calibration: the effort required for humans to know when to trust,
doubt, audit, or override the agent.

Amershi et al.'s human-AI interaction guidelines are useful because they emphasize
uncertainty, controllability, feedback, correction, and user expectations. But standard HCI
metrics are often product-level, not economy-level. A delegation-cost framework must convert
HCI burden into labor economics.

### 4. AI evaluation and agent benchmarks

GAIA tests real-world assistant questions requiring reasoning, multimodality, browsing, and
tool use; the original paper reports large gaps between humans and GPT-4 with plugins.
SWE-bench uses real GitHub issues and pull requests, requiring codebase understanding and
multi-file changes. WebArena evaluates autonomous web agents in realistic websites; OSWorld
evaluates open-ended computer tasks across real desktop environments. tau-bench tests
tool-agent-user interaction and policy following in simulated customer-service domains,
finding that even strong function-calling agents can be inconsistent across trials.

METR's time-horizon metric is particularly relevant because it asks what length of human
task an AI can complete at a given success probability. The reported 50%-task-completion
time horizon is a capability metric grounded in human task duration, not just benchmark
accuracy. HCAST similarly collects human baselines under comparable conditions and estimates
how task duration relates to AI success. RE-Bench compares frontier agents and human experts
on open-ended ML research engineering tasks. TheAgentCompany simulates a small software
company and reports that the most competitive tested agent completed 24% of tasks
autonomously.

These are major advances, but delegation cost requires additional measurements:

Success rate != Cost of successful delegation

A benchmark can report that an agent completes 40% of tasks, but firms need to know how many
human minutes are needed to raise success to 95%, how costly failures are, and whether
verification is cheaper than doing the task.

## II. Taxonomy of delegation costs

Component taxonomy (component / definition / examples / shrinks with capability? /
persistent?):

- Specification: human effort to express goals, constraints, preferences, success criteria
  (prompting, briefs, examples, policies). Shrinks partly; persists for ambiguous goals.
- Context transfer: effort to provide background, documents, institutional knowledge,
  permissions (uploads, memory setup, retrieval, access control). Shrinks; persists when
  context is tacit or sensitive.
- Monitoring: human attention spent watching progress (checking intermediate steps, logs).
  Shrinks; some monitoring remains in high-stakes domains.
- Intervention: corrections during execution ("no, use the other dataset"; "stop, that
  violates policy"). Shrinks; persistent under changing goals or contested tradeoffs.
- Verification: checking whether output is correct and acceptable (code review, legal
  review, fact-checking, QA). Partly shrinks; often persistent; may increase for superhuman
  outputs.
- Rework: repairing or rerunning failed outputs (editing drafts, fixing hallucinated
  citations, debugging). Shrinks; persistent when task is novel or underdefined.
- Risk management: precautions due to liability, security, privacy, reputational loss, or
  irreversible error (audit trails, approvals, sandboxing, human signoff). Partly shrinks;
  strongly persistent.
- Coordination: aligning agent work with other humans, teams, systems, timelines. Partly
  shrinks; persistent in multi-stakeholder work.
- Legitimacy/accountability: human effort required because a human or institution must own
  the decision (medical, legal, hiring, strategy, public policy). Does not shrink or shrinks
  slowly; strongly persistent.
- Integration/setup: tooling, workflow redesign, permissions, process change (API setup,
  RPA integration, agent memory). Shrinks at margin; persistent as fixed adoption cost.

The most important distinction is: Execution difficulty != Delegation difficulty. A
difficult math proof may be easy to delegate if the objective is precise and verification is
possible. A seemingly simple executive email may be hard to delegate if it depends on
political context, hidden preferences, relationships, and reputational risk.

## III. Existing measurement approaches

Fragments across HCI, operations, AI evaluation, management, and field experiments: human
active minutes; number of interventions; clarification rounds; verification time; rework
burden; escalation rate; acceptance rate; error-correction count; supervisor workload
(NASA-TLX-style); attention allocation; latency; pass@k / reliability; risk-adjusted
expected loss; cost per accepted deliverable; supervision leverage (counterfactual human
work-hours completed per human supervision-hour).

The best empirical target is not one metric but a measurement bundle:

Delegation Cost = T_s + T_c + T_m + T_i + T_v + T_r + R

where T_s is specification time, T_c context-transfer time, T_m monitoring time, T_i
intervention time, T_v verification time, T_r rework time, and R is risk-adjusted expected
residual loss plus compliance burden.

## IV. Formal mathematical framework

### 1. Work unit

Let a work unit u be u = (o, x, K, A, S, E, L) where o: objective; x: initial context and
inputs; K: constraints, policies, preferences; A(y): acceptance predicate over output y;
S: stakeholders and authority structure; E: environment and tools; L(e): loss function over
errors or failures. This is broader than a task. A "task" usually captures an activity; a
work unit captures the delegation-relevant contract.

### 2. Direct human cost

Let H_u(q, rho) be the minimum expected human cost to complete u directly at quality
threshold q and acceptable risk rho:

H_u(q, rho) = min over pi_h of E[ w_h T_h + C_delay + E[L(e)] ]
subject to P(A(y) >= q) >= 1 - rho.

### 3. Delegation cost

Let a be an AI agent and pi_d a delegation protocol. Human governance effort is decomposed
G = (T_s, T_c, T_m, T_i, T_v, T_r, T_g) where T_g is governance/risk-management time. Then:

DC_{u,a}(q, rho) = min over pi_d of E[ w_h * 1'G + C_a + C_delay + E[L(e) | pi_d, a] ]
subject to P(A(y_a) >= q) >= 1 - rho.

This makes delegation cost conditional on quality and risk. A low-quality AI output is not
cheap if it fails the acceptance constraint.

### 4. Delegation Burden Ratio

DBR_{u,a}(q, rho) = DC_{u,a}(q, rho) / H_u(q, rho)

DBR < 1: delegation economically cheaper than direct work. DBR = 1: break even. DBR > 1:
the AI may be capable, but delegation is not yet economical. DBR ~ 0: near-full automation,
ignoring fixed adoption costs. DBR can exceed 1 when prompting, debugging, and verification
take longer than doing the work.

### 5. Human Supervision Share

HSS_{u,a} = (T_s + T_c + T_m + T_i + T_v + T_r + T_g) / T_direct_human

Avoids pricing complications; estimable in experiments.

### 6. Supervision leverage

SL_{u,a} = (counterfactual human hours of accepted work produced) /
           (human governance hours required)

If one human supervisor can govern 20 hours of agentic work in one hour, SL = 20. If
verification takes as long as doing the task, SL ~ 1.

### 7. Capability elasticity of delegation cost

epsilon_D = d log DC_{u, a_theta} / d log theta, where theta indexes agent capability. Some
work units have high capability elasticity; others low, because their burden comes from
persistent ambiguity, accountability, or verification difficulty.

### 8. Structural delegation cost

SDC_u(q, rho) = liminf_{theta -> infinity} DC_{u, a_theta}(q, rho)

The irreducible delegation cost under arbitrarily capable agents; not necessarily zero.
Examples of positive lower bounds: a CEO deciding what objective should be pursued; a doctor
obtaining patient consent and bearing clinical responsibility; a lawyer certifying a filing;
a scientist deciding whether a surprising result is meaningful; a manager reconciling
stakeholders with conflicting preferences; a public official making a legitimate decision
under democratic accountability.

### 9. Which formulation is best?

Three levels combined: (i) additive component model for diagnosis; (ii) Delegation Burden
Ratio for economic comparison; (iii) Structural Delegation Cost / Intrinsic Delegability
Index for forecasting.

## V. Experimental methodology

Experimental object: the Delegable Work Unit (o, x, K, A, S, E, L). A good empirical work
unit is not "write" or "analyze data"; it is "given this dataset, this prior memo, this
stakeholder's preferences, and these constraints, produce a decision-ready recommendation
that will be accepted by an independent evaluator using this rubric."

Core conditions: A human direct; B human delegates and supervises; C AI autonomous + human
verification; D iterative human-AI collaboration; E AI autonomous without review; F human
manages multiple agents. The most credible delegation-cost estimate compares A vs B vs C,
with D to distinguish delegation from collaboration.

Outcomes, primary: DBR, HSS, SL, quality-adjusted cost per accepted output. Secondary:
active minutes by component, interventions, clarification rounds, verification time, rework
time, error severity, acceptance rate, residual risk, latency, supervisor workload, learning
effects.

Design: stratified, crossed, randomized field-lab hybrid; matched work-unit pairs;
within-worker crossover where manageable; blinded evaluators; telemetry plus self-reports;
multiple agent systems and versions; professions spanning software engineering, legal
research, finance, scientific literature review, customer support, marketing, operations,
project management, executive decision support.

Threats: task sampling bias; worker selection bias; novelty effects; learning/carryover;
evaluator leakage; hidden labor; quality threshold instability; model update instability;
risk undermeasurement; organizational embedding.

Power: estimate on log(DBR); paired design n ~ (z_{1-alpha/2} + z_{1-beta})^2 sigma_d^2 /
delta^2; with sigma_d = 0.5, delta = 0.2, alpha = 0.05, power 0.8, n ~ 49 matched pairs per
stratum; inflate by 1 + (m-1) * ICC for clustering. Practical target: hundreds to thousands
of work-unit attempts, because heterogeneity is the object of study.

## VI. Intrinsic Delegability Index

Concept: how much of a work unit's delegation burden comes from structural properties of the
work rather than the current agent's weaknesses. High-IDI: delegation cost should fall close
to zero as agents improve. Low-IDI: persistent human governance needs.

Definition: IDI_u = 1 - SDC_u / H_u. IDI ~ 1: intrinsically easy to delegate. IDI ~ 0: even
perfect execution leaves most human burden intact. IDI < 0: delegation structurally costs
more than direct execution because of risk, legitimacy, or verification burdens.

Dimensions (high delegability / low delegability): objective clarity (precise goal /
evolving, contested, political); context encapsulation (bundleable / tacit, social, local,
confidential); preference stability (stable / changing during work); verification ease
(cheap checking / expert judgment or real-world feedback); error reversibility (cheap to
undo / irreversible or high-stakes); outcome observability (visible soon / delayed or
ambiguous); decomposability (independent modules / dense dependencies); stakeholder
complexity (one owner / conflicting objectives); tacit knowledge load (instructions capture
know-how / embodied expertise); environmental uncertainty (stable / dynamic, adversarial,
nonstationary); tool and data accessibility (safe access / fragmented, private,
permissioned); legitimacy requirement (output matters / human authorship and accountability
matter); consequence of failure (low loss / high legal, financial, medical, security,
reputational loss); coordination burden (acts alone / synchronous human coordination);
novelty (similar cases exist / exploratory or unprecedented).

Measurement today: expert rubric scoring on the dimensions; behavioral proxies
(specification length, clarification turns, verification/direct-time ratio, rework fraction,
inter-evaluator disagreement); repeated-agent trials across capability levels; hierarchical
modeling separating work-unit effects from agent effects. Stylized model:

log DC_{u,a} = alpha + beta'X_u + gamma*theta_a + delta'(X_u x theta_a) + eta_worker +
eta_domain + epsilon

The intrinsic component is the work-unit features and residual work-unit effects that
persist across agents.

Validation: IDI is coherent if it predicts current delegation burden; rate of decline in
burden across stronger agents; residual supervision at high capability; firm adoption
patterns; escalation rates in production; worker-reported supervisory load; quality-adjusted
cost savings. Strongest validation is longitudinal.

## VII. Capability dependence

Costs likely to shrink (current-system limitations): prompt engineering, routine context
ingestion, simple planning failures, tool-use errors, hallucinated facts, formatting and
style rework, short-horizon memory limits, mechanical monitoring, low-level debugging,
simple verification through tests.

Costs likely to persist (nature of the work): deciding what should be done; resolving
conflicting preferences; allocating responsibility; obtaining consent; managing legitimacy;
handling irreversible risk; verifying outputs whose correctness is not mechanically
testable; coordinating stakeholders; maintaining trust; bearing legal and reputational
accountability.

Costs that may increase with capability: scope of delegated work; blast radius of errors;
security and misuse risk; verification difficulty; audit-trail needs; organizational
dependence; skill decay; accountability ambiguity; multi-agent coordination. Central
paradox: as execution cost falls, governance cost may become the binding constraint.

Scenario forecast: current frontier (low burden for drafting, summarization, simple code,
routine support; high for ambiguous, high-stakes, long-horizon); expert-human-level agents
(specification and rework fall sharply; verification, risk, accountability remain); highly
capable autonomous agents (humans shift to objectives, authority, audit, exceptions);
superhuman systems (execution cheap, verification and legitimacy harder when outputs exceed
human expertise).

Delegation costs approach zero only when: objective clear + context accessible + output
verifiable + errors reversible + stakes low + legitimacy does not require human judgment.

## VIII. Representation of economic work

Competing representations: occupations (scale, too coarse); jobs (firm-specific, unstable);
tasks (granular, decontextualized); activities (behaviorally thin); skills (inputs, not
delegated outputs); competencies (worker capability, not work products); workflows
(sequences, dependencies, handoffs; harder to standardize); business processes (repeatable
work); projects (heterogeneous); objectives (closest to agentic delegation, hard to
measure); outcomes (economically meaningful, attribution difficult).

Best unit: the Delegable Work Unit, nested in workflows, mappable upward: DWU -> Workflow ->
Job -> Occupation -> Industry -> Economy. A DWU is a bounded work episode in which an
accountable human or organization seeks an accepted outcome under specified context, tools,
constraints, stakeholders, and risk. A mini-contract between objective and outcome.

## IX. Evaluation of existing datasets and frameworks

O*NET: standardized occupational information across knowledge, skills, abilities, tasks,
work activities, work context; regularly updated. Insufficient as a foundation: weak on
workflow sequences, project context, tacit knowledge, stakeholder conflict, verification
difficulty, risk and liability, dynamic objectives, intra-occupation variation,
firm-specific tools, agentic multi-step work. Likely to fail for research, discovery,
executive decision-making, entrepreneurship, strategy, coordination-intensive management,
multi-stakeholder work. Judgment: use O*NET as a mapping layer, not the primary ontology.

ESCO: multilingual occupations/skills/competences classification; same basic limitation.
PIAAC: adult proficiency and skill use; worker capability, not delegation cost. OEWS:
employment and wage estimates for ~830 occupations; essential for scaling. ATUS: time
allocation; no delegation cost. Lightcast/Burning Glass: real-time posting-derived skills;
postings are not workflows. Enterprise workflow and process data (Jira, GitHub, Zendesk,
Salesforce, ServiceNow, Asana, Linear, Notion, Slack, Workspace, M365; process mining; PR
data; version histories): most promising source. Judgment: hybrid = enterprise DWU data +
experimental delegation trials + O*NET/OEWS/ATUS mapping + Lightcast skill dynamics.

## X. Scaling delegation cost to the economy

Method: define DWU taxonomy; sample work units; estimate delegation burden experimentally;
link DWUs to workflows; link workflows to occupations and industries; weight by labor hours
and wages; model adoption thresholds and fixed costs; forecast across capability scenarios.

Economy-wide metrics: delegation burden by occupation / workflow / industry; share of labor
hours with DBR < 0.2; with 0.2 <= DBR < 0.8; with DBR >= 1; supervision-intensive residual
labor share; agent work-hours per human governance-hour.

Scaling approaches: occupation-based (tractable, medium); task-based (medium); workflow-based
(strong theory, high forecasting value); firm-level (strong, low tractability);
process-mining (strong for repeatable digital work); project/objective-based (highest for
agentic work, hard). Most defensible: workflow-first, occupation-linked.

Adoption model: a firm adopts delegation for work unit u iff
DC_{u,a} + F_integration + F_training + R_org < H_u, with fixed costs F and organizational
risk R_org (compliance, liability, disruption, change management). Improves on
automation-exposure models: exposure asks whether AI can affect a task; delegation cost asks
whether AI can be profitably governed in real production.

## XI. Implications for AI economics

Delegation cost vs automation exposure: Frey and Osborne (computerization susceptibility),
Felten-Raj-Seamans (AI Occupational Exposure), Eloundou et al. (GPT exposure), Acemoglu and
Restrepo (automation and new tasks) are useful but incomplete: exposure is not adoption.
Delegation cost may be a better leading indicator than benchmark accuracy because it tracks
the bottleneck firms actually face: can we safely and cheaply make the system do it for us?

Productivity studies need delegation-cost decomposition: Noy and Zhang (writing), Brynjolfsson,
Li, and Raymond (customer support), Peng et al. (Copilot), Dell'Acqua et al. (jagged
frontier) show heterogeneous gains. Delegation cost explains the heterogeneity: gains are
largest when specification and verification are cheap relative to execution; AI hurts when
workers misjudge delegability.

## XII. Annotated bibliography: 70 key works

(Seed list as provided; verify before use. Economics, firms, contracts, organizations:
Coase 1937; Williamson TCE; Alchian and Demsetz 1972; Holmstrom and Milgrom multitask;
Grossman and Hart; Hart and Moore; Marschak and Radner; Simon; March and Simon; Nelson and
Winter. Knowledge and management: Szulanski; Argote and Ingram; Brown and Duguid; Nonaka and
Takeuchi; Carlile; Lave and Wenger; Teece; Aghion and Tirole. Human factors and HCI:
Bainbridge; Parasuraman, Sheridan, and Wickens; Sarter, Woods, and Billings; Lee and See;
Parasuraman and Manzey; Skitka, Mosier, and Burdick; Dietvorst, Simmons, and Massey; Logg,
Minson, and Moore; Amershi et al. Automation, tasks, labor: Autor, Levy, and Murnane;
Acemoglu and Autor; Acemoglu and Restrepo; Frey and Osborne; Felten, Raj, and Seamans;
Eloundou et al.; Brynjolfsson and Mitchell; Agrawal, Gans, and Goldfarb. Empirical AI
productivity: Noy and Zhang; Brynjolfsson, Li, and Raymond; Peng et al.; Dell'Acqua et al.;
OECD generative AI report. Benchmarks: GAIA; SWE-bench; WebArena; OSWorld; tau-bench;
tau2-bench; RE-Bench; HCAST; METR time-horizon; TheAgentCompany; Anthropic agent autonomy
measurement; DecisionBench / emergent delegation benchmarks. Labor data: O*NET; ESCO; PIAAC;
OEWS; ATUS; Lightcast; process mining (van der Aalst). Policy: Hadfield and Koh, economy of
AI agents; Ada Lovelace Institute, dilemmas of delegation; levels of autonomy for AI agents;
agent autonomy measurement. Additional foundations: Arrow; Milgrom and Roberts; Dawes;
human-centered automation; organizational routines; boundary objects; AI evaluation
infrastructure.)

## XIII. Most important open research questions

1. What is the right unit of economic work? (DWU vs workflows, projects, tasks, outcomes.)
2. Can intrinsic delegability be separated from current model weakness?
3. What is the lower bound on human governance?
4. When does verification cost exceed execution cost?
5. How should risk be priced?
6. How does delegation skill vary across workers?
7. Does AI reduce or increase inequality among workers?
8. How does delegation change firm boundaries?
9. Can AI agents verify other AI agents cheaply enough to reduce human burden?
10. What happens when outputs exceed human evaluative ability?
11. How much of the economy is workflow-structured enough for agentic delegation?
12. Can enterprise telemetry be used without violating privacy and worker autonomy?

## Final assessment

Delegation cost should be treated as a fundamental economic construct for AI-era labor
analysis. It improves on automation exposure because it explains why capability does not
immediately become adoption; on task-based analysis because it treats work as embedded in
objectives, workflows, institutions, and risk; on benchmark accuracy because it measures the
human effort needed to produce accepted outcomes.

The strongest research program builds: Delegable Work Unit taxonomy + Delegation Burden
Ratio + Intrinsic Delegability Index + workflow-to-economy scaling model.

Central empirical hypothesis: AI diffusion accelerates when DBR falls below 1.
Central theoretical hypothesis: lim_{theta -> infinity} DC_{u, a_theta} > 0 for many
economically important forms of work. Even extremely capable AI systems do not eliminate
delegation costs in general; they transform them, from execution, correction, and rework
toward objective-setting, verification, authority, legitimacy, and risk governance.
