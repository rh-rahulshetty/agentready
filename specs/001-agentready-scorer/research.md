# Research: AgentReady Repository Scorer

**Phase**: 0 - Technical Research and Best Practices
**Date**: 2025-11-20
**Purpose**: Document technical decisions, rationale, and best practices for implementation

## 1. CLI Framework Selection

### Decision: Click

**Rationale**:
- Declarative command definition with decorators (clean, readable)
- Automatic help generation and input validation
- Native support for subcommands, options, and arguments
- Excellent error handling with user-friendly messages
- Wide adoption in Python CLI tools (pytest, pip, AWS CLI v2)

**Alternatives Considered**:
- `argparse` (stdlib): Too verbose, manual help text, basic validation
- `typer`: Type-hint based, but adds FastAPI dependency (unnecessary weight)
- `docopt`: String-based interface description (less type-safe)

**Best Practices**:
- Use `click.Path(exists=True, file_okay=False)` for repository path validation
- Implement `--verbose` with `click.option('--verbose', is_flag=True)`
- Use `click.echo()` for stdout (handles encoding across platforms)
- Use `click.secho()` for colored output (certification levels, progress)
- Implement progress bars with `click.progressbar()`

## 2. HTML Report Generation

### Decision: Jinja2 + Embedded CSS/JavaScript

**Rationale**:
- Jinja2 is industry-standard Python templating (Django, Flask)
- Template-based approach separates presentation from logic
- Easy to maintain and update report layout
- Embedding CSS/JS ensures offline functionality (FR-003)
- Single-file output simplifies distribution

**Alternatives Considered**:
- Direct HTML string building: Unmaintainable, error-prone
- WeasyPrint (HTML→PDF): Not required, HTML itself is deliverable
- React/Vue SPA: Requires build step, complex for static reports

**Best Practices**:
- Inline all CSS in `<style>` tag (avoid external stylesheets)
- Inline all JavaScript in `<script>` tag (no CDN dependencies)
- Use vanilla JavaScript (no jQuery/framework dependencies)
- Minify embedded CSS/JS for smaller file size
- Use CSS Grid/Flexbox for responsive layout (modern browser support)
- Implement collapsible sections with `<details>` and `<summary>` tags (native HTML5)
- Add `data-*` attributes for JavaScript hooks (clean separation)

**Interactive Features Implementation**:
- Filtering: JavaScript array `.filter()` on attribute findings
- Sorting: JavaScript array `.sort()` with custom comparators
- Collapsible sections: CSS `:target` pseudo-class + JavaScript event listeners
- Progress bars: CSS `width` percentage on div elements
- Color coding: CSS classes based on score thresholds

## 3. Language Detection Strategy

### Decision: File Extension Analysis + gitignore Awareness

**Rationale**:
- File extensions are reliable primary indicator (.py, .js, .ts, .go, .java)
- gitignore exclusion prevents counting generated/vendor code
- Fast scanning (no file content parsing required for detection)
- Supports polyglot repositories (multiple languages)

**Alternatives Considered**:
- GitHub Linguist: Heavyweight dependency, overkill for detection
- File content analysis (shebangs, syntax): Slow, unnecessary
- Package manager detection only: Misses standalone scripts

**Best Practices**:
- Scan repository once, cache language map
- Respect .gitignore patterns (use gitpython's `git ls-files`)
- Map extensions to languages: `.py`→Python, `.js/.jsx`→JavaScript, `.ts/.tsx`→TypeScript
- Handle ambiguous extensions (`.h` could be C or C++)
- Set minimum file threshold (e.g., 5+ files to count as "using language")

## 4. Attribute Weighting System

### Decision: Tier-Based Default + YAML Configuration Override

**Rationale**:
- Research report defines 4 tiers (Essential → Advanced)
- Default weights encode tier priorities (Tier 1 highest impact)
- YAML configuration allows organizational customization
- Weights must sum to 1.0 (percentages) for interpretable scores

**Default Weight Distribution**:
```
Tier 1 (Essential) - 5 attributes:    40% total (8% each)
Tier 2 (Critical) - 6 attributes:     30% total (5% each)
Tier 3 (Important) - 7 attributes:    20% total (~2.86% each)
Tier 4 (Advanced) - 7 attributes:     10% total (~1.43% each)
```

**Configuration File Format** (.agentready-config.yaml):
```yaml
weights:
  claude_md_file: 0.08
  conventional_commits: 0.05
  type_annotations: 0.08
  # ... all 25 attributes

# Optional: Override tier defaults
tier_multipliers:
  tier_1: 2.0  # Double importance
  tier_2: 1.5
  tier_3: 1.0
  tier_4: 0.5
```

**Best Practices**:
- Validate weights sum to 1.0 ± 0.01 (floating point tolerance)
- Provide clear error messages for invalid configurations
- Document weight rationale in example config file
- Allow partial overrides (missing attributes use defaults)

## 5. Assessment Architecture Pattern

### Decision: Strategy Pattern with Base Assessor Interface

**Rationale**:
- Each attribute is an independent assessment strategy
- Common interface ensures consistency across assessors
- Easy to add new attributes or modify existing ones
- Enables parallel assessment execution (future optimization)
- Supports graceful degradation (skip failed assessors)

**Base Assessor Interface**:
```python
class BaseAssessor(ABC):
    @property
    @abstractmethod
    def attribute_id(self) -> str:
        """Unique attribute identifier (e.g., 'claude_md_file')"""

    @property
    @abstractmethod
    def tier(self) -> int:
        """Tier 1-4 from research report"""

    @abstractmethod
    def assess(self, repository: Repository) -> Finding:
        """Execute assessment, return Finding with score, evidence, remediation"""

    def is_applicable(self, repository: Repository) -> bool:
        """Check if attribute applies to this repository (e.g., language-specific)"""
        return True
```

**Best Practices**:
- Keep assessors stateless (no instance variables)
- Return structured Finding objects (never raw dicts)
- Include specific evidence (file paths, line numbers, measurements)
- Generate remediation guidance from research report content
- Handle errors gracefully (return Finding with error status, not exceptions)
- Use type hints for all method signatures

## 6. Repository Analysis Tools

### Decision: gitpython + Language-Specific Analyzers

**Primary Tools**:
- **gitpython**: Repository metadata, commit history, .gitignore parsing
- **radon**: Python cyclomatic complexity, maintainability index
- **lizard**: Multi-language complexity analysis (C, C++, Java, JavaScript, etc.)
- **stdlib pathlib**: File system traversal and pattern matching

**Rationale**:
- gitpython provides Git-native operations (respects .gitignore)
- radon is Python-specific, highly accurate for Python codebases
- lizard supports multiple languages with consistent interface
- Avoid shell calls to external tools (portability, security)

**Best Practices**:
- Cache file system scans (don't traverse repository multiple times)
- Use gitpython's `git.Repo.iter_commits()` for commit analysis
- Lazy-load analysis tools (import only when language detected)
- Set reasonable limits (max files to analyze, timeout per check)
- Provide progress callbacks for long-running analyses

## 7. Error Handling and Graceful Degradation

### Decision: Try-Assess-Skip Pattern

**Rationale**:
- Partial results more valuable than complete failure
- Users can fix blockers (install missing tools) and re-run
- Clear error reporting enables self-service troubleshooting
- Maintains progress indication (X/25 attributes assessed)

**Error Handling Strategy**:
```python
for assessor in assessors:
    try:
        if not assessor.is_applicable(repo):
            findings.append(Finding.not_applicable(assessor.attribute_id))
            continue

        finding = assessor.assess(repo)
        findings.append(finding)

    except MissingToolError as e:
        findings.append(Finding.skipped(
            assessor.attribute_id,
            reason=f"Missing tool: {e.tool_name}",
            remediation=f"Install with: {e.install_command}"
        ))

    except PermissionError as e:
        findings.append(Finding.skipped(
            assessor.attribute_id,
            reason=f"Permission denied: {e.filename}"
        ))

    except Exception as e:
        findings.append(Finding.error(
            assessor.attribute_id,
            reason=f"Unexpected error: {str(e)}"
        ))
        logger.exception(f"Assessment failed for {assessor.attribute_id}")
```

**Best Practices**:
- Define custom exception types for known failure modes
- Include remediation guidance in error findings
- Log full stack traces for unexpected errors (debugging)
- Count skipped/error attributes separately from assessed
- Adjust score calculation (exclude skipped from denominator per FR-027)

## 8. Report File Naming and Versioning

### Decision: Timestamp-Based Filenames with Latest Symlink

**Rationale**:
- Timestamps enable tracking score improvements over time
- Unique filenames prevent accidental overwrites
- Symlink to latest makes it easy to find most recent report
- ISO 8601 format ensures sortable filenames

**File Naming Convention**:
```
.agentready/
├── report-2025-11-20T14-30-00.html
├── report-2025-11-20T14-30-00.md
├── report-latest.html -> report-2025-11-20T14-30-00.html
└── report-latest.md -> report-2025-11-20T14-30-00.md
```

**Best Practices**:
- Use ISO 8601 with colons replaced by hyphens (cross-platform safe)
- Create symlinks atomically (write to temp, rename)
- Offer `--output-name` flag for custom naming
- Clean up old reports (keep last N runs, configurable)
- Store assessment metadata in JSON sidecar file (for automation)

## 9. Markdown Report Structure

### Decision: GitHub-Flavored Markdown with Tables

**Rationale**:
- GFM is ubiquitous (GitHub, GitLab, Bitbucket, VS Code)
- Tables display structured data clearly
- Collapsible sections with `<details>` work in GFM
- Easy to diff in version control

**Report Structure**:
```markdown
# AgentReady Assessment Report

**Repository**: owner/repo
**Date**: 2025-11-20 14:30:00
**Score**: 72/100 (Silver)
**Attributes Assessed**: 23/25 (2 skipped)

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Documentation | 85% | ✅ Pass |
| Code Quality | 62% | ⚠️ Needs Improvement |
| ... | ... | ... |

## Detailed Findings

### 1. Context Window Optimization

#### 1.1 CLAUDE.md Configuration Files ✅

**Score**: 100/100
**Evidence**:
- File exists: `CLAUDE.md` (487 lines)
- Contains tech stack section
- Contains standard commands

<details>
<summary>Good Practices Found</summary>

- Concise format (<1000 lines)
- Clear repository structure
</details>

#### 1.2 Concise Structured Documentation ⚠️

**Score**: 60/100
**Evidence**:
- README exists (1247 lines) - exceeds recommended 500 lines

**Remediation**:
- Split README into multiple docs
- Move detailed API docs to wiki
```

**Best Practices**:
- Use emoji sparingly (✅❌⚠️ for status only)
- Include clickable table of contents for long reports
- Preserve all research report citations
- Use code blocks with language tags for remediation commands
- Keep tables simple (3-5 columns maximum)

## 10. Testing Strategy

### Decision: Pytest with Fixtures + Test Repositories

**Rationale**:
- Pytest is Python's de-facto testing framework
- Fixtures enable reusable test repositories
- Test repositories provide known-good/known-bad data
- Contract tests validate report schemas

**Test Repository Approach**:
Create fixture repositories in `tests/fixtures/repositories/`:
- `minimal-python/`: Bare Python project (most attributes fail)
- `gold-standard-python/`: Exemplary Python project (high score)
- `polyglot/`: Multi-language repository
- `edge-cases/`: Unusual structures (monorepo, submodules, etc.)

**Best Practices**:
- Use `@pytest.fixture(scope="session")` for repository setup (expensive)
- Store expected scores/findings in JSON files
- Test each assessor in isolation (unit tests)
- Test full workflow with real git repositories (integration tests)
- Use `pytest-cov` to enforce >80% coverage
- Mock external tools in unit tests, use real tools in integration tests

## 11. Proportional Scoring Algorithm

### Decision: Linear Proportional Scoring

**Context**: Many attributes have measurable thresholds that can be partially met (e.g., 65% test coverage when 80% is required). Linear proportional scoring provides deterministic, understandable results (per FR-014).

**Rationale**: Linear proportional scoring is:
- **Simple**: Easy to understand and explain to users
- **Deterministic**: Same inputs always produce same outputs
- **Fair**: Provides clear incentives for incremental improvement
- **Predictable**: Users can calculate expected score changes

**Algorithm**:
```python
def calculate_proportional_score(measured_value, threshold, attribute_type):
    """
    Calculate proportional score for partial compliance.

    Args:
        measured_value: The measured value (numeric or parseable)
        threshold: The target threshold
        attribute_type: 'higher_is_better' or 'lower_is_better'

    Returns:
        Score from 0-100
    """
    if attribute_type == 'higher_is_better':
        # Example: test coverage (want higher values)
        if measured_value >= threshold:
            return 100
        elif measured_value <= 0:
            return 0
        else:
            return (measured_value / threshold) * 100

    elif attribute_type == 'lower_is_better':
        # Example: file length (want lower values)
        if measured_value <= threshold:
            return 100
        elif threshold == 0:
            return 0  # Avoid division by zero
        else:
            # Degrade linearly, cap at 0
            return max(0, 100 - ((measured_value - threshold) / threshold) * 100)
```

**Edge Cases**:
- Division by zero: Return 0 score
- Negative values: Clamp to 0
- Values exceeding 2x threshold (lower_is_better): Cap at 0
- Values exceeding 2x threshold (higher_is_better): Cap at 100

**Examples**:
- Test coverage: 65% measured, 80% threshold → 65/80 * 100 = 81.25 score
- File length: 450 lines measured, 300 threshold → 100 - ((450-300)/300)*100 = 50 score
- Cyclomatic complexity: 5 measured, 10 threshold → 100 (meets threshold)

**Alternatives Considered**:
- Exponential penalties: Too harsh for minor violations
- Sigmoid curves: Complex to explain, non-obvious behavior
- Step functions: Too coarse-grained (all-or-nothing)

**References**:
- Spec FR-014: "Tool MUST handle repositories that partially meet attribute criteria"
- Spec FR-027: "Tool MUST calculate overall score based only on successfully evaluated attributes"

## Summary

All technical decisions grounded in pragmatic Python ecosystem best practices. No research gaps or unresolved questions. Implementation can proceed directly to Phase 1 (data modeling and contracts).
