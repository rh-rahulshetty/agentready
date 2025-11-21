# Remediation A2: Tier-Based Weight Distribution

**Issue**: FR-031 references tier-based weighting but doesn't specify the distribution.

**Target File**: `specs/001-agentready-scorer/data-model.md`

**Action**: Add new section after entities section

---

## Content to Add

## Weight Distribution

### Default Tier-Based Weights

Per FR-031, attributes are weighted by tier priority with heavy penalties for missing essentials (especially CLAUDE.md). Tier 1 (Essential) attributes have 8x the impact of Tier 4 (Advanced) attributes.

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
