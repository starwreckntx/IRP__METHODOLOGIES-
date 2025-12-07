/**
 * IRP Dashboard - GitHub API Integration
 * Provides real-time data fetching from the IRP repository
 */

const GITHUB_API = {
    baseUrl: 'https://api.github.com',
    owner: 'starwreckntx',
    repo: 'IRP__METHODOLOGIES-',
    
    // Cache for API responses
    cache: new Map(),
    cacheTimeout: 5 * 60 * 1000, // 5 minutes

    /**
     * Fetch with caching
     */
    async fetch(endpoint, options = {}) {
        const cacheKey = endpoint;
        const cached = this.cache.get(cacheKey);
        
        if (cached && Date.now() - cached.timestamp < this.cacheTimeout) {
            return cached.data;
        }

        const url = `${this.baseUrl}${endpoint}`;
        const response = await fetch(url, {
            ...options,
            headers: {
                'Accept': 'application/vnd.github.v3+json',
                ...options.headers
            }
        });

        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status}`);
        }

        const data = await response.json();
        this.cache.set(cacheKey, { data, timestamp: Date.now() });
        return data;
    },

    /**
     * Get repository info
     */
    async getRepoInfo() {
        return this.fetch(`/repos/${this.owner}/${this.repo}`);
    },

    /**
     * Get directory contents
     */
    async getContents(path = '') {
        return this.fetch(`/repos/${this.owner}/${this.repo}/contents/${path}`);
    },

    /**
     * Get file content (decoded)
     */
    async getFileContent(path) {
        const file = await this.fetch(`/repos/${this.owner}/${this.repo}/contents/${path}`);
        if (file.encoding === 'base64') {
            return atob(file.content);
        }
        return file.content;
    },

    /**
     * Get recent commits
     */
    async getCommits(perPage = 10) {
        return this.fetch(`/repos/${this.owner}/${this.repo}/commits?per_page=${perPage}`);
    },

    /**
     * Get skills manifest
     */
    async getSkillsManifest() {
        try {
            const content = await this.getFileContent('skills_manifest.json');
            return JSON.parse(content);
        } catch (e) {
            console.error('Failed to load skills manifest:', e);
            return null;
        }
    },

    /**
     * Get skill registry
     */
    async getSkillRegistry() {
        try {
            return await this.getFileContent('skills/SKILL_REGISTRY.md');
        } catch (e) {
            console.error('Failed to load skill registry:', e);
            return null;
        }
    },

    /**
     * Get ledger state
     */
    async getLedgerState() {
        try {
            const content = await this.getFileContent('skills/cross-model/mnemosyne-ledger/state/ledger-state-live.json');
            return JSON.parse(content);
        } catch (e) {
            console.error('Failed to load ledger state:', e);
            return null;
        }
    },

    /**
     * Get skill file content
     */
    async getSkillContent(skillPath) {
        try {
            return await this.getFileContent(`skills/${skillPath}/SKILL.md`);
        } catch (e) {
            console.error('Failed to load skill:', e);
            return null;
        }
    },

    /**
     * Get integration folder structure
     */
    async getIntegrationContents() {
        try {
            return await this.getContents('integration');
        } catch (e) {
            console.error('Failed to load integration folder:', e);
            return [];
        }
    },

    /**
     * Clear cache
     */
    clearCache() {
        this.cache.clear();
    }
};

// Export for use in other modules
window.GitHubAPI = GITHUB_API;
