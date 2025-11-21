# QuickStart: AgentReady Repository Scorer

**Goal**: Get from repository clone to running your first assessment in <5 minutes

**Prerequisites**: Python 3.11+ installed

---

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
# Create and activate virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install agentready
pip install agentready

# Verify installation
agentready --version
```

### Option 2: Install from Source

```bash
# Clone repository
git clone https://github.com/your-org/agentready.git
cd agentready

# Install with development dependencies
pip install -e ".[dev]"

# Verify installation
agentready --version
```

---

## Basic Usage

### Run Assessment on Current Directory

```bash
# Navigate to your repository
cd /path/to/your/repository

# Run assessment (uses current directory)
agentready

# Reports saved to .agentready/ directory
```

### Run Assessment on Specific Repository

```bash
# Assess a different repository
agentready /path/to/other/repository

# Or use relative paths
agentready ../my-project
```

### View Generated Reports

```bash
# Open HTML report in browser
open .agentready/report-latest.html     # macOS
xdg-open .agentready/report-latest.html # Linux
start .agentready/report-latest.html    # Windows

# View Markdown report
cat .agentready/report-latest.md

# Or open in your favorite markdown viewer
code .agentready/report-latest.md  # VS Code
```

---

## Common Options

### Verbose Output

See detailed progress during assessment:

```bash
agentready --verbose
```

Output:
```
🔍 Analyzing repository: /home/user/myproject
✓ Validated git repository
✓ Detected languages: Python, Markdown
✓ Loaded research report (v1.0.0)

📊 Assessing attributes:
  [1/25] ✅ CLAUDE.md Configuration Files... 100/100
  [2/25] ⚠️  Concise Structured Documentation... 60/100
  [3/25] ✅ README Structure... 85/100
  ...
  [25/25] ❌ Performance Benchmarks... Skipped (no benchmarks found)

📄 Generating reports...
  ✓ HTML report: .agentready/report-2025-11-20T14-30-00.html
  ✓ Markdown report: .agentready/report-2025-11-20T14-30-00.md

✨ Assessment complete!
   Score: 72/100 (Silver)
   Duration: 2m 7s
```

### Custom Output Directory

Save reports to a specific location:

```bash
agentready --output-dir /custom/path
```

Reports will be saved to `/custom/path/` instead of `.agentready/`

### Update Research Report

Download latest version of the research report:

```bash
agentready --update-research
```

This updates the bundled research report with the latest findings and recommendations.

---

## Configuration File

### Create Custom Configuration

```bash
# Generate example configuration
agentready --generate-config

# This creates .agentready-config.yaml
```

### Example Configuration

```yaml
# .agentready-config.yaml

# Custom attribute weights (must sum to 1.0)
weights:
  claude_md_file: 0.10          # Increase importance (default: 0.08)
  test_coverage: 0.10           # Increase importance (default: 0.05)
  conventional_commits: 0.05    # Keep default
  # ... other attributes use defaults

# Exclude specific attributes from assessment
excluded_attributes:
  - performance_benchmarks  # Skip if not relevant to your project

# Override language detection
language_overrides:
  Python:
    - "*.pyx"    # Include Cython files as Python
  JavaScript:
    - "*.jsx"
    - "*.tsx"    # Include TypeScript/React files

# Custom output directory (overrides --output-dir flag)
output_dir: reports/agentready
```

### Use Configuration

```bash
# agentready automatically loads .agentready-config.yaml from current directory
agentready

# Or specify a different config file
agentready --config /path/to/config.yaml
```

---

## Understanding Your Results

### Certification Levels

| Level | Score | Meaning |
|-------|-------|---------|
| 🥇 Platinum | 90-100 | Exemplary agent-ready codebase |
| 🥇 Gold | 75-89 | Highly optimized for AI agents |
| 🥈 Silver | 60-74 | Well-suited for AI development |
| 🥉 Bronze | 40-59 | Basic agent compatibility |
| ⛔ Needs Improvement | 0-39 | Significant work needed |

### Prioritizing Improvements

The HTML report's "Next Steps" section shows top improvements ranked by:
1. **Point Potential**: How many points you could gain
2. **Tier Priority**: Tier 1 (Essential) improvements listed first
3. **Ease of Fix**: Quick wins highlighted

**Example Priority**:
```
Next Steps to Gold (need +3 points):
1. Fix README size (+10 potential) - Tier 1 - Easy
2. Add pre-commit hooks (+8 potential) - Tier 2 - Medium
3. Improve dependency freshness (+5 potential) - Tier 2 - Easy
```

Focus on Tier 1 and Tier 2 improvements first for maximum impact.

---

## Tracking Progress Over Time

### Compare Reports

```bash
# Run assessment
agentready

# Make improvements to your repository
# (e.g., add CLAUDE.md, improve test coverage, add pre-commit hooks)

# Run assessment again
agentready

# Compare Markdown reports (they're git-friendly!)
git diff .agentready/report-2025-11-20T14-30-00.md .agentready/report-2025-11-20T16-45-00.md
```

### Commit Reports to Version Control

```bash
# Add reports to git for historical tracking
git add .agentready/report-*.md
git commit -m "docs: add agent-ready assessment (Silver, 72/100)"

# Include in pull requests to show improvements
```

---

## Troubleshooting

### "Not a git repository" Error

```bash
Error: /path/to/directory is not a git repository (no .git directory found)
```

**Solution**: Ensure you're in a git repository root:
```bash
git init  # If needed
git status  # Verify
```

### Missing Tool Warnings

```bash
⏭️ Skipped: Cyclomatic Complexity (missing tool: radon)
```

**Solution**: Install missing language-specific tools:
```bash
# Python complexity analysis
pip install radon

# Multi-language complexity
pip install lizard

# Re-run assessment
agentready
```

### Slow Assessment (>5 minutes)

```bash
⚠️ Assessment took 8m 32s (expected <5m for <10k files)
```

**Causes**:
- Very large repository (>10k files)
- Slow disk I/O
- Many languages to analyze

**Solutions**:
- Use `--exclude` to skip vendor/generated directories
- Run on SSD for faster file scanning
- Consider assessing specific subdirectories

### Permission Errors

```bash
⏭️ Skipped: File Size Limits (permission denied: /protected/directory)
```

**Solution**: Ensure read access to all repository files or accept partial results (agentready continues with available data).

---

## Next Steps

1. **Review HTML Report**: Open `.agentready/report-latest.html` in browser
2. **Check Top Priorities**: Look at "Next Steps" section
3. **Make Improvements**: Start with Tier 1 (Essential) attributes
4. **Re-assess**: Run `agentready` again to see score improvement
5. **Track Progress**: Commit reports to git for historical comparison

---

## Examples

### Assess Multiple Repositories

```bash
#!/bin/bash
# assess-all.sh - Assess all repositories in a directory

for repo in ~/projects/*/; do
    echo "Assessing $repo..."
    agentready "$repo" --output-dir "$repo/.agentready"
done
```

### CI/CD Integration

```yaml
# .github/workflows/agentready.yml
name: Agent-Ready Assessment

on:
  pull_request:
    branches: [ main ]

jobs:
  assess:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install agentready
        run: pip install agentready

      - name: Run assessment
        run: agentready --output-dir reports/

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: agentready-report
          path: reports/report-latest.html

      - name: Comment score on PR
        run: |
          SCORE=$(cat reports/report-latest.md | grep "Overall Score" | awk '{print $3}')
          echo "Agent-Ready Score: $SCORE" >> $GITHUB_STEP_SUMMARY
```

### Custom Weighting for Organization

```yaml
# .agentready-config.yaml
# Enterprise configuration emphasizing security and testing

weights:
  # Security-focused (30% total)
  security_scanning: 0.10
  secrets_management: 0.10
  dependency_freshness: 0.10

  # Testing-focused (25% total)
  test_coverage: 0.10
  test_naming: 0.08
  pre_commit_hooks: 0.07

  # Documentation (20% total)
  claude_md_file: 0.08
  readme_structure: 0.07
  inline_documentation: 0.05

  # Code quality (15% total)
  type_annotations: 0.06
  cyclomatic_complexity: 0.05
  code_smells: 0.04

  # Remaining attributes split remaining 10%
  # (not listed = use calculated defaults from remaining weight)
```

---

## Getting Help

```bash
# Show all available commands and options
agentready --help

# Show version information
agentready --version

# Show research report version
agentready --research-version

# Generate example configuration
agentready --generate-config

# Validate existing configuration
agentready --validate-config
```

---

## Quick Reference

| Command | Purpose |
|---------|---------|
| `agentready` | Assess current directory |
| `agentready /path` | Assess specific repository |
| `agentready --verbose` | Show detailed progress |
| `agentready --output-dir DIR` | Custom output location |
| `agentready --config FILE` | Use custom configuration |
| `agentready --update-research` | Update research report |
| `agentready --generate-config` | Create example config |
| `agentready --help` | Show all options |

---

**Time from install to first report**: ~2 minutes
**Typical assessment duration**: 2-5 minutes
**Report formats**: HTML (interactive) + Markdown (version control)
**Default output**: `.agentready/` directory

🎯 **Goal Achieved**: You now have a comprehensive assessment of your repository's AI-readiness!
