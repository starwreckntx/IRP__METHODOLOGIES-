/**
 * IRP Dashboard - Main Application
 * Orchestrates all dashboard functionality
 */

class IRPDashboard {
    constructor() {
        this.api = window.GitHubAPI;
        this.skillsData = [];
        this.ledgerData = null;
        this.currentView = 'overview';
        
        this.init();
    }

    async init() {
        this.bindEvents();
        await this.loadInitialData();
        this.updateSyncStatus(true);
    }

    bindEvents() {
        // Navigation
        document.querySelectorAll('.nav-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.switchView(item.dataset.view);
            });
        });

        // Sync button
        document.getElementById('syncBtn').addEventListener('click', () => {
            this.syncData();
        });

        // Skill search
        document.getElementById('skillSearch').addEventListener('input', (e) => {
            this.filterSkills(e.target.value);
        });

        // Modal close
        document.getElementById('modalClose').addEventListener('click', () => {
            this.closeModal();
        });

        // Click outside modal to close
        document.getElementById('skillModal').addEventListener('click', (e) => {
            if (e.target.id === 'skillModal') {
                this.closeModal();
            }
        });
    }

    switchView(viewName) {
        // Update nav
        document.querySelectorAll('.nav-item').forEach(item => {
            item.classList.toggle('active', item.dataset.view === viewName);
        });

        // Update views
        document.querySelectorAll('.view').forEach(view => {
            view.classList.toggle('active', view.id === `view-${viewName}`);
        });

        this.currentView = viewName;

        // Load view-specific data
        if (viewName === 'topology') {
            this.renderTopology();
        }
    }

    async loadInitialData() {
        try {
            // Load all data in parallel
            const [manifest, ledger, commits, integration] = await Promise.all([
                this.api.getSkillsManifest(),
                this.api.getLedgerState(),
                this.api.getCommits(5),
                this.api.getIntegrationContents()
            ]);

            this.skillsData = manifest?.skills || [];
            this.ledgerData = ledger;

            this.renderOverview(commits);
            this.renderSkills();
            this.renderLedger();
            this.renderProtocols();
            this.renderIntegration(integration);

        } catch (error) {
            console.error('Failed to load data:', error);
            this.updateSyncStatus(false);
        }
    }

    async syncData() {
        this.updateSyncStatus(false, 'Syncing...');
        this.api.clearCache();
        await this.loadInitialData();
        this.updateSyncStatus(true);
    }

    updateSyncStatus(connected, text = null) {
        const statusEl = document.getElementById('syncStatus');
        const dot = statusEl.querySelector('.status-dot');
        const textEl = statusEl.querySelector('.status-text');
        
        dot.classList.toggle('connected', connected);
        textEl.textContent = text || (connected ? 'Connected' : 'Disconnected');
    }


    // === RENDER METHODS ===

    renderOverview(commits) {
        // Stats
        document.getElementById('totalSkills').textContent = this.skillsData.length || '--';
        
        // Count unique categories
        const categories = new Set(this.skillsData.map(s => s.category?.split('/')[0]));
        document.getElementById('totalCategories').textContent = categories.size || '--';

        // Ledger stats
        const entries = this.ledgerData?.entries || [];
        document.getElementById('ledgerEntries').textContent = entries.length || '--';
        document.getElementById('activeHandshakes').textContent = 
            this.ledgerData?.active_handshakes?.length || '0';

        // Recent activity
        const activityList = document.getElementById('activityList');
        if (commits && commits.length > 0) {
            activityList.innerHTML = commits.map(commit => `
                <div class="activity-item">
                    <div class="activity-icon">📝</div>
                    <div class="activity-content">
                        <div class="activity-title">${this.escapeHtml(commit.commit.message.split('\n')[0])}</div>
                        <div class="activity-time">${this.formatDate(commit.commit.author.date)}</div>
                    </div>
                </div>
            `).join('');
        } else {
            activityList.innerHTML = '<div class="loading">No recent activity</div>';
        }

        // Protocol status
        const protocolStatus = document.getElementById('protocolStatus');
        protocolStatus.innerHTML = `
            <div class="protocol-item">
                <span class="protocol-name">Mnemosyne Protocol</span>
                <span class="protocol-status-badge">v1.1_Integrated</span>
            </div>
            <div class="protocol-item">
                <span class="protocol-name">CRTP</span>
                <span class="protocol-status-badge">v1.2</span>
            </div>
            <div class="protocol-item">
                <span class="protocol-name">Codex Law</span>
                <span class="protocol-status-badge">ACTIVE</span>
            </div>
        `;
    }

    renderSkills() {
        const grid = document.getElementById('skillsGrid');
        
        if (!this.skillsData.length) {
            grid.innerHTML = '<div class="loading">No skills found</div>';
            return;
        }

        grid.innerHTML = this.skillsData.map(skill => `
            <div class="skill-card" data-path="${skill.path || skill.name}">
                <div class="skill-name">${skill.name || skill.skill_id}</div>
                <div class="skill-category">${skill.category || 'uncategorized'}</div>
                <div class="skill-desc">${skill.description || 'No description available'}</div>
            </div>
        `).join('');

        // Add click handlers
        grid.querySelectorAll('.skill-card').forEach(card => {
            card.addEventListener('click', () => {
                this.showSkillDetail(card.dataset.path);
            });
        });
    }

    filterSkills(query) {
        const grid = document.getElementById('skillsGrid');
        const cards = grid.querySelectorAll('.skill-card');
        const lowerQuery = query.toLowerCase();

        cards.forEach(card => {
            const name = card.querySelector('.skill-name').textContent.toLowerCase();
            const category = card.querySelector('.skill-category').textContent.toLowerCase();
            const desc = card.querySelector('.skill-desc').textContent.toLowerCase();
            
            const matches = name.includes(lowerQuery) || 
                           category.includes(lowerQuery) || 
                           desc.includes(lowerQuery);
            
            card.style.display = matches ? '' : 'none';
        });
    }

    async showSkillDetail(skillPath) {
        const modal = document.getElementById('skillModal');
        const title = document.getElementById('modalTitle');
        const body = document.getElementById('modalBody');

        title.textContent = skillPath;
        body.innerHTML = '<div class="loading">Loading skill...</div>';
        modal.classList.add('open');

        try {
            const content = await this.api.getSkillContent(skillPath);
            if (content) {
                body.innerHTML = `<div class="skill-content">${marked.parse(content)}</div>`;
            } else {
                body.innerHTML = '<div class="loading">Skill content not found</div>';
            }
        } catch (e) {
            body.innerHTML = '<div class="loading">Failed to load skill</div>';
        }
    }

    closeModal() {
        document.getElementById('skillModal').classList.remove('open');
    }


    renderLedger() {
        const content = document.getElementById('ledgerContent');
        
        if (!this.ledgerData) {
            content.innerHTML = '<div class="loading">No ledger data available</div>';
            return;
        }

        const entries = this.ledgerData.entries || [];
        const storage = this.ledgerData.storage_tiers || { HOT: 0, WARM: 0, COLD: 0 };

        // Update stats
        document.getElementById('ledgerHot').textContent = storage.HOT || 0;
        document.getElementById('ledgerWarm').textContent = storage.WARM || 0;
        document.getElementById('ledgerCold').textContent = storage.COLD || 0;

        // Render entries
        if (entries.length === 0) {
            content.innerHTML = '<div class="loading">No ledger entries</div>';
            return;
        }

        content.innerHTML = entries.map(entry => `
            <div class="ledger-entry">
                <div>
                    <span class="entry-type ${entry.type?.toLowerCase()}">${entry.type}</span>
                    <span style="margin-left: 8px">${entry.id || entry.content?.substring(0, 40) || 'Unknown'}</span>
                </div>
                <div class="entry-state">${entry.state || 'UNKNOWN'} | ${entry.storage || 'N/A'}</div>
            </div>
        `).join('');
    }

    renderProtocols() {
        const grid = document.getElementById('protocolGrid');
        
        const protocols = [
            { name: 'Mnemosyne Protocol', version: 'v1.1_Integrated', status: 'ACTIVE', desc: 'Cross-model semantic memory' },
            { name: 'CRTP', version: 'v1.2', status: 'ACTIVE', desc: 'CaaS Relational Transport Protocol' },
            { name: 'Codex Law', version: '1.0', status: 'ENFORCED', desc: 'CONSENT, INVITATION, INTEGRITY, GROWTH' },
            { name: 'Chronicle Protocol', version: '5.0', status: 'ACTIVE', desc: 'SHA-256 cryptographic logging' },
            { name: 'Xylem Protocol', version: '1.0', status: 'ACTIVE', desc: 'Entropy distribution & resource management' },
            { name: 'Guardian Protocol', version: '1.0', status: 'STANDBY', desc: 'Ethical oversight & cognitive trap detection' },
            { name: 'Antidote Protocol', version: '1.0', status: 'MONITORING', desc: 'Ideological drift detection' },
            { name: 'RTC', version: '2.0', status: 'AVAILABLE', desc: 'Recursive Thought Committee' }
        ];

        grid.innerHTML = protocols.map(p => `
            <div class="protocol-card">
                <div class="protocol-name">
                    ${p.name}
                    <span class="protocol-status-badge">${p.status}</span>
                </div>
                <div class="protocol-version">${p.version}</div>
                <p style="color: var(--text-secondary); font-size: 13px; margin-top: 8px;">${p.desc}</p>
            </div>
        `).join('');
    }

    renderIntegration(contents) {
        const tree = document.getElementById('archiveTree');
        
        if (!contents || contents.length === 0) {
            tree.innerHTML = '<div class="loading">No integration files found</div>';
            return;
        }

        const folders = contents.filter(item => item.type === 'dir');
        const files = contents.filter(item => item.type === 'file');

        let html = '';

        // Render folders
        folders.forEach(folder => {
            html += `
                <div class="archive-folder">
                    <div class="folder-name" onclick="dashboard.toggleFolder(this)">
                        <span>📁</span>
                        <span>${folder.name}</span>
                    </div>
                    <div class="folder-contents" data-path="${folder.path}">
                        <div class="loading">Click to load...</div>
                    </div>
                </div>
            `;
        });

        // Render files
        files.forEach(file => {
            html += `<div class="archive-file" onclick="dashboard.viewFile('${file.path}')">${file.name}</div>`;
        });

        tree.innerHTML = html;
    }

    async toggleFolder(element) {
        const contents = element.nextElementSibling;
        const isOpen = contents.classList.contains('open');
        
        if (isOpen) {
            contents.classList.remove('open');
        } else {
            contents.classList.add('open');
            // Load folder contents if not already loaded
            if (contents.querySelector('.loading')) {
                try {
                    const path = contents.dataset.path;
                    const items = await this.api.getContents(path);
                    contents.innerHTML = items.map(item => 
                        `<div class="archive-file" onclick="dashboard.viewFile('${item.path}')">${item.name}</div>`
                    ).join('');
                } catch (e) {
                    contents.innerHTML = '<div class="loading">Failed to load</div>';
                }
            }
        }
    }

    async viewFile(path) {
        try {
            const content = await this.api.getFileContent(path);
            const modal = document.getElementById('skillModal');
            const title = document.getElementById('modalTitle');
            const body = document.getElementById('modalBody');

            title.textContent = path.split('/').pop();
            
            if (path.endsWith('.md')) {
                body.innerHTML = marked.parse(content);
            } else if (path.endsWith('.json')) {
                body.innerHTML = `<pre>${this.escapeHtml(JSON.stringify(JSON.parse(content), null, 2))}</pre>`;
            } else if (path.endsWith('.xml')) {
                body.innerHTML = `<pre>${this.escapeHtml(content)}</pre>`;
            } else {
                body.innerHTML = `<pre>${this.escapeHtml(content)}</pre>`;
            }

            modal.classList.add('open');
        } catch (e) {
            console.error('Failed to load file:', e);
        }
    }

    renderTopology() {
        const canvas = document.getElementById('topologyCanvas');
        const ctx = canvas.getContext('2d');
        
        // Set canvas size
        canvas.width = canvas.parentElement.offsetWidth;
        canvas.height = canvas.parentElement.offsetHeight;

        // Clear
        ctx.fillStyle = '#161b22';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // Draw topology if we have data
        if (!this.ledgerData || !this.ledgerData.topology) {
            ctx.fillStyle = '#8b949e';
            ctx.font = '14px Inter';
            ctx.textAlign = 'center';
            ctx.fillText('No topology data available', canvas.width / 2, canvas.height / 2);
            return;
        }

        // Simple node visualization
        const nodes = this.ledgerData.topology.nodes || [];
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;
        const radius = Math.min(canvas.width, canvas.height) * 0.35;

        nodes.forEach((node, i) => {
            const angle = (2 * Math.PI * i) / nodes.length;
            const x = centerX + radius * Math.cos(angle);
            const y = centerY + radius * Math.sin(angle);

            // Draw node
            ctx.beginPath();
            ctx.arc(x, y, 20, 0, 2 * Math.PI);
            ctx.fillStyle = node.state === 'ACTIVE' ? '#3fb950' : 
                           node.state === 'DORMANT' ? '#d29922' : '#a371f7';
            ctx.fill();

            // Draw label
            ctx.fillStyle = '#e6edf3';
            ctx.font = '11px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(node.id || `Node ${i}`, x, y + 35);
        });

        // Draw edges
        const edges = this.ledgerData.topology.edges || [];
        ctx.strokeStyle = '#30363d';
        ctx.lineWidth = 1;
        
        edges.forEach(edge => {
            const fromIdx = nodes.findIndex(n => n.id === edge.from);
            const toIdx = nodes.findIndex(n => n.id === edge.to);
            if (fromIdx >= 0 && toIdx >= 0) {
                const fromAngle = (2 * Math.PI * fromIdx) / nodes.length;
                const toAngle = (2 * Math.PI * toIdx) / nodes.length;
                
                ctx.beginPath();
                ctx.moveTo(centerX + radius * Math.cos(fromAngle), centerY + radius * Math.sin(fromAngle));
                ctx.lineTo(centerX + radius * Math.cos(toAngle), centerY + radius * Math.sin(toAngle));
                ctx.stroke();
            }
        });
    }

    // === UTILITY METHODS ===

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    formatDate(dateString) {
        const date = new Date(dateString);
        const now = new Date();
        const diff = now - date;
        
        if (diff < 60000) return 'Just now';
        if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
        if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
        return date.toLocaleDateString();
    }
}

// Initialize dashboard
const dashboard = new IRPDashboard();
