# Remediation A1: Proportional Scoring Formula

**Issue**: FR-014 mentions proportional scoring but doesn't define the algorithm.

**Target File**: `specs/001-agentready-scorer/research.md`

**Action**: Add new section after existing technical decisions (after Decision 10)

---

## Content to Add

### Decision 11: Proportional Scoring Algorithm

**Context**: Many attributes have measurable thresholds that can be partially met (e.g., 65% test coverage when 80% is required). Linear proportional scoring provides deterministic, understandable results.

**Decision**: Use linear proportional scoring with the following formula:

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

**Rationale**: Linear proportional scoring is:
- **Simple**: Easy to understand and explain to users
- **Deterministic**: Same inputs always produce same outputs
- **Fair**: Provides clear incentives for incremental improvement
- **Predictable**: Users can calculate expected score changes

Non-linear scoring (exponential penalties, sigmoid curves) was considered but rejected due to complexity and reduced transparency.

**References**:
- Spec FR-014: "Tool MUST handle repositories that partially meet attribute criteria"
- Spec FR-027: "Tool MUST calculate overall score based only on successfully evaluated attributes"
- Research report: All 25 attributes have quantifiable thresholds
