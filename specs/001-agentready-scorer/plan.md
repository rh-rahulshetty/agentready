# Implementation Plan: AgentReady Repository Scorer

**Branch**: `001-agentready-scorer` | **Date**: 2025-11-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-agentready-scorer/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a command-line tool called "agentready" that assesses git repositories against 25 evidence-based attributes for AI-assisted development readiness. The tool analyzes repository quality across categories like documentation, code quality, testing, structure, CI/CD, and security, then generates dual-format reports (interactive HTML + version-control-friendly Markdown) with specific findings, evidence, remediation guidance, and an overall agent-readiness score with certification level (Platinum/Gold/Silver/Bronze).

Technical approach: Library-first architecture with standalone assessment modules for each attribute category, CLI wrapper orchestrating the scan workflow, bundled research data with update capability, and self-contained HTML report generation with embedded interactivity.

## Technical Context

**Language/Version**: Python 3.11+ (only N and N-1 versions supported per constitution)
**Primary Dependencies**:
- Click (CLI framework)
- Jinja2 (HTML template rendering)
- PyYAML (configuration file parsing)
- gitpython (repository introspection)
- Language-specific analyzers: radon (Python complexity), lizard (multi-language complexity)

**Storage**: File-based (no database required)
- Bundled research report (agent-ready-codebase-attributes.md)
- Optional user configuration file (.agentready-config.yaml)
- Generated reports (.agentready/ directory)

**Testing**: pytest with pytest-cov for coverage tracking
- Unit tests for individual attribute assessors
- Integration tests for full scan workflows
- Contract tests for report schemas

**Target Platform**: Cross-platform CLI (Linux, macOS, Windows via Python)
**Project Type**: Single project (CLI tool with library modules)
**Performance Goals**:
- Complete assessment in <5 minutes for repositories with <10k files
- Deterministic scoring (consistent results across runs)
- Minimal memory footprint (<500MB for typical repositories)

**Constraints**:
- Offline-capable (internet only for research report updates)
- Self-contained HTML reports (no external CDN dependencies)
- Graceful degradation (partial results if some checks fail)
- No modification of scanned repository (read-only analysis)

**Scale/Scope**:
- 25 attribute assessors (one per research report attribute)
- Support 5+ programming languages (Python, JavaScript, TypeScript, Go, Java minimum)
- Handle repositories up to 100k files (with performance degradation warning)

### Research Report Update Mechanism

**Per FR-023**: Tool must support updating the bundled research report.

**Versioning Philosophy**: agentready releases are bundled with a specific research report version. The tool and research report are versioned together (e.g., agentready v1.2.0 includes research report v1.2.0).

**Implementation Design**:

1. **Bundled Report**:
   - Research report shipped with tool installation in `src/agentready/data/agent-ready-codebase-attributes.md`
   - Tool version and research version always match in releases
   - Users can always rely on stable, tested research content

2. **Custom Research Reports**:
   - Users can point to custom research reports:
     ```bash
     agentready --research-file /path/to/custom-research.md
     agentready --research-file https://example.com/custom-research.md
     ```
   - Enables organizations to customize criteria for internal standards
   - Custom reports must pass validation (per FR-024)

3. **Update Command** (explicit opt-in only):
   ```bash
   agentready --update-research
   ```

4. **Update Source**:
   - Primary: `https://github.com/ambient-code/agentready/raw/main/src/agentready/data/agent-ready-codebase-attributes.md`
   - Downloads latest research report from main branch
   - User explicitly opts in to update

5. **Update Process** (atomic):
   ```
   a. Download new version to temp file
   b. Validate structure (per FR-024):
      - Check for required metadata (version, date)
      - Verify 25 attributes present
      - Validate Markdown format
      - Parse successfully with research_loader.py
   c. If valid:
      - Backup current: agent-ready-codebase-attributes.md → .md.backup
      - Atomic rename: temp → agent-ready-codebase-attributes.md
      - Remove backup on success
      - Display: "Updated research report from vX.Y.Z to vA.B.C"
   d. If invalid:
      - Delete temp file
      - Restore from backup if needed
      - Exit with error message and validation details
      - Keep current version intact
   ```

6. **Version Tracking**:
   - Research report includes metadata header:
     ```markdown
     ---
     version: 1.2.0
     date: 2025-11-20
     ---
     ```
   - Tool displays current research version:
     ```bash
     agentready --research-version
     # Output: Research report v1.2.0 (2025-11-20)
     ```

7. **Offline Behavior**:
   - If network unavailable: "Cannot reach update server. Using bundled version v1.0.0"
   - If update fails: "Update failed (validation error). Using current version v1.0.0"
   - Never leave tool in broken state
   - Always fall back to last known-good version

8. **Rollback**:
   ```bash
   agentready --restore-bundled-research  # Restore original from package
   ```
   - Restores research report from tool installation package
   - Useful if custom/updated research causes issues

**Error Handling**:
- Network timeout (30s): Graceful failure, keep current version
- Invalid format: Detailed validation error, rollback to previous
- Permission denied: Error with instructions to check file permissions
- Partial download: Checksum validation, retry or abort

**Testing** (integration test):
- Mock HTTP server with valid/invalid research reports
- Verify atomic updates (no partial writes)
- Test rollback on validation failure
- Confirm offline graceful degradation
- Verify version detection and display

**Philosophy**: Research report updates are explicitly opt-in only via `--update-research`. Standard workflow uses stable bundled version. Users who want latest research or custom criteria can update or override as needed.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Evidence-Based Design
✅ **PASS** - All 25 attributes derived from agent-ready-codebase-attributes.md research report with 50+ authoritative citations. Every assessment criterion grounded in documented findings from Anthropic, Microsoft, Google, ArXiv, IEEE/ACM sources.

### Principle II: Measurable Quality
✅ **PASS** - Each attribute has:
- Clear criteria (e.g., "CLAUDE.md exists and <1000 lines", "test coverage >80%")
- Automated tooling specified (radon, pytest-cov, gitpython, lizard)
- Quantifiable thresholds from research report
- Good/bad examples in research report

### Principle III: Tool-First Mindset
✅ **PASS** - Architecture follows library-first approach:
- Standalone assessor modules (importable, independently testable)
- CLI wrapper as thin orchestration layer
- Text-based I/O (repository path in → JSON/Markdown/HTML out)
- Each assessor usable without full agentready toolchain

### Principle IV: Test-Driven Development
✅ **PASS** - TDD workflow planned:
- Phase 2 will generate test tasks BEFORE implementation tasks
- Contract tests for report schemas (validate structure)
- Integration tests for scan workflows
- Unit tests for each attribute assessor
- Test coverage >80% enforced

### Principle V: Structured Output
✅ **PASS** - Dual-format output design:
- HTML for human consumption (interactive, visual)
- Markdown for version control/automation (parseable, diffable)
- Internal JSON representation (structured data model)
- Structured logging with progress indicators
- Error messages with context and guidance (FR-030)

### Principle VI: Incremental Delivery
✅ **PASS** - User stories prioritized for MVP-first:
- P1 (MVP): Core scoring engine → Delivers immediate value
- P2: Interactive HTML features → Enhanced UX
- P3: Remediation guidance → Actionable next steps
- P4: Version control integration → Team collaboration
- Each story independently testable and deployable

### Principle VII: Documentation as Code
✅ **PASS** - Documentation strategy:
- README with <5 minute quickstart (generated in Phase 1)
- CLAUDE.md with project context (to be created)
- Inline docstrings explaining "why" (assessment rationale)
- Examples in quickstart.md
- Research report citations preserved in all outputs

**GATE STATUS**: ✅ ALL PRINCIPLES PASS - Proceed to Phase 0 research

## Project Structure

### Documentation (this feature)

```text
specs/001-agentready-scorer/
├── spec.md              # Feature specification
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── assessment-schema.json    # Assessment data model JSON schema
│   ├── report-markdown-schema.md # Markdown report structure
│   └── report-html-schema.md     # HTML report structure/API
└── checklists/
    └── requirements.md  # Validation checklist
```

### Source Code (repository root)

```text
src/
├── agentready/
│   ├── __init__.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py           # Click-based CLI entry point
│   ├── assessors/
│   │   ├── __init__.py
│   │   ├── base.py           # Base assessor interface
│   │   ├── documentation.py  # Attributes 1.1-2.3 (CLAUDE.md, README, docstrings, ADRs)
│   │   ├── code_quality.py   # Attributes 3.1-3.4 (complexity, length, types, smells)
│   │   ├── structure.py      # Attributes 4.1-4.2 (layout, separation of concerns)
│   │   ├── testing.py        # Attributes 5.1-5.3 (coverage, naming, pre-commit)
│   │   ├── dependencies.py   # Attributes 6.1-6.2 (lock files, freshness/security)
│   │   ├── vcs.py            # Attributes 7.1-7.3 (commits, gitignore, templates)
│   │   ├── build.py          # Attributes 8.1-8.3 (one-command setup, docs, containers)
│   │   ├── errors.py         # Attributes 9.1-9.2 (error clarity, structured logging)
│   │   ├── api_docs.py       # Attributes 10.1-10.2 (OpenAPI, GraphQL)
│   │   ├── modularity.py     # Attributes 11.1-11.3 (DRY, naming, semantic files)
│   │   ├── cicd.py           # Attributes 12.1-12.2 (pipeline visibility, branch protection)
│   │   ├── security.py       # Attributes 13.1-13.2 (scanning, secrets)
│   │   └── performance.py    # Attribute 15.1 (benchmarks)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── repository.py     # Repository entity
│   │   ├── attribute.py      # Attribute definition
│   │   ├── assessment.py     # Assessment entity
│   │   ├── finding.py        # Finding entity
│   │   └── config.py         # Configuration model
│   ├── services/
│   │   ├── __init__.py
│   │   ├── scanner.py        # Orchestrates assessment workflow
│   │   ├── scorer.py         # Calculates weighted scores
│   │   ├── language_detector.py  # Detects repository languages
│   │   └── research_loader.py    # Loads bundled/updated research report
│   ├── reporters/
│   │   ├── __init__.py
│   │   ├── base.py           # Base reporter interface
│   │   ├── markdown.py       # Markdown report generator
│   │   └── html.py           # HTML report generator (with embedded JS/CSS)
│   ├── templates/
│   │   └── report.html.j2    # Jinja2 template for HTML report
│   └── data/
│       ├── agent-ready-codebase-attributes.md  # Bundled research report
│       └── default-weights.yaml                 # Default tier-based weights
│
tests/
├── unit/
│   ├── test_assessors.py     # Individual assessor tests
│   ├── test_models.py        # Data model tests
│   ├── test_services.py      # Service layer tests
│   └── test_reporters.py     # Report generator tests
├── integration/
│   ├── test_scan_workflow.py      # End-to-end scan tests
│   ├── test_report_generation.py  # Dual-format report tests
│   └── test_cli.py                # CLI interface tests
└── contract/
    ├── test_assessment_schema.py  # JSON schema validation
    ├── test_markdown_schema.py    # Markdown structure validation
    └── test_html_schema.py        # HTML structure validation

pyproject.toml                # Project metadata, dependencies, build config
README.md                     # Project overview and quickstart
CLAUDE.md                     # Claude Code context file
.agentready-config.example.yaml  # Example configuration file
```

**Structure Decision**: Single project (Option 1) selected. This is a CLI tool with library modules, not a web/mobile application. The structure follows Python src-layout convention with clear separation between CLI (thin wrapper), core logic (assessors, services, models), and output (reporters). Tests mirror source structure for easy navigation.

## Complexity Tracking

> **No violations** - All constitution principles pass without requiring justification.
