# AgentReady Backlog

**Purpose**: Track future features and improvements for the agentready tool.

---

## Future Features

### Bootstrap New GitHub Repositories

**Priority**: P5 (Future Enhancement)

**Description**: Create functionality to bootstrap new GitHub repositories with agentready tooling and best practices from the start.

**Requirements**:
- Initialize new repository with agent-ready structure
- Create initial CLAUDE.md, README, .gitignore from templates
- Set up pre-commit hooks
- Configure GitHub Actions for agentready assessment
- Set up Dependabot
- Create PR/Issue templates
- Generate initial pyproject.toml or package.json with recommended dependencies

**Use Case**:
```bash
# Bootstrap new repository
agentready init --repo ambient-code/new-project --language python

# This would:
# 1. Create repository structure matching standard layout
# 2. Add CLAUDE.md, README.md, .gitignore templates
# 3. Configure CI/CD with agentready assessment workflow
# 4. Set up development environment configuration
```

**Related**: Initial repository creation, onboarding automation

**Notes**:
- Should support multiple languages (Python, JavaScript, TypeScript, Go, Java)
- Templates should be customizable
- Could integrate with GitHub CLI (gh) for repository creation
- Consider integration with `gh repo create` workflow

---

## Schema & Configuration

### Report Schema Versioning

**Priority**: P3 (Important)

**Description**: Define and version the JSON/HTML/Markdown report schemas to ensure backwards compatibility and enable schema evolution.

**Requirements**:
- JSON schema for assessment reports (contracts/assessment-schema.json exists)
- HTML schema for interactive reports (contracts/report-html-schema.md exists)
- Markdown schema for version control reports (contracts/report-markdown-schema.md exists)
- Schema versioning strategy (semantic versioning)
- Backwards compatibility testing
- Schema migration tools for major version changes

**Use Case**:
```bash
# Validate report against schema
agentready validate-report assessment-2025-11-20.json

# Migrate old report to new schema version
agentready migrate-report --from 1.0.0 --to 2.0.0 old-report.json
```

**Related**: Report generation, data model evolution

**Notes**:
- Schemas exist in contracts/ directory but need formal versioning
- Consider using JSON Schema Draft 2020-12
- Tool should validate generated reports against bundled schema
- Breaking schema changes should trigger major version bump

---

### Research Report Generator/Updater Utility

**Priority**: P4 (Enhancement)

**Description**: Create a utility tool to help maintain and update the research report (agent-ready-codebase-attributes.md) following the validation schema defined in contracts/research-report-schema.md.

**Requirements**:
- Generate new research reports from templates
- Validate existing reports against schema (contracts/research-report-schema.md)
- Update/add attributes while maintaining schema compliance
- Automatically format citations and references
- Extract tier assignments and metadata
- Verify 25 attributes, 4 tiers, 20+ references
- Check for required sections (Definition, Measurable Criteria, Impact on Agent Behavior)

**Use Case**:
```bash
# Validate existing research report
agentready research validate agent-ready-codebase-attributes.md

# Generate new research report from template
agentready research init --output new-research.md

# Add new attribute to research report
agentready research add-attribute \
  --id "attribute_26" \
  --name "New Attribute" \
  --tier 2 \
  --file research.md

# Update metadata (version, date)
agentready research bump-version --type minor

# Lint and format research report
agentready research format research.md
```

**Features**:
- Schema validation (errors vs warnings per research-report-schema.md)
- Automated metadata header generation (version, date in YAML frontmatter)
- Attribute numbering consistency checks (1.1, 1.2, ..., 15.1)
- Citation deduplication and formatting
- Tier distribution balance warnings
- Category coverage analysis
- Markdown formatting enforcement (consistent structure)
- Reference URL reachability checks

**Related**: Research report maintenance, schema compliance, documentation quality

**Notes**:
- Must follow contracts/research-report-schema.md validation rules
- Should prevent invalid reports from being committed
- Could integrate with pre-commit hooks for research report changes
- Consider CLI commands under `agentready research` subcommand
- Tool should be self-documenting (help users fix validation errors)
- Future: Could use LLMs to help generate attribute descriptions from academic papers

---

### Repomix Integration

**Priority**: P4 (Enhancement)

**Description**: Integrate with Repomix (https://github.com/yamadashy/repomix) to generate AI-optimized repository context files for both new and existing repositories.

**Requirements**:
- Generate Repomix output for existing repositories
- Include Repomix configuration in bootstrapped new repositories
- Optional GitHub Actions integration for automatic regeneration
- Support Repomix configuration customization
- Integrate with agentready assessment workflow

**Use Case**:
```bash
# Generate Repomix output for current repository
agentready repomix-generate

# Bootstrap new repo with Repomix integration
agentready init --repo my-project --language python --repomix

# This would:
# 1. Set up Repomix configuration
# 2. Add GitHub Action for automatic regeneration
# 3. Generate initial repository context file
# 4. Include Repomix output in .gitignore appropriately
```

**Features**:
- Automatic Repomix configuration based on repository language
- GitHub Actions workflow for CI/CD integration
- Custom ignore patterns aligned with agentready assessment
- Support for both markdown and XML output formats
- Integration with agentready bootstrap command

**Related**: Repository initialization, AI-assisted development workflows

**Notes**:
- Repomix generates optimized repository context for LLMs
- Could enhance CLAUDE.md with reference to Repomix output
- Should align with existing .gitignore patterns
- Consider adding Repomix freshness check to assessment attributes
- May improve agentready's own repository understanding

---

## Backlog Metadata

**Created**: 2025-11-21
**Last Updated**: 2025-11-21
**Total Items**: 4
