# Data Model: AgentReady Repository Scorer

**Phase**: 1 - Data Modeling
**Date**: 2025-11-20
**Purpose**: Define entities, relationships, and validation rules for the assessment system

## Overview

The data model consists of 7 primary entities organized in a hierarchical assessment workflow:
`Repository` → `Assessment` → `Finding[]` → `Remediation`

All entities use Python dataclasses with type hints for clarity and validation.

## Entity Definitions

### 1. Repository

Represents the target git repository being assessed.

**Fields**:
- `path: pathlib.Path` - Absolute path to repository root
- `name: str` - Repository name (derived from path)
- `url: str | None` - Remote origin URL if available
- `branch: str` - Current branch name
- `commit_hash: str` - Current HEAD commit SHA
- `languages: dict[str, int]` - Detected languages with file counts (e.g., `{"Python": 42, "JavaScript": 18}`)
- `total_files: int` - Total files in repository (respecting .gitignore)
- `total_lines: int` - Total lines of code

**Validation Rules**:
- `path` must exist and contain `.git` directory
- `name` derived from `path.name`
- `languages` keys must be valid language names
- `total_files` and `total_lines` must be non-negative

**Relationships**:
- One Repository → One Assessment

**Example**:
```python
Repository(
    path=Path("/home/user/myproject"),
    name="myproject",
    url="https://github.com/user/myproject.git",
    branch="main",
    commit_hash="abc123def456",
    languages={"Python": 42, "Markdown": 12},
    total_files=54,
    total_lines=8432
)
```

---

### 2. Attribute

Defines one of the 25 agent-ready quality attributes from the research report.

**Fields**:
- `id: str` - Unique identifier (e.g., "claude_md_file", "test_coverage")
- `name: str` - Human-readable name (e.g., "CLAUDE.md Configuration Files")
- `category: str` - Research report section (e.g., "Context Window Optimization")
- `tier: int` - Priority tier 1-4 (1=Essential, 4=Advanced)
- `description: str` - What this attribute measures
- `criteria: str` - Measurable criteria for passing
- `default_weight: float` - Default weight in scoring (0.0-1.0)

**Validation Rules**:
- `id` must be unique, lowercase, snake_case
- `tier` must be 1, 2, 3, or 4
- `default_weight` must be in range [0.0, 1.0]
- All default weights across 25 attributes must sum to 1.0 ± 0.01

**Relationships**:
- One Attribute → Many Findings (across different assessments)

**Example**:
```python
Attribute(
    id="claude_md_file",
    name="CLAUDE.md Configuration Files",
    category="Context Window Optimization",
    tier=1,
    description="Markdown file at repository root for Claude Code context",
    criteria="File exists, <1000 lines, contains required sections",
    default_weight=0.08
)
```

---

### 3. Assessment

Represents a complete evaluation of a repository at a specific point in time.

**Fields**:
- `repository: Repository` - The repository assessed
- `timestamp: datetime` - When assessment was performed
- `overall_score: float` - Weighted average score 0-100
- `certification_level: str` - Platinum/Gold/Silver/Bronze based on score
- `attributes_assessed: int` - Number of successfully evaluated attributes
- `attributes_skipped: int` - Number of skipped attributes (tool missing, errors)
- `attributes_total: int` - Total attributes (should be 25)
- `findings: list[Finding]` - Individual attribute results
- `config: Config | None` - Custom configuration used (if any)
- `duration_seconds: float` - Time taken for assessment

**Validation Rules**:
- `overall_score` must be in range [0.0, 100.0]
- `certification_level` must be one of: "Platinum", "Gold", "Silver", "Bronze", "Needs Improvement"
- `attributes_assessed + attributes_skipped` must equal `attributes_total`
- `findings` length must equal `attributes_total`

**Certification Thresholds**:
- Platinum: 90-100
- Gold: 75-89
- Silver: 60-74
- Bronze: 40-59
- Needs Improvement: 0-39

**Relationships**:
- One Assessment → One Repository
- One Assessment → Many Findings (exactly 25)

**Example**:
```python
Assessment(
    repository=repo,
    timestamp=datetime(2025, 11, 20, 14, 30, 0),
    overall_score=72.5,
    certification_level="Silver",
    attributes_assessed=23,
    attributes_skipped=2,
    attributes_total=25,
    findings=[...],
    config=None,
    duration_seconds=127.3
)
```

---

### 4. Finding

Result of assessing a single attribute against a repository.

**Fields**:
- `attribute: Attribute` - The attribute being assessed
- `status: str` - "pass", "fail", "skipped", "error", "not_applicable"
- `score: float | None` - Score 0-100, or None if skipped/error
- `measured_value: str | None` - Actual measurement (e.g., "847 lines", "63% coverage")
- `threshold: str | None` - Expected threshold (e.g., "<300 lines", ">80% coverage")
- `evidence: list[str]` - Specific files/metrics supporting the finding
- `remediation: Remediation | None` - How to fix if failing
- `error_message: str | None` - Error details if status="error"

**Validation Rules**:
- `status` must be one of the defined values
- `score` required if status="pass" or status="fail", otherwise None
- `score` must be in range [0.0, 100.0] if present
- `error_message` required if status="error"

**Status Meanings**:
- `pass`: Attribute meets criteria (score typically 70-100)
- `fail`: Attribute doesn't meet criteria (score typically 0-69)
- `skipped`: Attribute couldn't be assessed (missing tool, permission error)
- `error`: Unexpected error during assessment
- `not_applicable`: Attribute doesn't apply to this repository (e.g., language-specific check)

**Relationships**:
- Many Findings → One Assessment
- Many Findings → One Attribute

**Example**:
```python
Finding(
    attribute=Attribute(...),
    status="fail",
    score=40.0,
    measured_value="847 lines",
    threshold="<300 lines",
    evidence=["src/large_module.py: 847 lines"],
    remediation=Remediation(...),
    error_message=None
)
```

---

### 5. Remediation

Actionable guidance for fixing a failing attribute.

**Fields**:
- `summary: str` - One-line summary of what to do
- `steps: list[str]` - Ordered steps to remediate
- `tools: list[str]` - Tools/packages needed (e.g., "black", "pytest-cov")
- `commands: list[str]` - Example commands to run
- `examples: list[str]` - Code/config examples
- `citations: list[Citation]` - Links to documentation/research

**Validation Rules**:
- `summary` must be non-empty
- `steps` should have at least one step
- Each command should be a single line

**Relationships**:
- One Remediation → One Finding
- Many Remediation → Many Citations

**Example**:
```python
Remediation(
    summary="Split large_module.py into smaller modules",
    steps=[
        "Identify logical groupings within large_module.py",
        "Extract each grouping into separate module",
        "Update imports in dependent files",
        "Verify tests still pass"
    ],
    tools=["radon"],
    commands=["radon cc src/large_module.py -a"],
    examples=["# Before: 847 lines\n# After: 4 modules of ~200 lines each"],
    citations=[...]
)
```

---

### 6. Citation

Reference to authoritative source from research report.

**Fields**:
- `source: str` - Source name (e.g., "Anthropic Engineering Blog")
- `title: str` - Article/paper title
- `url: str | None` - Link to source
- `relevance: str` - Why this citation supports the attribute

**Validation Rules**:
- `source` must be non-empty
- `url` must be valid URL if present

**Relationships**:
- Many Citations → One Remediation

**Example**:
```python
Citation(
    source="Microsoft Learn",
    title="Code metrics - Cyclomatic complexity",
    url="https://learn.microsoft.com/code-metrics",
    relevance="Defines cyclomatic complexity thresholds"
)
```

---

### 7. Config

User configuration for customizing assessment behavior.

**Fields**:
- `weights: dict[str, float]` - Custom attribute weights (attribute_id → weight)
- `excluded_attributes: list[str]` - Attributes to skip
- `language_overrides: dict[str, list[str]]` - Force language detection
- `output_dir: pathlib.Path | None` - Custom output directory

**Validation Rules**:
- `weights` keys must be valid attribute IDs
- `weights` values must be in range [0.0, 1.0]
- `weights` values must sum to 1.0 ± 0.01
- `excluded_attributes` must contain valid attribute IDs

**Relationships**:
- One Config → One Assessment (optional)

**Example**:
```python
Config(
    weights={
        "claude_md_file": 0.10,  # Increase importance
        "test_coverage": 0.10,
        # ... other attributes
    },
    excluded_attributes=["performance_benchmarks"],
    language_overrides={"Python": ["*.pyx"]},
    output_dir=Path("/custom/reports")
)
```

---

## Weight Distribution

### Default Tier-Based Weights

Per FR-031, attributes are weighted by tier priority with heavy penalties for missing essentials (especially CLAUDE.md). Tier 1 (Essential) attributes have 10x the impact of Tier 4 (Advanced) attributes.

| Tier | Description | Total Weight | Attributes | Weight Per Attribute |
|------|-------------|--------------|------------|---------------------|
| Tier 1 | Essential | 50% | 5 attributes | 10.0% each |
| Tier 2 | Critical | 30% | 10 attributes | 3.0% each |
| Tier 3 | Important | 15% | 5 attributes | 3.0% each |
| Tier 4 | Advanced | 5% | 5 attributes | 1.0% each |

**Total**: 100% across 25 attributes

**Penalty Philosophy**: Missing Tier 1 essentials (especially CLAUDE.md at 10%) creates significant score impact, incentivizing foundational improvements before advanced optimizations.

### Attribute-to-Tier Mapping

Based on research report tier assignments (lines 1535-1570):

**Tier 1 (Essential)** - 50% total weight (10% each):
1. CLAUDE.md Configuration Files (1.1) - **10.0%** ⚠️ CRITICAL
2. README Structure (2.1) - 10.0%
3. Type Annotations (3.3) - 10.0%
4. Standard Project Layouts (4.1) - 10.0%
5. Lock Files for Reproducibility (6.1) - 10.0%

**Tier 2 (Critical)** - 30% total weight (3% each):
6. Test Coverage Requirements (5.1) - 3.0%
7. Pre-commit Hooks & CI/CD Linting (5.3) - 3.0%
8. Conventional Commit Messages (7.1) - 3.0%
9. .gitignore Completeness (7.2) - 3.0%
10. One-Command Build/Setup (8.1) - 3.0%
11. Concise Structured Documentation (1.2) - 3.0%
12. Inline Documentation (2.2) - 3.0%
13. File Size Limits (1.3) - 3.0%
14. Dependency Freshness & Security (6.2) - 3.0%
15. Separation of Concerns (4.2) - 3.0%

**Tier 3 (Important)** - 15% total weight (3% each):
16. Cyclomatic Complexity Thresholds (3.1) - 3.0%
17. Structured Logging (9.2) - 3.0%
18. OpenAPI/Swagger Specifications (10.1) - 3.0%
19. Architecture Decision Records (2.3) - 3.0%
20. Semantic File & Directory Naming (11.3) - 3.0%

**Tier 4 (Advanced)** - 5% total weight (1% each):
21. Security Scanning Automation (13.1) - 1.0%
22. Performance Benchmarks (15.1) - 1.0%
23. Code Smell Elimination (3.4) - 1.0%
24. Issue & Pull Request Templates (7.3) - 1.0%
25. Container/Virtualization Setup (8.3) - 1.0%

### Custom Weight Configuration

Users can override default weights via `.agentready-config.yaml`:

```yaml
weights:
  claude_md_file: 0.15          # Increase from 10% to 15% (org prioritizes CLAUDE.md)
  test_coverage: 0.05           # Increase from 3% to 5%
  conventional_commits: 0.01    # Decrease from 3% to 1%
  # ... other attributes use defaults, rescaled to sum to 1.0
```

**Validation** (per FR-033):
- All 25 attributes must be present (explicitly or via defaults)
- Weights must be positive numbers
- Weights must sum to 1.0 (±0.001 tolerance for floating point)
- Missing attributes inherit rescaled tier defaults

### Score Calculation Example

```python
overall_score = sum(
    attribute_score * weight
    for attribute_score, weight in zip(scores, weights)
    if attribute_status == 'assessed'  # Exclude skipped per FR-027
)

# Normalize if some attributes skipped
total_weight_assessed = sum(
    weight for weight, status in zip(weights, statuses)
    if status == 'assessed'
)
normalized_score = (overall_score / total_weight_assessed) * 100
```

**Example Scenario**:
- Repository missing CLAUDE.md: loses 10 points immediately
- Repository with CLAUDE.md but no tests: scores 10 (CLAUDE.md) + 0 (tests)
- Perfect CLAUDE.md + perfect tests = 10 + 3 = 13 points from just 2 attributes

### Configuration Precedence

When weights exist in multiple locations:

1. **CLI flags** (highest priority) - `--weight claude_md_file=0.15`
2. **Config file** - `.agentready-config.yaml`
3. **Tier defaults** (lowest priority) - Built-in distribution

**Rationale**: Tier-based distribution with heavy penalties for missing essentials ensures:
- Users prioritize foundational improvements (CLAUDE.md, README, types)
- Missing CLAUDE.md (10% weight) has 10x impact of missing container setup (1% weight)
- Aligns with research report's "Essential → Advanced" priority guidance
- Steep gradient incentivizes completing Tier 1 before moving to advanced features

---

## Configuration Weight Validation

**Per FR-033**: Custom weights in `.agentready-config.yaml` must be validated.

### Validation Rules

#### Rule 1: Completeness
All 25 attributes must have weights (explicit or inherited):

```python
REQUIRED_ATTRIBUTES = [
    'claude_md_file', 'concise_documentation', 'file_size_limits',
    'readme_structure', 'inline_documentation', 'architecture_decisions',
    'cyclomatic_complexity', 'function_length', 'type_annotations',
    'code_smells', 'standard_layout', 'separation_concerns',
    'test_coverage', 'test_naming', 'precommit_hooks',
    'lock_files', 'dependency_freshness', 'conventional_commits',
    'gitignore_completeness', 'issue_pr_templates', 'one_command_setup',
    'dev_env_docs', 'container_setup', 'error_clarity',
    'structured_logging', 'openapi_specs', 'graphql_schemas',
    'dry_principle', 'naming_conventions', 'semantic_naming',
    'cicd_visibility', 'branch_protection', 'security_scanning',
    'secrets_management', 'performance_benchmarks'
]

def validate_completeness(config_weights, default_weights):
    missing = [
        attr for attr in REQUIRED_ATTRIBUTES
        if attr not in config_weights and attr not in default_weights
    ]
    if missing:
        raise ValidationError(f"Missing weights for: {', '.join(missing)}")
```

#### Rule 2: Positive Values
All weights must be positive numbers:

```python
def validate_positive(weights):
    invalid = {attr: w for attr, w in weights.items() if w <= 0}
    if invalid:
        raise ValidationError(f"Weights must be positive: {invalid}")
```

#### Rule 3: Sum Constraint
Weights must sum to 1.0 within floating-point tolerance:

```python
TOLERANCE = 0.001  # Allow 0.1% rounding error

def validate_sum(weights):
    total = sum(weights.values())
    if abs(total - 1.0) > TOLERANCE:
        raise ValidationError(
            f"Weights must sum to 1.0 (got {total:.4f}). "
            f"Difference: {total - 1.0:+.4f}"
        )
```

#### Rule 4: Reasonable Bounds
Individual weights should be between 0.5% and 20% (warnings only):

```python
MIN_WEIGHT = 0.005  # 0.5%
MAX_WEIGHT = 0.20   # 20%

def validate_bounds(weights):
    warnings = []
    for attr, weight in weights.items():
        if weight < MIN_WEIGHT:
            warnings.append(f"{attr}: {weight:.1%} is very low (< 0.5%)")
        if weight > MAX_WEIGHT:
            warnings.append(f"{attr}: {weight:.1%} is very high (> 20%)")
    return warnings  # Non-blocking warnings
```

### Partial Configuration Handling

Users can specify only overrides, inheriting defaults for others:

```yaml
# .agentready-config.yaml (partial configuration)
weights:
  claude_md_file: 0.15      # Override Tier 1 default (10%)
  test_coverage: 0.05       # Override Tier 2 default (3%)
  # Other 23 attributes: inherit rescaled tier defaults
```

**Rescaling Algorithm**:

```python
def merge_and_rescale(config_weights, tier_defaults):
    """
    Merge config overrides with tier defaults, then rescale to sum to 1.0.

    Args:
        config_weights: User-specified weights (partial or complete)
        tier_defaults: Default tier-based weights (complete, sums to 1.0)

    Returns:
        Final weights dictionary (complete, sums to 1.0)
    """
    # Start with tier defaults
    final_weights = tier_defaults.copy()

    # Override with config values
    final_weights.update(config_weights)

    # Rescale to sum to 1.0
    total = sum(final_weights.values())
    rescaled = {attr: w / total for attr, w in final_weights.items()}

    return rescaled

# Example:
# config = {'claude_md_file': 0.15, 'test_coverage': 0.05}
# defaults = {25 attributes summing to 1.0}
# After merge: sum = 1.07 (overrides increased total by 0.07)
# After rescale: all weights * (1.0 / 1.07) ≈ 0.935x scaling factor
```

### Validation Command

```bash
agentready --validate-config [path/to/config.yaml]
```

**Output Example**:

```
Validating config: .agentready-config.yaml

✓ All 25 attributes have weights
✓ All weights are positive
✓ Weights sum to 1.0000 (within tolerance)
⚠ claude_md_file: 15.0% is high (default: 10.0%, tier 1 average: 10.0%)
⚠ test_coverage: 5.0% is high (default: 3.0%, tier 2 average: 3.0%)

Configuration: VALID with 2 warnings

Effective weights after rescaling:
  claude_md_file: 14.02% (config: 15.0%, rescaled down)
  test_coverage: 4.67% (config: 5.0%, rescaled down)
  conventional_commits: 2.80% (default: 3.0%, rescaled down)
  ... (22 more attributes)

Total: 100.00%
```

### Error Messages

**Invalid Sum**:
```
ERROR: Weights must sum to 1.0 (got 0.8500). Difference: -0.1500

Your weights total 85%. This suggests missing attributes or incorrect values.

Current distribution:
  Explicitly specified: 0.6500 (13 attributes)
  Using tier defaults: 0.2000 (12 attributes)

Suggestion: Either specify all 25 attributes explicitly, or let unspecified
attributes inherit tier defaults (which will be automatically rescaled).
```

**Negative Weight**:
```
ERROR: Weights must be positive: {'test_coverage': -0.05}

Negative weights are not allowed. Did you mean to reduce other weights instead?
```

**Missing Attributes**:
```
ERROR: Missing weights for: inline_documentation, architecture_decisions

All 25 attributes must have weights. Either:
1. Specify these attributes in your config, OR
2. Ensure they exist in default-weights.yaml

To see all required attributes:
  agentready --list-attributes
```

**Tolerance Exceeded**:
```
ERROR: Weights must sum to 1.0 (got 1.0025). Difference: +0.0025

Sum exceeds tolerance (±0.001). Likely due to rounding errors.

Suggestion: Reduce precision or adjust values. For example:
  claude_md_file: 0.100 (instead of 0.1003)
  test_coverage: 0.050 (instead of 0.0497)
```

### Validation Integration

- **On config load**: Automatic validation (fail fast on errors)
- **On manual validate**: Detailed report with warnings
- **On assessment run**: Validation errors block execution
- **On example generation**: `--generate-config` produces valid example with comments

### Configuration Precedence

**Precedence Order** (highest to lowest):

1. **CLI flags** - `agentready --weight claude_md_file=0.15`
2. **Config file** - `.agentready-config.yaml` in current directory
3. **Config file (alternate path)** - `agentready --config /path/to/config.yaml`
4. **Tier defaults** - Built-in `src/agentready/data/default-weights.yaml`

**Merging Rules**:
- CLI flags override config file weights
- Config file overrides tier defaults
- Unspecified attributes always inherit tier defaults
- Final weights always rescaled to sum to 1.0

**Example**:
```bash
# CLI flag takes precedence
agentready --config custom.yaml --weight claude_md_file=0.20

# Precedence:
# 1. claude_md_file = 0.20 (from CLI flag)
# 2. Other weights from custom.yaml (if present)
# 3. Remaining weights from tier defaults
# 4. All rescaled to sum to 1.0
```

---

## State Transitions

### Assessment Workflow

```
Repository → Validate → Detect Languages → Load Config → Create Assessment

For each Attribute:
    Create Assessor → Check Applicability

    if applicable:
        Execute Assessment → Create Finding
    else:
        Create Finding (status=not_applicable)

Calculate Overall Score → Determine Certification Level

Generate Reports → Save to Disk
```

### Finding Status Flow

```
                           ┌─────────────┐
                           │   Start     │
                           └──────┬──────┘
                                  │
                    ┌─────────────┴──────────────┐
                    │                            │
            ┌───────▼────────┐          ┌───────▼────────┐
            │  is_applicable?│          │   Execute      │
            │      No         │          │   Assessment   │
            └───────┬─────────┘          └───────┬────────┘
                    │                            │
            ┌───────▼────────┐      ┌────────────┼────────────┐
            │ not_applicable  │      │            │            │
            └────────────────┘  ┌───▼───┐  ┌─────▼─────┐ ┌───▼────┐
                                │ pass   │  │   fail    │ │ error  │
                                └────────┘  └───────────┘ └────────┘
```

## Serialization

All entities must support JSON serialization for:
- Report generation (HTML/Markdown use JSON as intermediate format)
- Automation integration (tools consuming assessment data)
- Caching/persistence (save assessment results)

**Serialization Strategy**:
- Use `dataclasses.asdict()` with custom JSON encoder
- Convert `datetime` to ISO 8601 strings
- Convert `Path` to strings
- Convert enums to string values
- Preserve nested structures

**Example JSON Output**:
```json
{
  "repository": {
    "name": "myproject",
    "path": "/home/user/myproject",
    "languages": {"Python": 42},
    "total_files": 54
  },
  "timestamp": "2025-11-20T14:30:00",
  "overall_score": 72.5,
  "certification_level": "Silver",
  "findings": [
    {
      "attribute": {"id": "claude_md_file", "name": "CLAUDE.md"},
      "status": "pass",
      "score": 100.0,
      "evidence": ["CLAUDE.md exists (487 lines)"]
    }
  ]
}
```

---

## Summary

Data model defines 7 entities with clear responsibilities:
- `Repository`: What is being assessed
- `Attribute`: What is being measured
- `Assessment`: Container for complete evaluation
- `Finding`: Result of one attribute check
- `Remediation`: How to fix failures
- `Citation`: Supporting research
- `Config`: User customization

All validation rules enforced at model layer (fail fast). State transitions are linear (no complex workflows). JSON serialization supports all output formats and automation integrations.
