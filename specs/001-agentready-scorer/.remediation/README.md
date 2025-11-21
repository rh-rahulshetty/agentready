# Specification Remediation Summary

**Analysis Date**: 2025-11-21
**Analyst**: Claude Code Analysis
**Status**: Ready for Review

---

## Overview

This directory contains 5 remediation documents addressing HIGH and MEDIUM severity specification issues identified in the analysis phase. All content has been finalized based on user decisions and is ready for integration into the specification.

## Remediation Files

### A1-proportional-scoring.md (HIGH Priority)
**Issue**: Proportional scoring algorithm undefined
**Target**: `specs/001-agentready-scorer/research.md`
**Decision**: Linear proportional scoring (user approved)
**Impact**: Resolves FR-014 ambiguity, enables deterministic partial compliance scoring

### A2-tier-weight-distribution.md (HIGH Priority)
**Issue**: Tier-based weight distribution not specified
**Target**: `specs/001-agentready-scorer/data-model.md`
**Decision**: 50/30/15/5 distribution with heavy CLAUDE.md penalty (user approved)
**Impact**: Resolves FR-031 ambiguity, defines complete 25-attribute weight mapping
**Key Points**:
- CLAUDE.md gets 10% weight (critical penalty for missing)
- Tier 1: 50% (5 attributes @ 10% each)
- Actual tier assignments extracted from research report

### U1-research-update-mechanism.md (MEDIUM Priority)
**Issue**: Research report update process underspecified
**Target**: `specs/001-agentready-scorer/plan.md`
**Decision**: Explicit opt-in via `--update-research` only (user approved)
**Impact**: Resolves FR-023, enables research report updates with safety
**Key Points**:
- Bundled version is default
- Update only on explicit command
- Users can point to custom research files
- Atomic update with rollback on failure

### U2-research-validation.md (MEDIUM Priority)
**Issue**: Research report validation criteria missing
**Target**: Create new `specs/001-agentready-scorer/contracts/research-report-schema.md`
**Decision**: Warning-only validation (user approved)
**Impact**: Resolves FR-024, enables research report quality checks
**Key Points**:
- Errors block usage (missing metadata, wrong attribute count)
- Warnings allow usage (missing examples, low reference count)
- 25 attributes, 4 tiers, 20+ references required

### U3-weight-validation.md (MEDIUM Priority)
**Issue**: Weight validation rules incomplete
**Target**: `specs/001-agentready-scorer/data-model.md`
**Decision**: User recommendation approved (partial configs with rescaling)
**Impact**: Resolves FR-033, enables safe custom weight configuration
**Key Points**:
- Completeness, positivity, sum=1.0 ±0.001 enforced
- Bounds (0.5%-20%) are warnings only
- Partial configs supported with automatic rescaling
- CLI > config file > tier defaults precedence

---

## Integration Steps

To integrate these remediations into the specification:

1. **Review Each Document**:
   ```bash
   cd specs/001-agentready-scorer/.remediation
   cat A1-proportional-scoring.md
   cat A2-tier-weight-distribution.md
   cat U1-research-update-mechanism.md
   cat U2-research-validation.md
   cat U3-weight-validation.md
   ```

2. **Apply Remediations**:
   - Copy content from A1 → `research.md` (add Decision 11)
   - Copy content from A2 → `data-model.md` (add Weight Distribution section)
   - Copy content from U1 → `plan.md` (add to Technical Context)
   - Create new file from U2 → `contracts/research-report-schema.md`
   - Copy content from U3 → `data-model.md` (add Weight Validation section)

3. **Verify Integration**:
   ```bash
   # Check research.md has Decision 11
   grep "Decision 11" specs/001-agentready-scorer/research.md

   # Check data-model.md has weight sections
   grep "Weight Distribution" specs/001-agentready-scorer/data-model.md
   grep "Configuration Weight Validation" specs/001-agentready-scorer/data-model.md

   # Check plan.md has update mechanism
   grep "Research Report Update Mechanism" specs/001-agentready-scorer/plan.md

   # Check new contract file exists
   ls specs/001-agentready-scorer/contracts/research-report-schema.md
   ```

4. **Update Analysis Report**:
   - Mark A1, A2, U1, U2, U3 as RESOLVED
   - Re-run analysis to confirm no regressions
   - Update metrics (ambiguity count: 5 → 0)

---

## User Decisions Summary

| Issue | Question | Decision |
|-------|----------|----------|
| A1 | Linear vs non-linear scoring? | Linear (simple, transparent) |
| A1 | Capping behavior? | Cap at 0/100, no negative scores |
| A2 | Weight distribution? | 50/30/15/5 across tiers |
| A2 | CLAUDE.md penalty? | Heavy (10%, highest single attribute) |
| A2 | Tier assignments? | Extract from actual research report |
| U1 | Update frequency? | Explicit `--update-research` only |
| U1 | Repository location? | `ambient-code/agentready` (future) |
| U1 | Version compatibility? | Tool + research versioned together |
| U2 | Validation strictness? | Errors block, warnings allow |
| U2 | Minimum references? | 20 citations (evidence threshold) |
| U3 | Partial configs? | Supported with automatic rescaling |
| U3 | Weight bounds? | 0.5%-20% warnings, not errors |
| U3 | Precedence? | CLI > config > tier defaults |

---

## Additional Items

### Backlog Created

**File**: `/Users/jeder/repos/sk/agentready/BACKLOG.md`

**Items Added**:
1. Bootstrap new GitHub repositories (P5)
2. Report schema versioning (P3)

**Note**: Bootstrap feature includes repository at `ambient-code/agentready` which does not yet exist. Do not push or implement until repository is created.

### Configuration Output

**Requirement**: JSON output needed in addition to HTML/Markdown
**Status**: Already specified in FR-005 and contracts/assessment-schema.json
**Action**: No changes needed (JSON already designed)

---

## Metrics After Remediation

**Before**:
- Ambiguity Count: 5
- Underspecification Count: 5
- High Severity: 3
- Medium Severity: 8

**After** (projected):
- Ambiguity Count: 0 (-5)
- Underspecification Count: 0 (-5)
- High Severity: 0 (-3)
- Medium Severity: 3 (terminology, documentation)

**Coverage**: 100% (unchanged)
**Constitution Compliance**: 100% (unchanged)

---

## Next Steps

**Immediate**:
1. Review remediation documents
2. Integrate into specification files
3. Re-run `/speckit.analyze` to verify resolution
4. Proceed to `/speckit.implement`

**Future**:
1. Create `ambient-code/agentready` GitHub repository
2. Implement bootstrap feature from backlog
3. Version report schemas per backlog item

**Status**: ✅ Ready for implementation
