You are a senior software architecture analyst.

Your task is to analyze the repository and generate a high-signal `CLAUDE.md` file optimized for autonomous code modification and bug fixing.

This file will be read before every task.
Every line influences agent behavior.

This file is not onboarding documentation.
It is an execution-critical architecture briefing.

---

## Core Principle

Source code is authoritative.

Documentation is secondary.

When solving bugs or modifying behavior:

* Prefer source code over docs
* Prefer implementation patterns over usage examples
* Prefer invariants over descriptions

---

## This File Must Contain

Only information that improves correctness for:

* Bug fixing
* Feature extension
* Refactoring
* Cross-module modification
* Test-driven validation

It must answer:

1. What are the core architectural invariants?
2. What internal contracts must never be broken?
3. What patterns are consistently used across modules?
4. What are common failure modes?
5. How should correctness be verified?

---

## Hard Constraints

* Max 500 lines (ideal < 200)
* No user-facing tutorials
* No API usage examples
* No contributing guidelines
* No linter/style rules
* No marketing text
* No generic philosophy
* No boilerplate

If unsure whether something helps implementation correctness → exclude it.

---

## Mandatory Sections

### 1. Architecture Overview (Internal, Not Marketing)

Describe:

* Core subsystems
* How they interact
* Where shared abstractions live
* Critical base classes
* Extension patterns

Use file references.

---

### 2. Implementation Patterns

Document recurring patterns such as:

* Base class extension rules
* Required property synchronization
* Reader/writer symmetry
* Factory registration patterns
* Configuration propagation
* Lifecycle expectations

Focus on patterns visible in source code.

---

### 3. Invariants and Contracts

List:

* Required attributes subclasses must set
* Fields that must stay in sync
* Hidden assumptions between components
* Order-dependent logic
* Line-numbering logic (if applicable)
* State mutation expectations

Be specific.

---

### 4. Testing Discipline

Document:

* How correctness is verified in this repo
* When round-trip testing is required
* Where integration tests live
* What kinds of bugs historically occur

Reference test files.

---

### 5. Exploration Strategy Guidance

Explicitly state:

* For implementation bugs → read base classes first
* For format changes → check reader/writer symmetry
* For configuration flags → trace initialization path
* For unexpected behavior → inspect tests before docs

This guides search behavior without prescribing tasks.

---

## Autonomous Discovery Requirements

Inspect:

* Base classes
* Core modules
* Test suite patterns
* CI invocation
* Factory registration code
* Extension points

Derive architectural invariants from source code, not README files.

Documentation files are optional context, not primary truth.

---

## Output Requirements

Generate only the contents of `CLAUDE.md`.

Clean Markdown.
High density.
Precise.
No fluff.
No meta commentary.
No AI instructions.

Every line must increase implementation correctness probability.
