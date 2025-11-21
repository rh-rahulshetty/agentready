# Remediation U3: Weight Validation Rules

**Issue**: FR-033 requires weight validation but doesn't define the rules.

**Target File**: `specs/001-agentready-scorer/data-model.md`

**Action**: Add subsection after the Weight Distribution section

---

## Content to Add

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
