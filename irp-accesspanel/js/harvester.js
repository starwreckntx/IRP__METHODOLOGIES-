// Harvester Logic: Identifies stale threads and manages the "Composting" process
// IRP Access Panel - Recursive Garbage Collection Protocol
// Architect: Gemini 2.0 Flash | Implementation: Claude Opus 4.5

document.addEventListener('DOMContentLoaded', () => {
    fetchData();
});

let conceptsData = [];

async function fetchData() {
    try {
        const response = await fetch('data/mnemosyne.json');
        const data = await response.json();
        conceptsData = data.concepts;
        analyzeDecay();
        updateStats();
    } catch (error) {
        console.error('Error loading ledger:', error);
        document.getElementById('compost-bin').innerHTML = `
            <div class="p-4 text-red-700 bg-red-100 rounded border border-red-300">
                <i class="fas fa-exclamation-triangle mr-2"></i>
                Error loading Mnemosyne Ledger. Check console for details.
            </div>`;
    }
}

function analyzeDecay() {
    const container = document.getElementById('compost-bin');
    const today = new Date();

    // Analyze all concepts for decay
    const analyzedConcepts = conceptsData.map(c => {
        const lastUpdate = new Date(c.last_updated || "2025-01-01");
        const diffTime = Math.abs(today - lastUpdate);
        const daysInactive = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        // DECAY ALGORITHM
        // High Torsion + Old = Festering (Needs Resolve)
        // Low Torsion + Old = Petrified (Needs Harvest)
        // Archive/Compost tier = Already processed
        let status = "Active";
        let decayScore = 0;
        let advice = "";
        let urgency = "low";

        // Skip already archived/composted items
        if (c.tier === "Compost" || c.tier === "Archive") {
            status = "Archived";
            advice = "Already in " + c.tier + " tier.";
            return { ...c, daysInactive, status, decayScore, advice, urgency };
        }

        if (daysInactive > 14) {
            if (c.torsion > 0.6) {
                status = "Festering";
                decayScore = daysInactive * 2 * c.torsion; // Urgency multiplier
                advice = "High drift + inactive. RESOLVE conflict or ABANDON.";
                urgency = "critical";
            } else if (c.torsion > 0.4) {
                status = "Decaying";
                decayScore = daysInactive * 1.5 * c.torsion;
                advice = "Moderate drift detected. Review and stabilize.";
                urgency = "high";
            } else if (daysInactive > 45) {
                status = "Petrified";
                decayScore = daysInactive * 0.8;
                advice = "Stable but dormant. HARVEST lessons and consider Archive.";
                urgency = "medium";
            } else if (daysInactive > 30) {
                status = "Stale";
                decayScore = daysInactive * 0.5;
                advice = "Review required. Update or document status.";
                urgency = "low";
            }
        }

        // Seeds tier gets special handling - expected to be dormant
        if (c.tier === "Seeds" && status === "Petrified") {
            status = "Dormant Seed";
            advice = "Seed awaiting germination. Consider activating or composting.";
            urgency = "low";
        }

        return { ...c, daysInactive, status, decayScore, advice, urgency };
    });

    // Filter to only stale items and sort by decay score
    const staleConcepts = analyzedConcepts
        .filter(c => c.status !== "Active" && c.status !== "Archived")
        .sort((a, b) => b.decayScore - a.decayScore);

    renderTable(staleConcepts, container);
}

function updateStats() {
    const today = new Date();

    let festering = 0, stale = 0, healthy = 0;

    conceptsData.forEach(c => {
        if (c.tier === "Compost" || c.tier === "Archive") return;

        const lastUpdate = new Date(c.last_updated || "2025-01-01");
        const daysInactive = Math.ceil(Math.abs(today - lastUpdate) / (1000 * 60 * 60 * 24));

        if (c.torsion > 0.6 && daysInactive > 14) festering++;
        else if (daysInactive > 30) stale++;
        else healthy++;
    });

    document.getElementById('stat-festering').textContent = festering;
    document.getElementById('stat-stale').textContent = stale;
    document.getElementById('stat-healthy').textContent = healthy;
}

function renderTable(items, container) {
    if (items.length === 0) {
        container.innerHTML = `
            <div class="p-6 text-green-700 bg-green-50 rounded-lg border border-green-200 text-center">
                <i class="fas fa-seedling text-4xl mb-3"></i>
                <h3 class="text-lg font-bold mb-2">Garden is Fresh</h3>
                <p>No stale threads detected. All concepts are actively maintained.</p>
            </div>`;
        return;
    }

    let html = `
        <div class="overflow-x-auto">
            <table class="min-w-full bg-white rounded-lg overflow-hidden shadow">
                <thead class="bg-gradient-to-r from-stone-700 to-stone-800 text-white">
                    <tr>
                        <th class="py-3 px-4 text-left">Handle</th>
                        <th class="py-3 px-4 text-left">Status</th>
                        <th class="py-3 px-4 text-left">Torsion</th>
                        <th class="py-3 px-4 text-left">Inactive</th>
                        <th class="py-3 px-4 text-left">Advice</th>
                        <th class="py-3 px-4 text-center">Action</th>
                    </tr>
                </thead>
                <tbody>`;

    items.forEach(item => {
        const statusColors = {
            "Festering": "bg-red-100 text-red-800 border-red-300",
            "Decaying": "bg-orange-100 text-orange-800 border-orange-300",
            "Petrified": "bg-gray-200 text-gray-800 border-gray-300",
            "Stale": "bg-yellow-100 text-yellow-800 border-yellow-300",
            "Dormant Seed": "bg-purple-100 text-purple-800 border-purple-300"
        };

        const torsionColor = item.torsion > 0.6 ? "text-red-600" :
                            item.torsion > 0.4 ? "text-orange-600" :
                            item.torsion > 0.2 ? "text-yellow-600" : "text-green-600";

        const rowClass = item.urgency === "critical" ? "bg-red-50" :
                        item.urgency === "high" ? "bg-orange-50" : "";

        html += `
            <tr class="border-b hover:bg-gray-50 ${rowClass}">
                <td class="py-3 px-4">
                    <span class="font-bold">${escapeHtml(item.handle)}</span>
                    <span class="text-xs text-gray-500 ml-1">v${item.version}</span>
                    <div class="text-xs text-gray-400">${item.tier}</div>
                </td>
                <td class="py-3 px-4">
                    <span class="px-2 py-1 rounded text-xs font-bold border ${statusColors[item.status] || 'bg-gray-100'}">${item.status}</span>
                </td>
                <td class="py-3 px-4">
                    <span class="font-mono font-bold ${torsionColor}">${(item.torsion * 100).toFixed(0)}%</span>
                </td>
                <td class="py-3 px-4">
                    <span class="font-mono">${item.daysInactive}</span>
                    <span class="text-gray-500 text-sm">days</span>
                </td>
                <td class="py-3 px-4 text-sm text-gray-600 italic max-w-xs">${item.advice}</td>
                <td class="py-3 px-4 text-center">
                    <button onclick="openHarvestModal('${escapeHtml(item.handle)}')"
                            class="bg-emerald-600 text-white px-3 py-1.5 rounded text-sm hover:bg-emerald-700 transition">
                        <i class="fas fa-leaf mr-1"></i>Harvest
                    </button>
                </td>
            </tr>`;
    });

    html += `</tbody></table></div>`;
    container.innerHTML = html;
}

// Modal Logic
window.openHarvestModal = (handle) => {
    const modal = document.getElementById('harvest-modal');
    const title = document.getElementById('modal-title');
    const hiddenHandle = document.getElementById('target-handle');
    const conceptInfo = document.getElementById('concept-info');

    const concept = conceptsData.find(c => c.handle === handle);

    title.innerText = `Harvesting: ${handle}`;
    hiddenHandle.value = handle;

    if (concept) {
        conceptInfo.innerHTML = `
            <div class="bg-gray-50 rounded p-3 mb-4 text-sm">
                <div class="grid grid-cols-2 gap-2">
                    <div><strong>Version:</strong> ${concept.version}</div>
                    <div><strong>Tier:</strong> ${concept.tier}</div>
                    <div><strong>Torsion:</strong> ${(concept.torsion * 100).toFixed(0)}%</div>
                    <div><strong>Stability:</strong> ${(concept.stability * 100).toFixed(0)}%</div>
                </div>
                <div class="mt-2 text-gray-600">${concept.description}</div>
            </div>`;
    }

    // Reset form
    document.getElementById('lesson-input').value = '';
    document.getElementById('action-select').value = 'Compost';
    document.getElementById('step-2').classList.add('hidden');

    modal.classList.remove('hidden');
}

window.closeModal = () => {
    document.getElementById('harvest-modal').classList.add('hidden');
}

window.generateArtifact = () => {
    const handle = document.getElementById('target-handle').value;
    const lessonText = document.getElementById('lesson-input').value.trim();
    const action = document.getElementById('action-select').value;

    if (!lessonText) {
        alert('Please document the lesson learned before harvesting.');
        return;
    }

    const concept = conceptsData.find(c => c.handle === handle);

    // Create the update instruction
    const updateInstruction = {
        "action": "UPDATE_CONCEPT",
        "target": handle,
        "changes": {
            "tier": action,
            "last_updated": new Date().toISOString().split('T')[0],
            "lessons": [
                ...(concept.lessons || []),
                {
                    "date": new Date().toISOString().split('T')[0],
                    "harvested_by": "The_Harvester",
                    "previous_tier": concept.tier,
                    "content": lessonText
                }
            ]
        },
        "chronicle_note": `Harvested via Garbage Collection Protocol. Moved from ${concept.tier} to ${action}.`
    };

    const outputArea = document.getElementById('json-output');
    outputArea.value = JSON.stringify(updateInstruction, null, 2);

    document.getElementById('step-2').classList.remove('hidden');
}

window.copyToClipboard = () => {
    const outputArea = document.getElementById('json-output');
    navigator.clipboard.writeText(outputArea.value).then(() => {
        const btn = event.target.closest('button');
        const originalText = btn.innerHTML;
        btn.innerHTML = '<i class="fas fa-check mr-2"></i>Copied!';
        btn.classList.remove('bg-gray-700');
        btn.classList.add('bg-green-600');
        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.classList.remove('bg-green-600');
            btn.classList.add('bg-gray-700');
        }, 2000);
    });
}

// Utility: Escape HTML
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
