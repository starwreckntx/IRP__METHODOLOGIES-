/**
 * IRP Dashboard - Enhanced GitHub API Client
 * Real-time data fetching from GitHub repository
 * Version: 2.0
 */

const GitHubAPI = {
    owner: 'starwreckntx',
    repo: 'IRP__METHODOLOGIES-',
    baseUrl: 'https://api.github.com',
    rawBaseUrl: 'https://raw.githubusercontent.com',
    cache: new Map(),
    cacheTimeout: 300000, // 5 minutes
    rateLimitRemaining: 60,
    rateLimitReset: null,

    /**
     * Core API request handler with caching and rate limiting
     */
    async request(endpoint, options = {}) {
        const cacheKey = endpoint;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                headers: {
                    'Accept': 'application/vnd.github.v3+json',
                    ...options.headers
                },
                ...options
            });

            // Track rate limiting
            this.rateLimitRemaining = parseInt(response.headers.get('X-RateLimit-Remaining') || 60);
            this.rateLimitReset = parseInt(response.headers.get('X-RateLimit-Reset') || 0);

            if (!response.ok) {
                if (response.status === 403 && this.rateLimitRemaining === 0) {
                    throw new Error('GitHub API rate limit exceeded. Please try again later.');
                }
                throw new Error(`GitHub API error: ${response.status}`);
            }

            const data = await response.json();
            this.cache.set(cacheKey, { data, timestamp: Date.now() });
            return data;
        } catch (error) {
            console.error('GitHub API request failed:', error);
            throw error;
        }
    },

    /**
     * Fetch raw file content from GitHub
     */
    async getRawContent(path) {
        const cacheKey = `raw:${path}`;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        try {
            const url = `${this.rawBaseUrl}/${this.owner}/${this.repo}/main/${path}`;
            const response = await fetch(url);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch ${path}: ${response.status}`);
            }

            const data = await response.text();
            this.cache.set(cacheKey, { data, timestamp: Date.now() });
            return data;
        } catch (error) {
            console.error('Failed to fetch raw content:', error);
            return null;
        }
    },

    /**
     * Get repository information
     */
    async getRepoInfo() {
        return this.request(`/repos/${this.owner}/${this.repo}`);
    },

    /**
     * Get recent commits
     */
    async getCommits(count = 10) {
        return this.request(`/repos/${this.owner}/${this.repo}/commits?per_page=${count}`);
    },

    /**
     * Get directory contents
     */
    async getContents(path = '') {
        return this.request(`/repos/${this.owner}/${this.repo}/contents/${path}`);
    },

    /**
     * Get skills manifest
     */
    async getSkillsManifest() {
        const content = await this.getRawContent('skills_manifest.json');
        if (content) {
            try {
                return JSON.parse(content);
            } catch (e) {
                console.error('Failed to parse skills manifest:', e);
                return null;
            }
        }
        return null;
    },

    /**
     * Get ledger state
     */
    async getLedgerState() {
        const content = await this.getRawContent('skills/cross-model/mnemosyne-ledger/state/ledger-state-live.json');
        if (content) {
            try {
                return JSON.parse(content).ledger_state;
            } catch (e) {
                console.error('Failed to parse ledger state:', e);
                return null;
            }
        }
        return null;
    },

    /**
     * Get skill content
     */
    async getSkillContent(skillPath) {
        // Handle different path formats
        let path = skillPath;
        if (!path.includes('/')) {
            path = `skills/${skillPath}/SKILL.md`;
        } else if (!path.endsWith('.md')) {
            path = `skills/${path}/SKILL.md`;
        }
        return this.getRawContent(path);
    },

    /**
     * Get integration folder contents
     */
    async getIntegrationContents() {
        return this.getContents('integration');
    },

    /**
     * Get file content (decoded from base64)
     */
    async getFileContent(path) {
        const content = await this.getRawContent(path);
        return content;
    },

    /**
     * Get skill registry
     */
    async getSkillRegistry() {
        return this.getRawContent('skills/SKILL_REGISTRY.md');
    },

    /**
     * Search for files matching pattern
     */
    async searchFiles(query) {
        try {
            const result = await this.request(
                `/search/code?q=${encodeURIComponent(query)}+repo:${this.owner}/${this.repo}`
            );
            return result.items || [];
        } catch (e) {
            console.error('Search failed:', e);
            return [];
        }
    },

    /**
     * Get contributors
     */
    async getContributors() {
        return this.request(`/repos/${this.owner}/${this.repo}/contributors`);
    },

    /**
     * Get branches
     */
    async getBranches() {
        return this.request(`/repos/${this.owner}/${this.repo}/branches`);
    },

    /**
     * Get rate limit status
     */
    getRateLimitStatus() {
        return {
            remaining: this.rateLimitRemaining,
            resetTime: this.rateLimitReset ? new Date(this.rateLimitReset * 1000) : null
        };
    },

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    },

    /**
     * Set cache timeout
     */
    setCacheTimeout(ms) {
        this.cacheTimeout = ms;
    }
};

// Real-time update manager
const RealtimeManager = {
    updateInterval: null,
    callbacks: new Map(),
    
    /**
     * Start real-time updates
     */
    start(intervalMs = 60000) {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
        
        this.updateInterval = setInterval(async () => {
            await this.refresh();
        }, intervalMs);
        
        console.log(`Real-time updates started (interval: ${intervalMs}ms)`);
    },
    
    /**
     * Stop real-time updates
     */
    stop() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
            this.updateInterval = null;
        }
        console.log('Real-time updates stopped');
    },
    
    /**
     * Register callback for updates
     */
    onUpdate(key, callback) {
        this.callbacks.set(key, callback);
    },
    
    /**
     * Remove callback
     */
    offUpdate(key) {
        this.callbacks.delete(key);
    },
    
    /**
     * Trigger refresh
     */
    async refresh() {
        GitHubAPI.clearCache();
        
        for (const [key, callback] of this.callbacks) {
            try {
                await callback();
            } catch (e) {
                console.error(`Update callback '${key}' failed:`, e);
            }
        }
    }
};

// Export for use in other modules
window.GitHubAPI = GitHubAPI;
window.RealtimeManager = RealtimeManager;
