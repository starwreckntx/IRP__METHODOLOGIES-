# IRP Access Panel

**Live Dashboard:** `ledger.hueandlogic.com` (or `username.github.io/irp-accesspanel`)

Multi-model IRP framework visual dashboard with persistent state tracking.

## Features

- **Mnemosyne Ledger Browser** - Concept versioning with SemVer-A-T notation
- **Multi-Model Capability Catalog** - 9-model comparison matrix
- **CRTP Packet Viewer** - Cross-model transmission archive
- **Sprint Dashboard** - Active sprint tracking
- **Chronicle Audit Trail** - Git-backed decision log

## Quick Deploy

### 1. Create GitHub Repository

```bash
# Initialize repo
git init
git add .
git commit -m "feat: Initial IRP Access Panel deployment"

# Create repo on GitHub (replace USERNAME)
gh repo create USERNAME/irp-accesspanel --public --source=. --remote=origin --push

# Enable GitHub Pages
gh repo edit --enable-pages --pages-branch main --pages-path /
```

### 2. Configure Custom Domain (Optional)

**In your DNS provider (hueandlogic.com):**
```
CNAME ledger.hueandlogic.com → USERNAME.github.io
```

**In GitHub repo settings:**
1. Go to Settings → Pages
2. Custom domain: `ledger.hueandlogic.com`
3. Enforce HTTPS: ✅

**Or create CNAME file:**
```bash
echo "ledger.hueandlogic.com" > CNAME
git add CNAME
git commit -m "feat: Add custom domain CNAME"
git push
```

### 3. Access Dashboard

- **Custom domain:** https://ledger.hueandlogic.com
- **GitHub Pages:** https://USERNAME.github.io/irp-accesspanel

## Updating Data

### Update Mnemosyne Ledger

Edit `data/mnemosyne.json`:
```json
{
  "concepts": [
    {
      "handle": "YourConcept",
      "version": "1.0.0",
      "torsion": 0.05,
      "tier": "Hot",
      "centrality": 0.87,
      "stability": 0.96
    }
  ]
}
```

Commit and push:
```bash
git add data/mnemosyne.json
git commit -m "docs: Update Mnemosyne ledger - add YourConcept v1.0.0"
git push
```

### Update Model Catalog

Edit `data/models.json` and commit.

### Add CRTP Packet

Add XML file to `data/packets/`:
```bash
cp new_packet.xml data/packets/0x2B_modelname_response.xml
git add data/packets/
git commit -m "docs: Add CRTP packet from ModelName"
git push
```

## File Structure

```
irp-accesspanel/
├── index.html              # Main dashboard
├── mnemosyne.html          # Ledger browser (PRIORITY 1)
├── catalog.html            # Model capability catalog
├── packets.html            # CRTP packet viewer
├── sprints.html            # Sprint dashboard
├── css/
│   └── styles.css          # Tailwind CSS + custom styles
├── js/
│   ├── mnemosyne.js        # Ledger logic
│   ├── catalog.js          # Catalog visualization
│   ├── packets.js          # CRTP parser
│   └── sprints.js          # Sprint tracking
├── data/
│   ├── mnemosyne.json      # Concept ledger
│   ├── models.json         # 9-model catalog
│   ├── sprints.json        # Sprint state
│   └── packets/            # CRTP XML files
├── CNAME                   # Custom domain (optional)
└── README.md               # This file
```

## Guardian_Codex Compliance

- **CONSENT:** All updates require explicit git commit (human approval)
- **INVITATION:** Dashboard is read-only; edits via git workflow only
- **INTEGRITY:** Chronicle Protocol via git SHA-256 commit hashes
- **GROWTH:** Incremental updates, version-controlled evolution

## P-001-R1: "The Journey IS The Artifact"

Every git commit = decision logged. The dashboard visualizes the journey, not just outcomes.

## License

CC-BY-SA 4.0 (matches IRP framework)
