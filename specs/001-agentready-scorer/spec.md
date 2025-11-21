# Feature Specification: AgentReady Repository Scorer

**Feature Branch**: `001-agentready-scorer`
**Created**: 2025-11-20
**Status**: Draft
**Input**: User description: "I want to build a tool that scores git repos based on the findings of this report: agent-ready-codebase-attributes.md. The goal is to prepare a git repo for introduction of agentic development patterns. The tools goal is to provide repo owners with a report and brief remediation plan for each item that requires remediation. the tool must be called agentready. use the content of the report to generate remediation plans etc. i want the report to be a single html file that is interactive. i also want a markdown version of the report to be generated. always generate both formats when the tool is run"

## Clarifications

### Session 2025-11-20

- Q: Where should the agentready tool save the generated HTML and Markdown reports? → A: `.agentready/` directory in repository root by default, with user-specified output directory via CLI flag as option
- Q: How does the agentready tool locate the agent-ready-codebase-attributes.md research report file? → A: Research report bundled with tool installation, with support for downloading latest version from URL/repository
- Q: What should happen if the tool cannot complete assessment for some attributes (e.g., missing analysis tools, permission errors)? → A: Complete available attributes, clearly flag failed/skipped attributes in report with reasons
- Q: What should the tool display to stdout/stderr during execution (before reports are generated)? → A: Summary progress by default, detailed real-time logging with verbose flag
- Q: How should attribute weights be determined for calculating the overall agent-readiness score? → A: Fixed weights based on research report tier system by default, with user-configurable weights via configuration file

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Score Repository Against Agent-Ready Criteria (Priority: P1)

A repository owner wants to assess how well their codebase is optimized for AI-assisted development. They run the agentready tool on their repository and receive a comprehensive score with specific findings across all 25 agent-ready attributes documented in the research report.

**Why this priority**: This is the core value proposition - without scoring and assessment, there is no actionable feedback. This alone provides immediate value by identifying gaps.

**Independent Test**: Can be fully tested by running the tool against any git repository and verifying it produces a score and identifies attribute compliance levels. Delivers a complete assessment without needing remediation features.

**Acceptance Scenarios**:

1. **Given** a git repository with various quality attributes, **When** user runs agentready tool on repository, **Then** tool analyzes all 25 attributes from the research report and produces an overall agent-readiness score
2. **Given** a repository missing CLAUDE.md file, **When** agentready scans the repository, **Then** tool correctly identifies this attribute as non-compliant and includes it in the assessment
3. **Given** a repository with 85% test coverage, **When** agentready evaluates test coverage attribute, **Then** tool correctly identifies this as meeting the >80% threshold and scores it positively
4. **Given** a repository with no lock files, **When** agentready checks dependency management, **Then** tool flags missing lock files and includes specific examples of what's missing
5. **Given** analysis is complete, **When** tool generates reports, **Then** both HTML and Markdown versions are created with identical content

---

### User Story 2 - View Interactive HTML Report (Priority: P2)

After running the assessment, the repository owner views an interactive HTML report that allows them to explore findings by category, filter by compliance level, and drill into specific attribute details with expandable sections.

**Why this priority**: Enhances usability and makes large amounts of assessment data digestible. Builds on P1 by improving how results are consumed.

**Independent Test**: Can be tested by generating and opening the HTML report in a browser, verifying interactive elements (collapsible sections, filters, sorting) work without requiring the scoring engine.

**Acceptance Scenarios**:

1. **Given** agentready has completed assessment, **When** user opens the HTML report in browser, **Then** report displays overall score prominently with visual indicators (color coding, progress bars)
2. **Given** HTML report is displayed, **When** user clicks on an attribute category (e.g., "Documentation Standards"), **Then** section expands to show detailed findings for all attributes in that category
3. **Given** report shows multiple failing attributes, **When** user applies "show only failures" filter, **Then** report hides passing attributes and displays only those requiring remediation
4. **Given** an attribute is marked as failing, **When** user views that attribute in report, **Then** specific evidence is shown (e.g., "File size: src/large_module.py is 847 lines, exceeds 300 line limit")

---

### User Story 3 - Receive Remediation Guidance (Priority: P3)

For each attribute that fails compliance checks, the repository owner receives specific, actionable remediation steps based on the research report's recommendations, tooling suggestions, and examples.

**Why this priority**: Transforms assessment into action. Builds on P1 (scoring) and P2 (viewing) by providing the "what to do next" guidance.

**Independent Test**: Can be tested by reviewing remediation plans for known failing attributes and verifying they include specific tools, commands, examples, and links to documentation.

**Acceptance Scenarios**:

1. **Given** repository lacks CLAUDE.md file, **When** user views remediation for this attribute, **Then** guidance includes specific template, required sections, and example content
2. **Given** repository has cyclomatic complexity >25 in multiple functions, **When** user views remediation plan, **Then** plan lists specific files/functions exceeding threshold, suggests refactoring tools (radon for Python), and provides complexity reduction strategies
3. **Given** repository missing pre-commit hooks, **When** user views remediation, **Then** plan includes installation commands, sample configuration for the detected language, and links to pre-commit framework documentation
4. **Given** multiple attributes fail, **When** user views overall remediation plan, **Then** plan prioritizes fixes by impact tier (Tier 1 Essential → Tier 4 Advanced) as defined in research report

---

### User Story 4 - Read Markdown Report for Version Control (Priority: P4)

Repository owners want to track agent-readiness improvements over time by committing Markdown reports to version control, allowing them to compare scores across commits and share findings with team members in pull requests.

**Why this priority**: Enables continuous improvement tracking and team collaboration. Enhances existing features but not critical for initial value delivery.

**Independent Test**: Can be tested by generating Markdown report, committing it to git, and verifying it renders properly on platforms like GitHub with all tables, formatting, and links intact.

**Acceptance Scenarios**:

1. **Given** agentready completes assessment, **When** Markdown report is generated, **Then** report uses standard Markdown formatting (tables, headers, links) that renders correctly on GitHub
2. **Given** Markdown report from previous run exists, **When** user compares it with new report, **Then** differences in scores and attribute compliance are easily identifiable
3. **Given** report contains external citations, **When** user views Markdown report, **Then** all citations from research report are properly linked and attributions preserved

---

### Edge Cases

- What happens when repository is not a git repository (no .git directory)? Tool aborts with clear error message before assessment begins (validated per FR-017)
- How does tool handle extremely large repositories (>100k files)? Tool completes assessment but may exceed 5-minute target (SC-001 applies to <10k files only)
- What if repository uses multiple programming languages with different standards? Tool evaluates all detected languages and applies language-specific criteria per FR-013
- How does tool behave when file access is denied (permission errors)? Tool skips inaccessible files, continues assessment, flags permission issues in report per FR-026
- What if repository has no code files (documentation-only repos)? Tool completes assessment with many attributes marked N/A or failing, still produces valid report
- How does tool handle repositories with submodules or monorepo structures? Tool evaluates repository as-is, treating submodules as part of file structure
- What if HTML/Markdown report generation fails mid-process? Both reports fail atomically per FR-019, no partial report files left
- How does tool handle repositories with non-standard layouts that don't match any common pattern? Tool attempts best-effort pattern matching, may score lower on structure-related attributes

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Tool MUST be named "agentready" and executable from command line
- **FR-002**: Tool MUST accept a git repository path as input (current directory if not specified)
- **FR-003**: Tool MUST evaluate all 25 attributes defined in agent-ready-codebase-attributes.md research report
- **FR-004**: Tool MUST calculate an overall agent-readiness score (0-100) using weighted average of attribute scores (weights from FR-031/FR-032)
- **FR-005**: Tool MUST generate both HTML and Markdown format reports in a single execution
- **FR-006**: Tool MUST include specific evidence for each attribute evaluation (file names, line counts, measurements)
- **FR-007**: Tool MUST provide remediation guidance for each failing attribute, derived from research report recommendations
- **FR-008**: HTML report MUST be a single self-contained file (embedded CSS/JavaScript, no external dependencies)
- **FR-009**: HTML report MUST include interactive features (collapsible sections, filtering, sorting)
- **FR-010**: Markdown report MUST use standard GitHub-flavored Markdown for maximum compatibility
- **FR-011**: Tool MUST preserve all citations and attributions from the research report in generated reports
- **FR-012**: Tool MUST categorize attributes by tier (Tier 1 Essential through Tier 4 Advanced) as defined in research report
- **FR-013**: Tool MUST detect programming language(s) used in repository and apply language-specific criteria
- **FR-014**: Tool MUST handle repositories that partially meet attribute criteria (e.g., 50% test coverage) with proportional scoring
- **FR-015**: Remediation plans MUST include specific tooling recommendations, commands, and configuration examples from research report
- **FR-016**: Reports MUST include certification level (Platinum/Gold/Silver/Bronze) based on score ranges defined in research report
- **FR-017**: Tool MUST validate git repository before starting assessment (presence of .git directory)
- **FR-018**: Tool MUST provide progress indication showing completed attributes count during analysis (superseded by FR-028/FR-029 for specifics)
- **FR-019**: Both report formats MUST be generated atomically (both succeed or both fail)
- **FR-020**: Tool MUST save reports to `.agentready/` directory in repository root by default, creating directory if it doesn't exist
- **FR-021**: Tool MUST support `--output-dir` CLI flag allowing users to specify custom output directory for reports
- **FR-022**: Tool MUST bundle agent-ready-codebase-attributes.md research report as internal resource accessible without external dependencies
- **FR-023**: Tool MUST support updating bundled research report by downloading latest version from authoritative URL/repository
- **FR-024**: Tool MUST validate research report integrity (format, required sections) before using it for assessment
- **FR-025**: Tool MUST complete assessment for all evaluable attributes even if some attributes fail, rather than aborting entire scan
- **FR-026**: Tool MUST clearly indicate skipped or failed attributes in reports with specific failure reasons (e.g., "missing tool: radon", "permission denied: /protected/file")
- **FR-027**: Tool MUST calculate overall score based only on successfully evaluated attributes, excluding failed/skipped attributes from denominator
- **FR-028**: Tool MUST display summary progress to stdout by default (e.g., "Analyzing... [12/25 attributes complete]")
- **FR-029**: Tool MUST support `--verbose` CLI flag that enables detailed real-time logging of each file analyzed and check performed
- **FR-030**: Tool MUST output errors to stderr with clear error messages and context
- **FR-031**: Tool MUST use tier-based weighting system from research report by default (Tier 1 Essential weighted higher than Tier 4 Advanced)
- **FR-032**: Tool MUST support optional configuration file allowing users to customize attribute weights for organizational priorities
- **FR-033**: Tool MUST validate configuration file weights (all attributes present, weights are positive numbers, sum to meaningful total)

### Key Entities

- **Repository**: The target git repository being assessed, characterized by root path, detected languages, file structure, and git metadata
- **Attribute**: One of 25 agent-ready quality attributes from research report, including name, category, tier, weight, measurable criteria, and assessment method
- **Assessment**: Complete evaluation of repository, including overall score, certification level, per-attribute results, timestamp, and repository metadata
- **Finding**: Individual attribute evaluation result, including pass/fail status, measured value, threshold, evidence (specific files/metrics), and remediation guidance
- **Report**: Generated output document (HTML or Markdown), containing assessment results, formatted for specific use case (interactive viewing vs. version control)
- **Remediation Plan**: Actionable guidance for fixing failing attribute, including tools, commands, examples, and citations from research report
- **Citation**: Reference to authoritative source from research report, including author, title, publication, URL, and relevance to specific attribute

### Assumptions

- Repository owners have command-line access to their repositories
- Standard file system permissions allow reading repository files
- Repository follows conventional version control practices (not bare repository)
- Target audience has basic understanding of software quality metrics
- Internet connectivity optional for tool execution (required only for downloading updated research report)
- Reports will be viewed in modern browsers (for HTML) or platforms supporting GitHub-flavored Markdown
- Repository size is reasonable for local file system traversal (not petabyte-scale)
- Programming language detection can be performed via file extensions and common patterns

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can run complete assessment and generate both reports in under 5 minutes for repositories with <10k files
- **SC-002**: Tool correctly identifies compliance for all 25 attributes with >95% accuracy when validated against known test repositories
- **SC-003**: Generated HTML reports are fully functional without internet connectivity (no external CDN dependencies)
- **SC-004**: Markdown reports render correctly on GitHub, GitLab, and Bitbucket platforms without formatting issues
- **SC-005**: 90% of remediation plans include specific, executable commands or tool configurations that users can apply immediately
- **SC-006**: Overall agent-readiness scores align within 5 points when validated against manual evaluation by domain expert
- **SC-007**: Tool successfully handles repositories in at least 5 major programming languages (Python, JavaScript, TypeScript, Go, Java)
- **SC-008**: Users can identify top 3 priority improvements within 2 minutes of viewing report (via filtering/sorting features)
- **SC-009**: 100% of citations and attributions from research report are preserved in generated reports
- **SC-010**: Tool produces consistent scores when run multiple times on same repository (deterministic results)
