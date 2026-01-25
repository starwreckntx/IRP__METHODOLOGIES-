// Multi-Model Capability Catalog Logic
// IRP Access Panel - Cross-Model Bootstrap Implementation

let allModels = [];
let filteredModels = [];

// Capability dimension labels
const CAPABILITY_LABELS = {
    D1_protocol_compliance: { name: 'Protocol Compliance', icon: 'fa-shield-alt', color: 'blue' },
    D2_state_management: { name: 'State Management', icon: 'fa-database', color: 'purple' },
    D3_tool_ecosystem: { name: 'Tool Ecosystem', icon: 'fa-tools', color: 'green' },
    D4_adversarial_resilience: { name: 'Adversarial Resilience', icon: 'fa-shield-virus', color: 'red' },
    D5_co_architecture: { name: 'Co-Architecture', icon: 'fa-sitemap', color: 'indigo' },
    D6_rtc_simulation: { name: 'RTC Simulation', icon: 'fa-users', color: 'yellow' },
    D7_crtp_protocol: { name: 'CRTP Protocol', icon: 'fa-exchange-alt', color: 'pink' },
    D8_friction_resistance: { name: 'Friction Resistance', icon: 'fa-bolt', color: 'orange' },
    D9_bootstrapping_speed: { name: 'Bootstrapping Speed', icon: 'fa-rocket', color: 'teal' },
    D10_emergent_innovation: { name: 'Emergent Innovation', icon: 'fa-lightbulb', color: 'amber' }
};

// Provider colors
const PROVIDER_COLORS = {
    'OpenAI': 'bg-green-500',
    'Google': 'bg-blue-500',
    'Anthropic': 'bg-orange-500',
    'xAI': 'bg-gray-700',
    'Moonshot AI': 'bg-purple-500',
    'Alibaba Cloud / Tongyi Lab': 'bg-red-500',
    '深度求索': 'bg-indigo-500'
};

// Load models on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadModels();
    setupEventListeners();
    renderModels();
    updateStats();
});

// Load data from JSON
async function loadModels() {
    try {
        const response = await fetch('data/models.json');
        const data = await response.json();
        allModels = data.models || [];
        filteredModels = [...allModels];
    } catch (error) {
        console.error('Error loading models data:', error);
        allModels = [];
        filteredModels = [];
    }
}

// Setup event listeners for filters
function setupEventListeners() {
    document.getElementById('search-input').addEventListener('input', applyFilters);
    document.getElementById('provider-filter').addEventListener('change', applyFilters);
    document.getElementById('verification-filter').addEventListener('change', applyFilters);
    document.getElementById('sort-select').addEventListener('change', applyFilters);
}

// Apply filters and sorting
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const providerFilter = document.getElementById('provider-filter').value;
    const verificationFilter = document.getElementById('verification-filter').value;
    const sortBy = document.getElementById('sort-select').value;

    // Filter
    filteredModels = allModels.filter(model => {
        const matchesSearch = !searchTerm ||
            model.id.toLowerCase().includes(searchTerm) ||
            model.provider.toLowerCase().includes(searchTerm) ||
            model.product.toLowerCase().includes(searchTerm) ||
            model.model_family.toLowerCase().includes(searchTerm) ||
            model.roles.primary.toLowerCase().includes(searchTerm);

        const matchesProvider = providerFilter === 'all' || model.provider === providerFilter;
        const matchesVerification = verificationFilter === 'all' ||
            model.verification.status === verificationFilter;

        return matchesSearch && matchesProvider && matchesVerification;
    });

    // Sort
    filteredModels.sort((a, b) => {
        switch(sortBy) {
            case 'provider':
                return a.provider.localeCompare(b.provider);
            case 'avg_capability':
                return getAvgCapability(b) - getAvgCapability(a);
            case 'co_architecture':
                return b.capabilities.D5_co_architecture - a.capabilities.D5_co_architecture;
            case 'tool_ecosystem':
                return b.capabilities.D3_tool_ecosystem - a.capabilities.D3_tool_ecosystem;
            case 'rtc_simulation':
                return b.capabilities.D6_rtc_simulation - a.capabilities.D6_rtc_simulation;
            default:
                return a.id.localeCompare(b.id);
        }
    });

    renderModels();
    updateStats();
}

// Calculate average capability score
function getAvgCapability(model) {
    const caps = Object.values(model.capabilities);
    return caps.reduce((sum, val) => sum + val, 0) / caps.length;
}

// Render models to the grid
function renderModels() {
    const container = document.getElementById('models-container');
    const noResults = document.getElementById('no-results');

    if (filteredModels.length === 0) {
        container.innerHTML = '';
        noResults.classList.remove('hidden');
        return;
    }

    noResults.classList.add('hidden');
    container.innerHTML = filteredModels.map(model => createModelCard(model)).join('');
}

// Create HTML for a single model card
function createModelCard(model) {
    const avgScore = getAvgCapability(model);
    const providerColor = PROVIDER_COLORS[model.provider] || 'bg-gray-500';
    const verificationBadge = model.verification.status === 'VERIFIED'
        ? '<span class="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium"><i class="fas fa-check-circle mr-1"></i>Verified</span>'
        : '<span class="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium"><i class="fas fa-clock mr-1"></i>Pending</span>';

    // Find top 3 capabilities
    const sortedCaps = Object.entries(model.capabilities)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 3);

    // Find weakest capability
    const weakest = Object.entries(model.capabilities)
        .sort(([,a], [,b]) => a - b)[0];

    return `
        <div class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 border border-gray-100">
            <!-- Header -->
            <div class="relative">
                <div class="${providerColor} h-2"></div>
                <div class="px-6 py-4 border-b border-gray-100">
                    <div class="flex justify-between items-start">
                        <div class="flex-1">
                            <div class="flex items-center gap-2 mb-1">
                                <span class="text-xs font-medium text-gray-500 uppercase tracking-wide">${escapeHtml(model.provider)}</span>
                                ${verificationBadge}
                            </div>
                            <h3 class="text-xl font-bold text-gray-800">${escapeHtml(model.product)} - ${escapeHtml(model.model_family)}</h3>
                            <p class="text-sm text-gray-500 font-mono">${escapeHtml(model.id)}</p>
                        </div>
                        <div class="text-right">
                            <div class="text-3xl font-bold ${getScoreColor(avgScore)}">${(avgScore * 100).toFixed(0)}</div>
                            <div class="text-xs text-gray-500">AVG SCORE</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Role & Tier -->
            <div class="px-6 py-3 bg-gray-50 border-b border-gray-100">
                <div class="text-sm font-medium text-gray-700">
                    <i class="fas fa-user-tag mr-2 text-blue-500"></i>${escapeHtml(model.roles.primary)}
                </div>
                <div class="flex flex-wrap gap-1 mt-2">
                    ${model.roles.tier_assignments.map(tier => `
                        <span class="px-2 py-0.5 bg-blue-100 text-blue-700 rounded text-xs">${escapeHtml(tier)}</span>
                    `).join('')}
                </div>
            </div>

            <!-- Capability Bars -->
            <div class="px-6 py-4">
                <div class="text-sm font-semibold text-gray-700 mb-3">
                    <i class="fas fa-chart-bar mr-2"></i>Capability Profile (10 Dimensions)
                </div>
                <div class="space-y-2">
                    ${Object.entries(model.capabilities).map(([key, value]) => {
                        const label = CAPABILITY_LABELS[key];
                        return `
                            <div class="group">
                                <div class="flex items-center justify-between text-xs mb-1">
                                    <span class="text-gray-600 truncate flex items-center">
                                        <i class="fas ${label.icon} mr-1 text-${label.color}-500 w-4"></i>
                                        <span class="hidden sm:inline">${label.name}</span>
                                        <span class="sm:hidden">${key.replace('D', '').split('_')[0]}</span>
                                    </span>
                                    <span class="font-mono font-medium ${getScoreColor(value)}">${(value * 100).toFixed(0)}%</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                                    <div class="h-full rounded-full transition-all duration-500 ${getBarColor(value)}"
                                         style="width: ${value * 100}%"></div>
                                </div>
                            </div>
                        `;
                    }).join('')}
                </div>
            </div>

            <!-- Insights -->
            <div class="px-6 py-4 bg-gradient-to-r from-gray-50 to-white border-t border-gray-100">
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <div class="text-xs text-gray-500 mb-1"><i class="fas fa-trophy mr-1 text-yellow-500"></i>Top Capabilities</div>
                        <div class="space-y-1">
                            ${sortedCaps.map(([key, val]) => `
                                <div class="text-xs">
                                    <span class="font-medium text-green-700">${(val * 100).toFixed(0)}%</span>
                                    <span class="text-gray-600">${CAPABILITY_LABELS[key].name}</span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                    <div>
                        <div class="text-xs text-gray-500 mb-1"><i class="fas fa-exclamation-triangle mr-1 text-orange-500"></i>Growth Area</div>
                        <div class="text-xs">
                            <span class="font-medium text-orange-700">${(weakest[1] * 100).toFixed(0)}%</span>
                            <span class="text-gray-600">${CAPABILITY_LABELS[weakest[0]].name}</span>
                        </div>
                        ${weakest[1] === 0 ? `
                            <div class="mt-1 text-xs text-red-600 font-medium">
                                <i class="fas fa-ban mr-1"></i>Requires partner
                            </div>
                        ` : ''}
                    </div>
                </div>
            </div>

            <!-- Metadata Footer -->
            <div class="px-6 py-3 bg-gray-100 border-t border-gray-200 text-xs text-gray-500">
                <div class="flex justify-between items-center">
                    <span><i class="fas fa-calendar mr-1"></i>Cutoff: ${escapeHtml(model.knowledge_cutoff)}</span>
                    <span><i class="fas fa-check-double mr-1"></i>${escapeHtml(model.verification.method.replace('_', ' '))}</span>
                </div>
            </div>
        </div>
    `;
}

// Get score text color
function getScoreColor(score) {
    if (score >= 0.9) return 'text-green-600';
    if (score >= 0.75) return 'text-blue-600';
    if (score >= 0.5) return 'text-yellow-600';
    return 'text-red-600';
}

// Get bar background color
function getBarColor(score) {
    if (score >= 0.9) return 'bg-green-500';
    if (score >= 0.75) return 'bg-blue-500';
    if (score >= 0.5) return 'bg-yellow-500';
    if (score > 0) return 'bg-orange-500';
    return 'bg-red-500';
}

// Update statistics
function updateStats() {
    const total = filteredModels.length;
    const verified = filteredModels.filter(m => m.verification.status === 'VERIFIED').length;
    const pending = filteredModels.filter(m => m.verification.status === 'PENDING_VERIFICATION').length;

    // Calculate overall average capability
    const overallAvg = total > 0
        ? filteredModels.reduce((sum, m) => sum + getAvgCapability(m), 0) / total
        : 0;

    // Find model with highest co-architecture score
    const topArchitect = filteredModels.reduce((best, m) =>
        (!best || m.capabilities.D5_co_architecture > best.capabilities.D5_co_architecture) ? m : best
    , null);

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-verified').textContent = verified;
    document.getElementById('stat-pending').textContent = pending;
    document.getElementById('stat-avg').textContent = (overallAvg * 100).toFixed(0) + '%';

    if (topArchitect) {
        document.getElementById('stat-top-architect').textContent = topArchitect.product;
    }
}

// Utility: Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
