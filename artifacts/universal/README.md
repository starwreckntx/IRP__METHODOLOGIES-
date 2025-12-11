# Universal Artifacts Repository

**Version:** 1.0  
**Created:** 2025-12-07  
**Purpose:** Centralized storage for all generated artifacts, visualizations, and dashboards

## Directory Structure

```
artifacts/
├── universal/                    # Universal artifact storage
│   ├── README.md                # This file
│   ├── visualizations/          # Dashboard components & data viz
│   │   ├── topology-graph.html  # Semantic topology visualizer
│   │   ├── rpv-calculator.html  # Interactive RPV calculator
│   │   └── ledger-viewer.html   # Ledger state viewer
│   ├── ledger-entries/          # Generated ledger entries
│   ├── packets/                 # CRTP transmission packets
│   └── chronicles/              # Creative chronicle outputs
├── dashboard/                   # Main web dashboard
│   ├── index.html
│   ├── css/styles.css
│   └── js/
│       ├── app.js
│       ├── github-api.js
│       └── visualizations.js
└── exports/                     # Export outputs
```

## Artifact Categories

### 1. Ledger Entries
- XML format following `ledger-entry.xsd`
- Naming: `LE-{DATE}-{TIME}-{TYPE}.xml`
- Auto-indexed in `ledger-state-live.json`

### 2. Visualizations
- Interactive HTML/JS components
- Self-contained (no external dependencies beyond CDN)
- Real-time data from GitHub API

### 3. CRTP Packets
- Cross-model transmission packets
- Naming: `CRTP-{VERSION}-{TYPE}-{TIMESTAMP}.xml`
- Verified with SHA-256 hashes

### 4. Chronicles
- Session summaries in Creative Chronicle format
- Version 5.0 schema compliance
- Auto-generated at session boundaries

## Usage

### Adding New Artifacts

```bash
# Copy to appropriate subfolder
cp new-artifact.xml artifacts/universal/ledger-entries/

# Update manifest (if applicable)
# Artifacts are auto-discovered by dashboard
```

### Accessing via Dashboard

The main dashboard (`artifacts/dashboard/index.html`) automatically scans:
1. `universal/visualizations/` for interactive components
2. `universal/ledger-entries/` for artifact display
3. GitHub API for real-time repo data

### Generating Visualizations

```python
# Example: Generate topology visualization data
from skills.rpv_kernel import RPVKernel

kernel = RPVKernel()
# ... generate data ...
# Export to artifacts/universal/visualizations/
```

## Integration Points

| Source | Target | Method |
|--------|--------|--------|
| Mnemosyne Ledger | `ledger-entries/` | Automatic on state change |
| CRTP Forge | `packets/` | Manual or triggered |
| Chronicle Protocol | `chronicles/` | Session boundary |
| Dashboard | All | Real-time scan |

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Ledger Entry | `LE-{YYYYMMDD}-{HHMMSS}-{ID}.xml` | `LE-20251207-064500-RPVK.xml` |
| Visualization | `{name}-{version}.html` | `topology-graph-v1.html` |
| CRTP Packet | `CRTP-{code}-{target}-{timestamp}.xml` | `CRTP-0x13-gemini-20251207.xml` |
| Chronicle | `CC-{session}-{timestamp}.xml` | `CC-SESSION001-20251207.xml` |

## Maintenance

### Cleanup Policy
- HOT artifacts: Keep until state change
- WARM artifacts: 30-day retention
- COLD artifacts: Permanent archive

### Backup
Artifacts are committed to GitHub with each significant update.

---

*Part of IRP Framework v2.0 | Mnemosyne Protocol v1.1_Integrated*
