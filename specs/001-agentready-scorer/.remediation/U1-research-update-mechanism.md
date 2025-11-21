# Remediation U1: Research Report Update Mechanism

**Issue**: FR-023 requires update capability but doesn't specify the mechanism.

**Target File**: `specs/001-agentready-scorer/plan.md`

**Action**: Add subsection under "## Technical Context"

---

## Content to Add

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
