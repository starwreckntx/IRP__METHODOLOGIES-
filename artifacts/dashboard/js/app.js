/**
 * IRP Dashboard - Main Application
 * Enhanced real-time data visualization
 * Version: 2.0
 */

class IRPDashboard {
    constructor() {
        this.api = window.GitHubAPI;
        this.realtime = window.RealtimeManager;
        this.skillsData = [];
        this.ledgerData = null;
        this.currentView = 'overview';
        this.lastUpdate = null;
        
        this.init();
    }

    async init() {
        this.bindEvents();
        this.showLoading();
        await this.loadInitialData();
        this.updateSyncStatus(true);
        this.setupRealtime();
    }

    setupRealtime() {
        // Register update callbacks
        this.realtime.onUpdate('overview', () => this.refreshOverview());
        this.realtime.onUpdate('ledger', () => this.refreshLedger());
        
        // Start auto-refresh (every 2 minutes)
        this.realtime.start(120000);
    }

    showLoading() {
        document.querySelectorAll('.loading').forEach(el => {
            el.textContent = 'Loading...';
        });
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

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
            if (e.ctrlKey && e.key === 'r') {
                e.preventDefault();
                this.syncData();
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
            setTimeout(() => this.renderTopology(), 100);
        }
    }

    async loadInitialData() {
        try {
            // Load all data in parallel
            const [manifest, ledger, commits, integration, repoInfo] = await Promise.all([
                this.api.getSkillsManifest(),
                this.api.getLedgerState(),
                this.api.getCommits(10),
                this.api.getIntegrationContents(),
                this.api.getRepoInfo()
            ]);

            this.skillsData = manifest?.skills || [];
            this.ledgerData = ledger;
            this.repoInfo = repoInfo;
            this.lastUpdate = new Date();

            this.renderOverview(commits);
            this.renderSkills();
            this.renderLedger();
            this.renderProtocols();
            this.renderIntegration(integration);

        } catch (error) {
            console.error('Failed to load data:', error);
            this.updateSyncStatus(false, error.message);
        }
    }

    async refreshOverview() {
        try {
            const commits = await this.api.getCommits(10);
            this.renderOverview(commits);
        } catch (e) {
            console.error('Failed to refresh overview:', e);
        }
    }

    async refreshLedger() {
        try {
            this.ledgerData = await this.api.getLedgerState();
            this.renderLedger();
        } catch (e) {
            console.error('Failed to refresh ledger:', e);
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
        
        if (text) {
            textEl.textContent = text;
        } else if (connected && this.lastUpdate) {
            const timeStr = this.lastUpdate.toLocaleTimeString();
            textEl.textContent = `Connected · Updated ${timeStr}`;
        } else {
            textEl.textContent = connected ? 'Connected' : 'Disconnected';
        }
    }

    // === RENDER METHODS ===

    renderOverview(commits) {
        // Stats
        document.getElementById('totalSkills').textContent = this.skillsData.length || '--';
        
        // Count unique categories
        const categories = new Set(this.skillsData.map(s => {
            const cat = s.category?.split('/')[0];
            return cat || 'uncategorized';
        }));
        document.getElementById('totalCategories').textContent = categories.size || '--';

        // Ledger stats
        const stats = this.ledgerData?.statistics || {};
        document.getElementById('ledgerEntries').textContent = stats.total_entries || '--';
        document.getElementById('activeHandshakes').textContent = 
            this.ledgerData?.circulation?.active_handshakes?.length || '0';

        // Recent activity
        const activityList = document.getElementById('activityList');
        if (commits && commits.length > 0) {
            activityList.innerHTML = commits.map(commit => `
                <div class="activity-item">
                    <div class="activity-icon">📝</div>
                    <div class="activity-content">
                        <div class="activity-title" title="${this.escapeHtml(commit.commit.message)}">
                            ${this.escapeHtml(commit.commit.message.split('\n')[0].substring(0, 50))}
                        </div>
                        <div class="activity-time">${this.formatDate(commit.commit.author.date)}</div>
                    </div>
                </div>
            `).join('');
        } else {
            activityList.innerHTML = '<div class="loading">No recent activity</div>';
        }

        // Protocol status
        const protocolStatus = document.getElementById('protocolStatus');
        const handshakes = this.ledgerData?.circulation?.active_handshakes || [];
        
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
                <span class="protocol-status-badge">ENFORCED</span>
            </div>
            <div class="protocol-item">
                <span class="protocol-name">Active Handshakes</span>
                <span class="protocol-status-badge">${handshakes.length}</span>
            </div>
            ${handshakes.map(h => `
                <div class="protocol-item" style="padding-left: 20px;">
                    <span class="protocol-name" style="font-size: 12px; color: var(--text-secondary);">↳ ${h.partner}</span>
                    <span class="protocol-status-badge" style="font-size: 10px;">${h.status}</span>
                </div>
            `).join('')}
        `;
    }

    renderSkills() {
        const grid = document.getElementById('skillsGrid');
        
        if (!this.skillsData.length) {
            grid.innerHTML = '<div class="loading">No skills found in manifest</div>';
            return;
        }

        grid.innerHTML = this.skillsData.map(skill => {
            const name = skill.name || skill.skill_id || 'Unknown';
            const category = skill.category || 'uncategorized';
            const description = skill.description || 'No description available';
            const path = skill.path || name;
            
            return `
                <div class="skill-card" data-path="${path}">
                    <div class="skill-name">${name}</div>
                    <div class="skill-category">${category}</div>
                    <div class="skill-desc">${description}</div>
                </div>
            `;
        }).join('');

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
            body.innerHTML = `<div class="loading">Failed to load skill: ${e.message}</div>`;
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
        const storage = this.ledgerData.statistics?.by_storage || { HOT: 0, WARM: 0, COLD: 0 };

        // Update stats
        document.getElementById('ledgerHot').textContent = storage.HOT || 0;
        document.getElementById('ledgerWarm').textContent = storage.WARM || 0;
        document.getElementById('ledgerCold').textContent = storage.COLD || 0;

        // Render entries
        if (entries.length === 0) {
            content.innerHTML = '<div class="loading">No ledger entries</div>';
            return;
        }

        content.innerHTML = entries.map(entry => {
            const type = entry.type?.toLowerCase() || 'unknown';
            const id = entry.id || 'Unknown';
            const state = entry.state || 'UNKNOWN';
            const storage = entry.storage || 'N/A';
            const tags = entry.tags?.join(', ') || '';
            
            return `
                <div class="ledger-entry" title="${tags}">
                    <div>
                        <span class="entry-type ${type}">${entry.type || 'UNKNOWN'}</span>
                        <span style="margin-left: 8px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
                            ${id}
                        </span>
                    </div>
                    <div class="entry-state">${state} | ${storage}</div>
                </div>
            `;
        }).join('');
    }

    renderProtocols() {
        const grid = document.getElementById('protocolGrid');
        
        const protocols = [
            { name: 'Mnemosyne Protocol', version: 'v1.1_Integrated', status: 'ACTIVE', desc: 'Cross-model semantic memory with topology-based organization' },
            { name: 'CRTP', version: 'v1.2', status: 'ACTIVE', desc: 'CaaS Relational Transport Protocol for cross-model packets' },
            { name: 'Codex Law', version: '1.0', status: 'ENFORCED', desc: 'CONSENT, INVITATION, INTEGRITY, GROWTH' },
            { name: 'RPV Kernel', version: '1.0', status: 'ACTIVE', desc: 'Recursive Process Valuation for artifact value calculation' },
            { name: 'Chronicle Protocol', version: '5.0', status: 'ACTIVE', desc: 'SHA-256 cryptographic logging and session documentation' },
            { name: 'Xylem Protocol', version: '1.0', status: 'ACTIVE', desc: 'Entropy distribution & resource management (Pool/Mode 9)' },
            { name: 'Guardian Protocol', version: '1.0', status: 'STANDBY', desc: 'Ethical oversight & cognitive trap detection' },
            { name: 'Antidote Protocol', version: '1.0', status: 'MONITORING', desc: 'Ideological drift detection and correction' },
            { name: 'RTC', version: '2.0', status: 'AVAILABLE', desc: 'Recursive Thought Committee for multi-perspective analysis' }
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
                        <div class="loading">Click to load contents...</div>
                    </div>
                </div>
            `;
        });

        // Render files
        files.forEach(file => {
            const icon = this.getFileIcon(file.name);
            html += `<div class="archive-file" onclick="dashboard.viewFile('${file.path}')">${icon} ${file.name}</div>`;
        });

        tree.innerHTML = html;
    }

    getFileIcon(filename) {
        if (filename.endsWith('.xml')) return '📄';
        if (filename.endsWith('.md')) return '📝';
        if (filename.endsWith('.json')) return '🔧';
        if (filename.endsWith('.zip')) return '📦';
        if (filename.endsWith('.jpg') || filename.endsWith('.png')) return '🖼️';
        return '📄';
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
                    contents.innerHTML = items.map(item => {
                        const icon = this.getFileIcon(item.name);
                        if (item.type === 'dir') {
                            return `
                                <div class="archive-folder">
                                    <div class="folder-name" onclick="dashboard.toggleFolder(this)">
                                        <span>📁</span>
                                        <span>${item.name}</span>
                                    </div>
                                    <div class="folder-contents" data-path="${item.path}">
                                        <div class="loading">Click to load...</div>
                                    </div>
                                </div>
                            `;
                        }
                        return `<div class="archive-file" onclick="dashboard.viewFile('${item.path}')">${icon} ${item.name}</div>`;
                    }).join('');
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
                body.innerHTML = `<div class="skill-content">${marked.parse(content)}</div>`;
            } else if (path.endsWith('.json')) {
                try {
                    const formatted = JSON.stringify(JSON.parse(content), null, 2);
                    body.innerHTML = `<pre style="font-size: 12px; overflow-x: auto;">${this.escapeHtml(formatted)}</pre>`;
                } catch {
                    body.innerHTML = `<pre>${this.escapeHtml(content)}</pre>`;
                }
            } else if (path.endsWith('.xml')) {
                body.innerHTML = `<pre style="font-size: 12px; overflow-x: auto;">${this.escapeHtml(content)}</pre>`;
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
        const container = canvas.parentElement;
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;

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

        const topology = this.ledgerData.topology;
        const clusters = topology.clusters || [];
        const centerX = canvas.width / 2;
        const centerY = canvas.height / 2;

        // Draw clusters
        const clusterRadius = Math.min(canvas.width, canvas.height) * 0.35;
        const colors = {
            'Mnemosyne_Core': '#58a6ff',
            'Dormant_Aesthetic': '#d29922',
            'Valuation_System': '#a371f7'
        };

        clusters.forEach((cluster, clusterIdx) => {
            const clusterAngle = (2 * Math.PI * clusterIdx) / clusters.length;
            const clusterCenterX = centerX + clusterRadius * 0.5 * Math.cos(clusterAngle);
            const clusterCenterY = centerY + clusterRadius * 0.5 * Math.sin(clusterAngle);
            
            const nodes = cluster.nodes || [];
            const nodeRadius = Math.min(80, 150 / Math.sqrt(nodes.length));
            const color = colors[cluster.name] || '#3fb950';

            // Draw cluster label
            ctx.fillStyle = color;
            ctx.font = 'bold 12px Inter';
            ctx.textAlign = 'center';
            ctx.fillText(cluster.name.replace(/_/g, ' '), clusterCenterX, clusterCenterY - nodeRadius - 20);

            // Draw nodes in cluster
            nodes.forEach((nodeName, nodeIdx) => {
                const nodeAngle = (2 * Math.PI * nodeIdx) / nodes.length;
                const x = clusterCenterX + nodeRadius * Math.cos(nodeAngle);
                const y = clusterCenterY + nodeRadius * Math.sin(nodeAngle);

                // Draw node
                ctx.beginPath();
                ctx.arc(x, y, 15, 0, 2 * Math.PI);
                ctx.fillStyle = color;
                ctx.fill();
                ctx.strokeStyle = '#30363d';
                ctx.lineWidth = 2;
                ctx.stroke();

                // Draw label
                ctx.fillStyle = '#e6edf3';
                ctx.font = '10px Inter';
                ctx.textAlign = 'center';
                const shortName = nodeName.replace(/_/g, ' ').substring(0, 15);
                ctx.fillText(shortName, x, y + 28);
            });

            // Draw connections within cluster
            ctx.strokeStyle = color;
            ctx.globalAlpha = 0.3;
            ctx.lineWidth = 1;
            for (let i = 0; i < nodes.length; i++) {
                for (let j = i + 1; j < nodes.length; j++) {
                    const angle1 = (2 * Math.PI * i) / nodes.length;
                    const angle2 = (2 * Math.PI * j) / nodes.length;
                    ctx.beginPath();
                    ctx.moveTo(
                        clusterCenterX + nodeRadius * Math.cos(angle1),
                        clusterCenterY + nodeRadius * Math.sin(angle1)
                    );
                    ctx.lineTo(
                        clusterCenterX + nodeRadius * Math.cos(angle2),
                        clusterCenterY + nodeRadius * Math.sin(angle2)
                    );
                    ctx.stroke();
                }
            }
            ctx.globalAlpha = 1;
        });

        // Draw central hub
        ctx.beginPath();
        ctx.arc(centerX, centerY, 25, 0, 2 * Math.PI);
        ctx.fillStyle = '#3fb950';
        ctx.fill();
        ctx.strokeStyle = '#238636';
        ctx.lineWidth = 3;
        ctx.stroke();

        ctx.fillStyle = '#fff';
        ctx.font = 'bold 12px Inter';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('IRP', centerX, centerY);

        // Draw connections to central hub
        ctx.strokeStyle = '#30363d';
        ctx.lineWidth = 1;
        clusters.forEach((cluster, idx) => {
            const angle = (2 * Math.PI * idx) / clusters.length;
            const clusterCenterX = centerX + clusterRadius * 0.5 * Math.cos(angle);
            const clusterCenterY = centerY + clusterRadius * 0.5 * Math.sin(angle);
            
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.lineTo(clusterCenterX, clusterCenterY);
            ctx.stroke();
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
        if (diff < 604800000) return `${Math.floor(diff / 86400000)}d ago`;
        return date.toLocaleDateString();
    }
}

// Initialize dashboard
const dashboard = new IRPDashboard();
