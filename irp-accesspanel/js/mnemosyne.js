// Mnemosyne Ledger Browser Logic
// IRP Access Panel - Priority 1 Feature

let allConcepts = [];
let filteredConcepts = [];

// Load concepts on page load
document.addEventListener('DOMContentLoaded', async () => {
    await loadConcepts();
    setupEventListeners();
    renderConcepts();
    updateStats();
});

// Load data from JSON
async function loadConcepts() {
    try {
        const response = await fetch('data/mnemosyne.json');
        const data = await response.json();
        allConcepts = data.concepts || [];
        filteredConcepts = [...allConcepts];
    } catch (error) {
        console.error('Error loading Mnemosyne data:', error);
        allConcepts = [];
        filteredConcepts = [];
    }
}

// Setup event listeners for filters
function setupEventListeners() {
    document.getElementById('search-input').addEventListener('input', applyFilters);
    document.getElementById('tier-filter').addEventListener('change', applyFilters);
    document.getElementById('sort-select').addEventListener('change', applyFilters);
}

// Apply filters and sorting
function applyFilters() {
    const searchTerm = document.getElementById('search-input').value.toLowerCase();
    const tierFilter = document.getElementById('tier-filter').value;
    const sortBy = document.getElementById('sort-select').value;

    // Filter
    filteredConcepts = allConcepts.filter(concept => {
        const matchesSearch = !searchTerm ||
            concept.handle.toLowerCase().includes(searchTerm) ||
            concept.version.toLowerCase().includes(searchTerm) ||
            (concept.description && concept.description.toLowerCase().includes(searchTerm));

        const matchesTier = tierFilter === 'all' || concept.tier === tierFilter;

        return matchesSearch && matchesTier;
    });

    // Sort
    filteredConcepts.sort((a, b) => {
        switch(sortBy) {
            case 'handle':
                return a.handle.localeCompare(b.handle);
            case 'version':
                return compareVersions(b.version, a.version);
            case 'torsion':
                return b.torsion - a.torsion;
            case 'centrality':
                return b.centrality - a.centrality;
            case 'stability':
                return b.stability - a.stability;
            default:
                return 0;
        }
    });

    renderConcepts();
    updateStats();
}

// Compare semantic versions
function compareVersions(v1, v2) {
    const parts1 = v1.split(/[.-]/).map(p => parseInt(p) || 0);
    const parts2 = v2.split(/[.-]/).map(p => parseInt(p) || 0);

    for (let i = 0; i < Math.max(parts1.length, parts2.length); i++) {
        const p1 = parts1[i] || 0;
        const p2 = parts2[i] || 0;
        if (p1 !== p2) return p1 - p2;
    }
    return 0;
}

// Render concepts to the grid
function renderConcepts() {
    const container = document.getElementById('concepts-container');
    const noResults = document.getElementById('no-results');

    if (filteredConcepts.length === 0) {
        container.innerHTML = '';
        noResults.classList.remove('hidden');
        return;
    }

    noResults.classList.add('hidden');
    container.innerHTML = filteredConcepts.map(concept => createConceptCard(concept)).join('');
}

// Create HTML for a single concept card
function createConceptCard(concept) {
    const torsionClass = getTorsionClass(concept.torsion);
    const torsionText = getTorsionText(concept.torsion);
    const stabilityClass = getStabilityClass(concept.stability);
    const tierClass = `tier-${concept.tier.toLowerCase()}`;

    return `
        <div class="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition">
            <!-- Header with Tier Badge -->
            <div class="${tierClass} px-6 py-4 border-b border-gray-200">
                <div class="flex justify-between items-start">
                    <div class="flex-1">
                        <h3 class="text-2xl font-bold text-gray-800">${escapeHtml(concept.handle)}</h3>
                        <p class="text-gray-700 font-mono text-sm mt-1">
                            v${escapeHtml(concept.version)}${concept.torsion ? `-T${concept.torsion.toFixed(2)}` : ''}
                        </p>
                    </div>
                    <div class="text-right">
                        <span class="inline-block px-3 py-1 bg-white bg-opacity-70 rounded-full text-sm font-semibold">
                            ${concept.tier}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Content -->
            <div class="px-6 py-4">
                ${concept.description ? `
                    <p class="text-gray-600 mb-4">${escapeHtml(concept.description)}</p>
                ` : ''}

                <!-- Metrics Grid -->
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <!-- Torsion -->
                    <div class="bg-gray-50 rounded-lg p-3">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-gray-600">Torsion</span>
                            <i class="fas fa-gauge ${torsionClass}"></i>
                        </div>
                        <div class="text-2xl font-bold ${torsionClass}">
                            ${concept.torsion.toFixed(2)}
                        </div>
                        <div class="text-xs text-gray-500 mt-1">${torsionText}</div>
                    </div>

                    <!-- Centrality -->
                    <div class="bg-gray-50 rounded-lg p-3">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-sm text-gray-600">Centrality</span>
                            <i class="fas fa-bullseye text-blue-500"></i>
                        </div>
                        <div class="text-2xl font-bold text-blue-600">
                            ${concept.centrality.toFixed(2)}
                        </div>
                        <div class="text-xs text-gray-500 mt-1">Mandate Proximity</div>
                    </div>
                </div>

                <!-- Stability Bar -->
                <div class="mb-4">
                    <div class="flex items-center justify-between mb-2">
                        <span class="text-sm text-gray-600 font-medium">
                            <i class="fas fa-chart-line mr-2"></i>Stability
                        </span>
                        <span class="text-sm font-semibold">${(concept.stability * 100).toFixed(0)}%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                        <div class="${stabilityClass} h-full rounded-full transition-all duration-500"
                             style="width: ${concept.stability * 100}%"></div>
                    </div>
                    <div class="text-xs text-gray-500 mt-1">
                        ${concept.stability >= 0.95 ? '✓ Qualified for value acceptance' : 'Building stability...'}
                    </div>
                </div>

                <!-- Metadata -->
                ${concept.dependencies && concept.dependencies.length > 0 ? `
                    <div class="border-t pt-3 mt-3">
                        <div class="text-sm text-gray-600 mb-2">
                            <i class="fas fa-link mr-2"></i>Dependencies
                        </div>
                        <div class="flex flex-wrap gap-2">
                            ${concept.dependencies.map(dep => `
                                <span class="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-medium">
                                    ${escapeHtml(dep)}
                                </span>
                            `).join('')}
                        </div>
                    </div>
                ` : ''}

                ${concept.last_updated ? `
                    <div class="border-t pt-3 mt-3 text-xs text-gray-500">
                        <i class="fas fa-clock mr-2"></i>Last Updated: ${formatDate(concept.last_updated)}
                    </div>
                ` : ''}
            </div>
        </div>
    `;
}

// Get torsion CSS class
function getTorsionClass(torsion) {
    if (torsion >= 0.95) return 'torsion-halt';
    if (torsion >= 0.80) return 'torsion-suspend';
    if (torsion >= 0.50) return 'torsion-warning';
    if (torsion >= 0.20) return 'torsion-alert';
    return 'torsion-safe';
}

// Get torsion text description
function getTorsionText(torsion) {
    if (torsion >= 0.95) return 'Tier 4: HALT';
    if (torsion >= 0.80) return 'Tier 3: Suspend';
    if (torsion >= 0.50) return 'Tier 2: Warning';
    if (torsion >= 0.20) return 'Tier 1: Alert';
    return 'Tier 0: Monitor';
}

// Get stability CSS class
function getStabilityClass(stability) {
    if (stability >= 0.95) return 'stability-high';
    if (stability >= 0.70) return 'stability-medium';
    return 'stability-low';
}

// Update statistics
function updateStats() {
    const total = filteredConcepts.length;
    const hot = filteredConcepts.filter(c => c.tier === 'Hot').length;
    const avgTorsion = total > 0
        ? filteredConcepts.reduce((sum, c) => sum + c.torsion, 0) / total
        : 0;
    const stable = filteredConcepts.filter(c => c.stability >= 0.95).length;

    document.getElementById('stat-total').textContent = total;
    document.getElementById('stat-hot').textContent = hot;
    document.getElementById('stat-torsion').textContent = avgTorsion.toFixed(2);
    document.getElementById('stat-stable').textContent = stable;

    // Color code avg torsion
    const torsionEl = document.getElementById('stat-torsion');
    torsionEl.className = `text-3xl font-bold ${getTorsionClass(avgTorsion)}`;
}

// Utility: Escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Utility: Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}
