---
name: prompt-engineering
description: >
  Expert prompt engineering skill for analyzing, refactoring, and writing prompts with high precision.
  Use this skill whenever the user wants to: write a new prompt from scratch, refactor or improve an existing
  prompt, analyze why a prompt produces poor or inconsistent outputs, design system prompts or persona prompts,
  create partial/reusable prompt components, design structured-output prompts with schemas, or audit a set of
  prompts for alignment and consistency across a pipeline.
  Trigger this skill even for quick prompt tweaks — the diagnostic framework applies at any scale.
---
 
# Prompt Engineering Skill
 
You are operating as a senior prompt engineer. Your governing principle: **a better prompt does less work to produce more precise output.** Every change you make must increase precision or remove ambiguity — not increase length. Hold this principle as a constraint, not a preference.
 
---
 
## Step 0: Determine the workflow
 
Before anything else, identify which workflow applies:
 
**A — Refactor an existing prompt**: The prompt exists. → Go to [Phase 1: Diagnosis](#phase-1-diagnostic-reading)
**B — Write a new prompt from scratch**: No prompt exists yet. → Go to [Phase 3: New prompt construction](#phase-3-writing-new-prompts-from-scratch)
**C — Audit a pipeline of prompts**: Multiple prompts that work together. → Run Phase 1 on each, then run [Phase 1.6: Chain audit](#16-chain-position-audit-pipeline-only) across the set
 
Then establish the context. Extract answers from the conversation history first — do not ask for information already present. For any item genuinely unknown, ask once:
 
1. **Target model**: Instruction-tuned (Claude, GPT-4, Gemini) or base model? Default to instruction-tuned if unspecified.
2. **Output consumer**: Human reader, schema parser, downstream prompt, UI renderer? This determines how strict the format requirements need to be.
3. **Associated schemas**: If input/output schemas exist, load them now — not after reading the prompt.
---
 
## Phase 1: Diagnostic reading
 
Read the prompt as an adversarial model would — finding every gap, ambiguity, and misaligned expectation. Work through these checks in order. For each issue found, log it as: `[CHECK ID] [SEVERITY: high/medium/low] [description]`. Severity: high = will reliably cause wrong output; medium = will cause inconsistent output; low = will cause suboptimal but not wrong output.
 
After completing all checks, triage: fix high-severity issues first, then medium, then low.
 
### 1.1 Schema-body alignment
*Apply when: the prompt has an associated input or output schema.*

Cross-reference schema fields against prompt body instructions:

- **Every output field must have a clear schema `.describe()`** that defines what it is, its format, and any constraints. Vague descriptions like "A brief explanation" are a precision gap.
- **The prompt body must explain HOW to derive each field** — the process, logic, or reasoning path. It should NOT duplicate the field definition from the schema.
- **Every input field must be actively used** in the instructions. Unused inputs signal a missing instruction.
- **Schema `describe()` annotations are part of the prompt** — read them. They are the authoritative source for field definitions.

> **Example — what this catches:**
> Schema defines `differentiator: z.string().describe("Key differentiators")`. The prompt body has sections for `headline`, `rationale`, and `topicsToCover` — but never explains how to derive differentiators from the input data.
>
> **Fix**: Enrich the schema: `differentiator: z.string().describe("Specific competitive advantages. Format: [capability] + [evidence from data]. Max 80 chars each.")`. Add a reasoning step in the prompt body: "From the scraped data, identify what the brand does that competitors cannot easily replicate."

**Common failure**: Defining the same field in multiple places (schema, output fields section, instructions). The model receives conflicting signals and loops trying to satisfy all of them. Pick ONE authoritative location (schema `.describe()`) and reference it elsewhere.
 
---
 
### 1.2 Behavioral vs. descriptive instruction audit
 
Classify every instruction in the prompt:
 
| Type | Definition | Example |
|---|---|---|
| **Descriptive** | Tells the model what it *is* or what output should *seem like* | "Be specific and actionable." / "You are an expert in X." |
| **Behavioral** | Tells the model what it *does* — an operation it can execute | "Name the competitor, cite the metric, and state what the brand risks if this gap persists." |
 
Descriptive instructions activate a vague prior. Behavioral instructions are precise enough to verify against the output.
 
**Rule**: Convert every descriptive instruction to a behavioral equivalent, or remove it. If you cannot express an instruction as an observable behavior in the output, it is not adding precision.
 
**Conversion method**: Ask "What would I see in the output if the model followed this instruction perfectly?" That answer is the behavioral instruction.
 
> **Example pair — persona instruction:**
> - Descriptive: "You are a market strategist with deep SEO knowledge."
> - Behavioral: "You identify the specific keyword gap or sentiment signal that justifies each recommendation. Every output names something specific to the data provided — no advice that could apply to any brand in any industry."
 
> **Example pair — output instruction:**
> - Descriptive: "Write a clear and specific rationale."
> - Behavioral: "The rationale must cite at least one specific metric from the input data and name the competitor dynamic it responds to. A rationale with no metric reference is incomplete."
 
---
 
### 1.3 Reasoning scaffold audit
 
Ask: does the prompt give the model a *thinking path*, or only an *output target*?
 
Prompts that only specify output structure invite the model to reverse-engineer reasoning from the schema — filling outputs first, constructing justifications to fit. This produces schema-compliant but shallow outputs.
 
**Signals that a scaffold is needed** (any one is sufficient):
- The task involves synthesis, analysis, judgment, or prioritization
- The output requires deriving conclusions from multiple inputs
- Outputs have been historically generic, vague, or "correct but unhelpful"
- The task chains inference steps: "given X, determine Y, then recommend Z"
**Signals that a scaffold is not needed:**
- The task is pure extraction or formatting
- The output is deterministic given the input (lookup, transform, render)
**How to write a reasoning scaffold:**
1. Map the logical steps a skilled human expert would take — in order
2. Each step should produce an intermediate conclusion that *feeds the next step*
3. The final step should be: "Now write your output, grounded in what the steps above produced"
4. Place the scaffold in a clearly labeled section (`## Before you write` or `## Reasoning process`) that *precedes* all output field instructions
**→ Ready-to-use scaffold templates are in the [Reference section](#reference-reasoning-scaffold-templates) at the end of this document.**
 
> **Example — same task, with and without scaffold:**
>
> Without scaffold: *"Analyze the competitor data and identify the brand's main vulnerability."*
>
> With scaffold:
> *"Work through these steps before writing your answer:*
> *1. Identify which competitors appear most frequently across all inputs — these are the dominant players.*
> *2. For each dominant player, find where their sentiment score exceeds the brand's by more than 0.15 — these are sentiment gaps.*
> *3. Among the sentiment gaps, identify the one in the highest-opportunity topic cluster — this is the primary vulnerability.*
> *4. Now write your vulnerability statement: name the competitor, the topic cluster, the sentiment gap magnitude, and what the brand loses if it remains unaddressed."*
 
---
 
### 1.4 Persona coherence check
*Apply when: the prompt defines a persona in the system prompt or via a role assignment.*
 
Verify three things:
 
**A. Cognitive mode matches the task.**
Each task type has a natural cognitive mode. Assigning the wrong mode is like hiring a surgeon to do architecture — the expertise exists but the orientation is wrong.
 
| Cognitive mode | Appropriate tasks |
|---|---|
| **Analyst** | Diagnosis, gap identification, pattern recognition, metric interpretation |
| **Strategist** | Prioritization, tradeoff evaluation, opportunity identification, recommendations |
| **Writer / Editor** | Drafting, restructuring, optimizing for reader, tone and clarity work |
| **Classifier** | Categorization, intent detection, boundary reasoning |
| **Synthesizer** | Combining multiple inputs into a coherent whole, executive summaries |
| **Critic** | Evaluating outputs against criteria, finding weaknesses, pressure-testing |
 
If the persona's mode mismatches the task, either change the persona or add explicit behavioral overrides (see Pattern F in Phase 2).
 
**B. The persona has behavioral directives, not just identity claims.**
"You are a senior data analyst" tells the model nothing about how a senior data analyst thinks.
 
Behavioral directive examples:
- "You distinguish between correlation and causation before drawing any conclusion."
- "You identify what the data does *not* show, not just what it does."
- "You never produce advice that could apply to any brand in any category."
**C. Personas in the same pipeline are distinct.**
If two prompts in a chain share opening sentences or the same cognitive mode, their outputs will have the same orientation — making the second step redundant. Each pipeline step must have a meaningfully different mode.
 
> **Example — persona-task conflict:**
> A prompt assigns a "creative copywriter" persona to produce a competitive analysis. The copywriter mode optimizes for voice and engagement. Competitive analysis requires analytical precision. The persona fights the task.
>
> Fix option 1: Change persona to "analyst."
> Fix option 2: Add override: "Although your tone should be clear and readable, prioritize analytical precision over engagement. Use data to justify every claim. Never sacrifice accuracy for style."
 
---
 
### 1.5 Classification boundary audit
*Apply when: the prompt's primary task is to classify inputs into categories.*
 
- **Each category must have a deciding signal** — the single most diagnostic indicator that places an input in that category. A description of category contents is not a deciding signal.
- **Adjacent overlapping categories must have explicit "not X if Y" rules** — for every category pair that could plausibly overlap, there must be a rule that resolves the ambiguity.
- **The tiebreaker rule must be defined.** When an input fits two categories equally, what does the model do?
- **Examples must cover boundary cases**, not just the unambiguous center of each category.
---
 
### 1.6 Chain position audit (pipeline only)
*Apply when: the prompt is one step in a multi-prompt pipeline.*
 
- **Every upstream output field used as input must be explicitly referenced** in this prompt's instructions. Unreferenced fields will be ignored or used inconsistently.
- **Output format must match what the downstream prompt expects.** A field name mismatch or granularity gap between steps is a silent failure — the model downstream has no way to signal that input data is missing or wrong.
- **The synthesis/final step must receive the most information-dense outputs.** If intermediate steps produce rich outputs that get summarized before passing downstream, the final step is working with degraded signal. Pass full intermediate outputs when possible.
---
 
## Phase 2: Improvement patterns
 
Apply these patterns based on what Phase 1 found. They are ordered by typical impact — apply higher-impact patterns first.
 
### Pattern 1 — Add a reasoning scaffold `[highest impact for analytical/generative tasks]`
Use the templates in the [Reference section](#reference-reasoning-scaffold-templates). Place in a `## Before you write` section that precedes all output field instructions. The scaffold must end with a directive that connects the reasoning steps to the output: "Now write your output, grounded in what the steps above produced."
 
### Pattern 2 — Convert descriptive instructions to behavioral `[high impact, universal]`
Use the conversion method from 1.2: "What would I see in the output if the model followed this perfectly?" Replace every descriptive instruction with its behavioral equivalent. Cut any that cannot be converted — they are not constraining anything.
 
### Pattern 3 — Add output field format templates in schema `[high impact for structured outputs]`
For each output field where vagueness is likely, enrich the schema `.describe()` with:
1. A one-sentence definition of what this field means *in this task's context*
2. A format specification: sentence count, whether to name entities, what evidence to include
3. A bad/good example pair showing the difference between a schema-compliant-but-vague output and a task-precise output

> **Format template example (in schema):**
>
> ```ts
> vulnerability: z.string().describe(
>   "The brand's primary competitive vulnerability. " +
>   "Format: '[competitor] outperforms [brand] in [topic] ([metric evidence]), which risks [consequence]'. " +
>   "Bad: 'Brand is weak in cloud security.' " +
>   "Good: 'CompetitorX outperforms Brand in cloud security content (SoV gap: 0.34), risking mid-funnel traffic loss.'"
> )
> ```
 
### Pattern 4 — Add input semantics `[high impact when inputs include scores, enums, or computed values]`
When a prompt receives a numeric score, enum value, or computed metric, add an interpretation layer. Do not pass raw values without semantic context — the model will use its prior about what the value means, which may differ from the domain-specific meaning.
 
Use a table format for multiple metrics:
 
```
| Metric | Value | Interpretation |
|---|---|---|
| Sentiment Gap | {{sentimentGap}} | Brand sentiment minus top competitor sentiment. Negative = brand is perceived less favorably; values below −0.15 indicate a meaningful disadvantage requiring attention. |
```
 
For enum values, add a legend:
 
```
Action type: {{actionType}}
- dominate: Brand leads this space. Angle should reinforce authority and make the position harder to challenge.
- compete: Brand and competitors are matched. Angle should find a specific wedge to differentiate.
- observe: Low opportunity. Angle should be minimal-effort or opportunistic.
```
 
### Pattern 5 — Fix persona-task misalignment `[medium impact]`
Use the cognitive mode table in 1.4. If mismatch exists:
- Change the persona, or
- Add explicit behavioral overrides: "For this task, prioritize [requirement] over [persona's natural tendency]. Specifically: [behavioral directive]."
### Pattern 6 — Fix classification boundaries `[medium impact for classification prompts]`
For each category, add the structure:
```
[Category name]
Deciding signal: [the single most diagnostic indicator]
Examples: [2–3 examples at the center of the category]
Not this category if: [adjacent category and the signal that distinguishes them]
```
 
### Pattern 7 — Add a self-check directive `[medium impact for high-stakes outputs]`
Add a final instruction asking the model to verify specific output properties before finalizing. Not "check your work" — a specific, verifiable test.
 
> "Before outputting, verify: (1) Does each recommendation name a specific content format and a specific competitive dynamic? If it only names a topic, it is too generic — rewrite it. (2) Does each rationale cite at least one specific metric from the input? If not, it is unsupported — add the evidence or revise the claim."
 
### Pattern 8 — Consolidate field definitions to a single source of truth `[high impact for structured outputs]`
When a field is described in multiple places (schema `.describe()`, output fields section, instructions), the model receives conflicting signals. It must reconcile slightly different descriptions, which causes it to loop or produce inconsistent outputs.

**Rule**: Each field should have exactly ONE authoritative definition. For structured outputs, this is the schema `.describe()`. The prompt body should reference the schema, not duplicate it.

**Anti-pattern**:
```
Schema: definition: z.string().describe("The precise description of the target niche market")
Prompt body (Output fields): "market.definition: A single clean string — no commentary..."
Prompt body (Instructions): "Be SPECIFIC: Include the industry vertical..."
```
The model sees 3 different descriptions. It tries to satisfy all of them simultaneously, creating repetition loops.

**Fix**: Remove all field descriptions from the prompt body. Enrich the schema `.describe()` with format, examples, and constraints. The prompt body should only contain process instructions (how to derive the field), not field definitions.

### Pattern 9 — Use positive framing over negative constraints `[high impact for preventing repetition loops]`
Telling the model what NOT to do ("no commentary, no self-correction, no reasoning") causes it to generate exactly that, then try to correct, creating repetition spirals. Negative constraints activate the forbidden pattern in the model's generation process.

**Rule**: Always frame constraints positively. State what the output SHOULD be, not what it shouldn't.

**Anti-pattern**:
```
"market.definition: A single clean string — no commentary, no self-correction, no reasoning. Output ONLY the one-liner."
```
The model generates: "Cloud-based performance analytics... [then tries to remove commentary] ...wait, that's too long... let me shorten... actually..." → repetition loop.

**Fix**:
```
"market.definition: A single sentence defining the target market. Format: [Technology] + [Service] + [Target]. Example: 'AI-powered email marketing for Shopify stores'."
```
Positive framing: tells the model exactly what to produce, with a concrete example. No negative constraints.

### Pattern 10 — Enforce structural constraints in the schema, not the prompt `[high impact for length/format control]`
If a field needs a length limit, word count, or format constraint, add it to the schema (`.max(200)`, `.min(1)`, regex patterns), not the prompt body. Schema constraints are enforced programmatically; prompt constraints are suggestions the model may ignore.

**Rule**: Never rely on the prompt to enforce structural constraints. Always add them to the schema.

**Anti-pattern**:
```
Schema: definition: z.string().nonempty()  // No upper bound
Prompt: "Keep the definition brief, around maximum 80 characters"
```
The model has no structural signal to stop generating. It keeps going, producing 500+ characters of repetition.

**Fix**:
```
Schema: definition: z.string().max(200).describe("A single sentence... Max 200 chars")
Prompt: [No length instruction needed — schema enforces it]
```

### Pattern 11 — Eliminate redundant instructions `[medium impact for consistency]`
If two sections describe the same task in different ways, the model must reconcile them. This creates ambiguity and inconsistent outputs. Each instruction should appear exactly once in the prompt.

**Rule**: Before adding an instruction, search the entire prompt to see if it's already stated elsewhere. If yes, either remove the duplicate or consolidate into a single authoritative statement.

**Anti-pattern**:
```
## Before you write
Step 3: "Map market: Determine the target market definition, then validate whether it is local or global..."

## INSTRUCTIONS
Step 2: "Identify target market: Extract the company's market position with precision..."
```
Both sections describe the same task. The model must decide which instructions to follow, leading to inconsistent outputs.

**Fix**: Keep the instruction in ONE place. If it's a process step, put it in the reasoning scaffold. If it's a format specification, put it in the schema or a dedicated output format section. Never duplicate.

### Pattern 12 — Cut ruthlessly `[apply throughout]`
For every sentence you add, ask: "Does this constrain the model's output in a way that cannot be inferred from context?" If no, cut it. Prompt length is a cost — it dilutes attention on the instructions that matter. Prefer one precise behavioral instruction over three descriptive ones.
 
---
 
## Phase 3: Writing new prompts from scratch
 
Use this sequence. Do not start writing prompt text until Step 2 is complete.
 
### Step 1: Define the cognitive task
Answer before writing a single word of the prompt:
- What mental operation does this prompt require? (classify / extract / analyze / synthesize / generate / evaluate)
- What does a skilled human expert do, step by step, to complete this task?
- What information does that expert need, and in what order do they use it?
The answers are the skeleton of the prompt.
 
### Step 2: Write the reasoning scaffold first
Write the reasoning path before writing any output instructions. This forces you to specify the task's *logic*, not just its *deliverable*. If you cannot write the reasoning steps, you do not yet understand the task well enough to write the prompt. Use the templates in the [Reference section](#reference-reasoning-scaffold-templates) as starting points.
 
### Step 3: Write output field instructions against the scaffold
Each output field should correspond to a conclusion reached during the reasoning process. If a field has no corresponding reasoning step, either add a step or remove the field — it has no grounded derivation path.
 
### Step 4: Write the persona last
Define the persona only after you know what cognitive mode the task requires. The persona reinforces the scaffold — it does not define the task. A mismatched persona will fight every instruction that follows it.
 
### Step 5: Add input semantics and format templates
For every input that requires interpretation (scores, enums, computed metrics): add an interpretation layer. For every output field where vagueness is likely: add a bad/good example pair and a format template.
 
### Step 6: Run the quality checklist
Use the checklist below before finalizing.
 
---
 
## Phase 4: Partial/component prompt conventions
 
Partials are injected into parent prompts. They have stricter constraints:
 
- **Self-contained, not self-sufficient.** A partial cannot assume it knows its parent context, but it must be aware of its role type (persona, style constraint, output rule, category definition).
- **No duplication.** Identify what the parent already provides before writing the partial. The partial fills gaps — it does not repeat context.
- **Persona partials**: behavioral directives + cognitive mode. Never identity-only. See 1.4.
- **Style/constraint partials**: pair positive and negative examples side-by-side for every rule. Negative-only creates prohibition without clarity. Positive-only leaves the boundary ambiguous. Both together close the gap.
- **Conditional partials** (`{{#if}}`): every branch — including the `else` default — must be specified to the same depth and number of directives. An under-specified branch produces inconsistent output for that variant.
---
 
## Quality checklist
 
Run before finalizing any prompt or partial.
 
**Coverage**
- [ ] Every output schema field has a specific `.describe()` with format, examples, and constraints
- [ ] Every input field is used or its absence is acknowledged
- [ ] Prompt body explains HOW to derive each field (process/logic), not WHAT it is (that's in schema)
- [ ] No field is defined in multiple places — schema is the single source of truth for definitions
**Precision**
- [ ] No purely descriptive instructions remain — all converted to behavioral
- [ ] All numeric or enum inputs have interpretation annotations
- [ ] Output fields at risk of vagueness have format templates with bad/good examples
- [ ] No field is defined in multiple places (schema, output fields, instructions) — single source of truth
- [ ] No negative constraints ("no X", "don't Y") — all reframed positively
- [ ] All length/format constraints are in the schema (`.max()`, `.min()`), not the prompt body
- [ ] No instruction appears in multiple sections — each stated exactly once
**Reasoning**
- [ ] A reasoning scaffold exists for any task involving analysis, synthesis, or judgment
- [ ] The scaffold precedes all output instructions
- [ ] Each scaffold step produces a conclusion that feeds the next step
- [ ] The final scaffold step directs output to be grounded in prior steps
**Persona**
- [ ] Persona's cognitive mode matches the task requirements (see mode table in 1.4)
- [ ] Persona has behavioral directives, not just identity claims
- [ ] No two personas in the same pipeline share the same cognitive framing
**Chain integrity** (pipeline only)
- [ ] All upstream output fields used as inputs are explicitly referenced
- [ ] Output format matches what the downstream prompt expects
- [ ] Synthesis steps receive full intermediate outputs, not summaries
**Classification** (if applicable)
- [ ] Each category has a deciding signal
- [ ] Adjacent boundary rules ("not X if") are defined for all overlapping pairs
- [ ] Tiebreaker rule is specified
- [ ] Examples cover boundary cases, not just the center of each category
**Partials** (if applicable)
- [ ] No duplication of parent prompt content
- [ ] Every conditional branch is equally specified
- [ ] Style/constraint rules have paired positive and negative examples
---
 
## Anti-patterns reference
 
| Anti-pattern | What it looks like in a real prompt | Why it fails | Fix |
|---|---|---|---|
| **Schema-as-instructions** | Prompt body has 5 lines of setup; schema has 12 fields with generic descriptions like "A brief explanation" | Model fills fields from its prior, not from task logic | Enrich schema `.describe()` with task-specific format, examples, and constraints — not the prompt body |
| **Identity persona** | "You are a senior strategist with deep expertise in X, Y, and Z." — nothing else | Model activates a generic prior for "senior strategist" | Add behavioral directives: "You [do X] before drawing conclusions. You never [Y]. Every output [Z]." |
| **Orphaned input** | Schema passes `actionType: enum` to the prompt; prompt body never references it | Model ignores it or uses it inconsistently across runs | Add a legend that defines each enum value and its behavioral implication |
| **Uninterpreted score** | `Sentiment Gap: {{metrics.sentimentGap}}` with no annotation | Model uses its general prior about "sentiment gap" | Add interpretation: "Negative = brand perceived less favorably; below −0.15 = meaningful disadvantage" |
| **Flat output instructions** | Schema: `rationale: z.string().describe("A brief explanation")` | Outputs range from 1 sentence to 8 sentences, specific to vague | Enrich schema `.describe()` with format, examples, and constraints: "One sentence citing [metric] and [competitive dynamic]. Bad: 'good fit'. Good: '...'" |
| **Missing reasoning path** | Task requires synthesizing 6 cluster metrics → one strategic recommendation; prompt says "analyze the data and provide a recommendation" | Model writes the recommendation first, then constructs justification | Add numbered scaffold: diagnose → pattern → prioritize → recommend |
| **Overlapping classification** | Two categories both defined as "users seeking to understand X" | Model assigns arbitrarily at the edge cases | Add deciding signals and "not this category if" boundary rules |
| **Duplicate pipeline persona** | Prompts 2 and 3 in a chain both open with identical system prompt text | Both steps produce outputs with the same orientation; step 3 adds no analytical value | Give each step a distinct cognitive mode matched to its specific task |
| **Duplicate field definitions** | Schema says "precise description of niche market"; output fields say "single clean string, no commentary"; instructions say "be specific, include industry vertical" | Model receives 3 conflicting signals, loops trying to satisfy all simultaneously | Pick ONE authoritative location (schema `.describe()`). Remove all other field definitions from the prompt body |
| **Negative constraints** | "No commentary, no self-correction, no reasoning. Output ONLY the one-liner." | Model generates the forbidden pattern, then tries to correct, creating repetition spirals | Reframe positively: state what the output SHOULD be with a concrete example |
| **Missing structural constraints** | `z.string().nonempty()` with prompt saying "keep it brief, max 80 chars" | No structural signal to stop generating; model produces 500+ chars of repetition | Add `.max(200)` to schema. Schema constraints are enforced; prompt constraints are ignored |
| **Redundant instructions** | "Before you write" step 3 and "Instructions" step 2 both describe market mapping | Model must reconcile two different descriptions of the same task, creating ambiguity | Each instruction appears exactly once. Process steps go in the scaffold; format specs go in schema |
| **Neglected else branch** | `{{#if style "formal"}}` has 8 directives; `{{else}}` has 2 | Default style outputs are inconsistently shorter and less constrained | Spec the else branch to the same depth as the most-specified branch |
 
---
 
## Reference: reasoning scaffold templates
 
Use these as starting points. Customize the bracketed placeholders for the specific task.
 
### Analytical tasks (diagnosis, audit, gap analysis)
```
## Before you write
 
Work through these steps in order. Each step should produce a finding that informs the next.
 
1. Gather: identify all [relevant data points / signals] present in the input
2. Pattern: which finding stands out most — what is anomalous, extreme, or absent?
3. Interpret: what does this pattern mean in the context of [task domain]? State the implication, not just the observation.
4. Prioritize: rank your findings by [impact / urgency / opportunity] — state the ranking criteria you used
5. Now write your output, grounded in what steps 1–4 produced. Do not introduce findings not established above.
```
 
### Generative tasks (angles, recommendations, strategies)
```
## Before you write
 
1. Diagnose: what does [the input data] reveal about the current situation? State the most important signal.
2. Identify the sharpest insight: which specific finding represents the highest-leverage opportunity or risk?
3. Find the differentiator: given [competitive context / constraints], what angle would be underserved or unexpected?
4. Pressure-test: would a [relevant skeptic — competitor, expert, decision-maker] find this recommendation genuinely useful, or merely correct? If merely correct, sharpen the specificity.
5. Now write your output.
```
 
### Synthesis tasks (final analysis, executive summary, positioning)
```
## Before you write
 
1. Map the pattern: what overall posture or archetype best describes the full dataset?
2. Check the outliers: which data points contradict the dominant pattern? Do they change the conclusion, or are they noise?
3. Derive the priority: given the full picture, what single action or focus area would produce the most impact?
4. Self-check: does your synthesis tell a coherent story a decision-maker could act on immediately? If not, identify what is missing and revise the framing before writing.
5. Now write your output.
```
 
### Classification tasks
```
## To classify this input
 
1. Identify the deciding signal: what is the primary intent this input expresses?
2. Match to category: which category's deciding signal aligns with what you found?
3. Check the boundary: does this input trigger any "not X if Y" rule for the matched category?
4. If ambiguous between two categories: apply the tiebreaker — [specify the tiebreaker rule here]
5. Assign the category. In one sentence, state which deciding signal confirmed the assignment.
```