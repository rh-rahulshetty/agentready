# Research Report Validation Schema

**Purpose**: Define validation criteria for agent-ready-codebase-attributes.md (per FR-024)

## Required Structure

### 1. Metadata Header (REQUIRED)

```markdown
---
version: SEMVER          # e.g., "1.2.0"
date: YYYY-MM-DD         # ISO 8601 date
---
```

**Validation**:
- ✅ Version follows semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Date is valid ISO 8601 format
- ⚠️ Date is not in future (warning only)

### 2. Attribute Definitions (REQUIRED)

Must contain exactly 25 attribute sections with this structure:

```markdown
### [Number].[Subnumber] [Attribute Name]

**Definition:** [Clear definition]

**Why It Matters:** [Rationale]

**Impact on Agent Behavior:**
- [Impact point 1]
- [Impact point 2]

**Measurable Criteria:**
- [Criterion 1]
- [Criterion 2]

**Citations:**
- [Source 1]
- [Source 2]
```

**Validation**:
- ✅ Exactly 25 attributes present
- ✅ Attributes numbered sequentially (1.1, 1.2, ..., 15.1)
- ✅ Each attribute has "Definition" section (non-empty)
- ✅ Each attribute has "Measurable Criteria" section (non-empty)
- ✅ At least one citation per attribute
- ⚠️ "Impact on Agent Behavior" section exists (warning if missing)

### 3. Tier Assignments (REQUIRED)

Research report must include tier classification section:

```markdown
## IMPLEMENTATION PRIORITIES

### Tier 1: Essential (Must-Have)
[List of attributes]

### Tier 2: Critical (Should-Have)
[List of attributes]

### Tier 3: Important (Nice-to-Have)
[List of attributes]

### Tier 4: Advanced (Optimization)
[List of attributes]
```

**Validation**:
- ✅ All 4 tiers defined
- ✅ All 25 attributes assigned to exactly one tier
- ✅ Each tier contains at least 1 attribute
- ⚠️ Tier distribution roughly balanced (warning if one tier has >50% of attributes)

### 4. Category Coverage (REQUIRED)

Must include attributes across these categories:
1. Context Window Optimization
2. Documentation Standards
3. Code Quality Metrics
4. Repository Structure
5. Testing & CI/CD
6. Dependency Management
7. Git & Version Control
8. Build & Development Setup
9. Error Handling & Debugging
10. API & Interface Documentation
11. Modularity & Code Organization
12. CI/CD Integration
13. Security & Compliance

**Validation**:
- ✅ At least 10 of 13 categories present
- ⚠️ Missing categories identified (warning only)

### 5. References Section (REQUIRED)

```markdown
## REFERENCES & CITATIONS

[Consolidated bibliography]
```

**Validation**:
- ✅ References section exists
- ✅ At least 20 unique citations (evidence-based design threshold)
- ⚠️ URLs are reachable (check via HEAD request, warn only if unreachable)

## Validation Severity

**ERRORS** (block usage - report must be fixed):
- Missing metadata header
- Invalid version/date format
- Incorrect attribute count (not 25)
- Missing "Measurable Criteria" in any attribute
- Fewer than 4 tiers defined
- Attributes not assigned to tiers

**WARNINGS** (allow usage - non-critical issues):
- Missing "Impact on Agent Behavior" sections
- Fewer than 20 references
- Unreachable citation URLs
- Unbalanced tier distribution
- Missing category coverage

## Validation Implementation

```python
class ResearchReportValidator:
    def validate(self, content: str) -> ValidationResult:
        errors = []
        warnings = []

        # Parse metadata
        metadata = self._extract_metadata(content)
        if not metadata:
            errors.append("Missing metadata header with version and date")
        elif not self._is_valid_semver(metadata.get('version')):
            errors.append(f"Invalid version format: {metadata.get('version')}")

        # Count attributes
        attributes = self._extract_attributes(content)
        if len(attributes) != 25:
            errors.append(f"Expected 25 attributes, found {len(attributes)}")

        # Check measurable criteria
        for attr in attributes:
            if not attr.measurable_criteria:
                errors.append(f"Missing measurable criteria for {attr.name}")
            if not attr.impact_on_agent:
                warnings.append(f"Missing 'Impact on Agent Behavior' for {attr.name}")

        # Check tier assignments
        tiers = self._extract_tiers(content)
        if len(tiers) < 4:
            errors.append(f"Expected 4 tiers, found {len(tiers)}")

        # Check references
        refs = self._extract_references(content)
        if len(refs) < 20:
            warnings.append(f"Only {len(refs)} references (recommend 20+ for evidence-based design)")

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings
        )
```

## Example Validation Output

```
✓ Metadata header valid (v1.2.0, 2025-11-20)
✓ 25 attributes found
✓ All attributes have measurable criteria
✓ 4 tiers defined with all attributes assigned
⚠ Attribute 1.1 missing 'Impact on Agent Behavior' section
⚠ Attribute 7.3 missing 'Impact on Agent Behavior' section
✓ 52 references found

Validation: PASSED with 2 warnings

Warnings can be ignored - research report is usable.
```

## Usage in Tool

```python
from agentready.services.research_loader import ResearchLoader

loader = ResearchLoader()
result = loader.load_and_validate('agent-ready-codebase-attributes.md')

if not result.valid:
    print("Research report validation FAILED:")
    for error in result.errors:
        print(f"  ❌ {error}")
    sys.exit(1)

if result.warnings:
    print("Research report validation warnings:")
    for warning in result.warnings:
        print(f"  ⚠️  {warning}")

# Proceed with valid research report
research = result.research
```
