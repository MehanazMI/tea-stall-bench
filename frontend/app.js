/**
 * Tea Stall Bench — Dashboard JavaScript
 * Handles pipeline execution and UI updates.
 */

const API_BASE = '/api/v1';

// ── DOM Elements ──────────────────────────────────────
const form = document.getElementById('pipeline-form');
const runBtn = document.getElementById('run-btn');
const btnText = runBtn.querySelector('.btn-text');
const btnLoading = runBtn.querySelector('.btn-loading');
const headerStatus = document.getElementById('header-status');
const errorBanner = document.getElementById('error-banner');
const errorMessages = document.getElementById('error-messages');
const outputPanel = document.getElementById('output-panel');

// Stage elements
const stages = {
    scout: {
        card: document.getElementById('stage-scout'),
        badge: document.getElementById('badge-scout'),
        content: document.getElementById('content-scout')
    },
    draft: {
        card: document.getElementById('stage-draft'),
        badge: document.getElementById('badge-draft'),
        content: document.getElementById('content-draft')
    },
    ink: {
        card: document.getElementById('stage-ink'),
        badge: document.getElementById('badge-ink'),
        content: document.getElementById('content-ink')
    }
};

// ── Form Submission ───────────────────────────────────
form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const topic = document.getElementById('topic').value.trim();
    if (!topic) return;

    // Reset UI
    resetUI();
    setRunning(true);

    // Simulate stage progression for visual effect
    animateStage('scout', 'active', 'Researching...');

    try {
        const response = await fetch(`${API_BASE}/pipeline`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                topic: topic,
                content_type: 'blog',
                style: document.getElementById('style').value,
                length: document.getElementById('length').value,
                channel: document.getElementById('channel').value
            })
        });

        if (!response.ok) {
            const err = await response.json();
            throw new Error(err.detail || `Server error: ${response.status}`);
        }

        const data = await response.json();
        renderResults(data);

    } catch (error) {
        showError(error.message);
        setAllStagesError();
    } finally {
        setRunning(false);
    }
});

// ── Render Pipeline Results ───────────────────────────
function renderResults(data) {
    // ── Stage 1: Scout ──
    if (data.research_data) {
        const hasError = data.errors?.some(e => e.startsWith('Research failed'));
        animateStage('scout', hasError ? 'error' : 'done', hasError ? 'Fallback Used' : 'Complete');

        const sourcesHtml = data.research_sources?.length
            ? `<p style="margin-top:0.5rem;color:var(--text-muted);font-size:0.75rem;">📎 ${data.research_sources.length} source(s) found</p>`
            : '';

        stages.scout.content.innerHTML = `
            <p>${truncate(data.research_data, 300)}</p>
            ${sourcesHtml}
        `;
    } else {
        animateStage('scout', 'error', 'Failed');
        stages.scout.content.innerHTML = '<p>No research data available.</p>';
    }

    // ── Stage 2: Draft ──
    if (data.outline) {
        const hasError = data.errors?.some(e => e.startsWith('Outline failed'));
        animateStage('draft', hasError ? 'error' : 'done', hasError ? 'Fallback Used' : 'Complete');

        let outlineHtml = '<ul class="outline-list">';
        (data.outline.sections || []).forEach(section => {
            outlineHtml += `<li>
                <span class="outline-heading">${escapeHtml(section.heading)}</span>
                <ul class="outline-points">
                    ${section.key_points.map(p => `<li>${escapeHtml(p)}</li>`).join('')}
                </ul>
            </li>`;
        });
        outlineHtml += '</ul>';
        stages.draft.content.innerHTML = outlineHtml;
    } else {
        animateStage('draft', 'error', 'Failed');
        stages.draft.content.innerHTML = '<p>No outline generated.</p>';
    }

    // ── Stage 3: Ink ──
    if (data.article_content) {
        animateStage('ink', 'done', 'Complete');
        stages.ink.content.innerHTML = `<p>${truncate(data.article_content, 250)}</p>`;
    } else {
        const hasError = data.errors?.some(e => e.startsWith('Writing failed'));
        animateStage('ink', hasError ? 'error' : 'done', hasError ? 'Failed' : 'No Content');
        stages.ink.content.innerHTML = '<p>Article generation failed.</p>';
    }

    // ── Errors ──
    if (data.errors?.length > 0) {
        showWarnings(data.errors);
    }

    // ── Output Panel ──
    if (data.article_content) {
        document.getElementById('article-title').textContent = data.article_title || data.topic;
        document.getElementById('article-content').textContent = data.article_content;
        document.getElementById('output-trace').textContent = `🏷️ ${data.trace_id}`;
        document.getElementById('output-words').textContent = `📝 ${data.word_count || 0} words`;

        // Calculate duration
        if (data.started_at && data.completed_at) {
            const duration = ((new Date(data.completed_at) - new Date(data.started_at)) / 1000).toFixed(1);
            document.getElementById('output-time').textContent = `⏱️ ${duration}s`;
        }

        outputPanel.style.display = 'block';
    }

    // ── Header Status ──
    setHeaderStatus('done', '✅ Completed');
}

// ── UI Helpers ────────────────────────────────────────

function resetUI() {
    // Reset stages
    Object.keys(stages).forEach(key => {
        animateStage(key, 'pending', 'Pending');
        const placeholders = { scout: 'Waiting for pipeline to start...', draft: 'Waiting for Scout...', ink: 'Waiting for Draft...' };
        stages[key].content.innerHTML = `<p class="stage-placeholder">${placeholders[key]}</p>`;
    });
    // Hide panels
    errorBanner.style.display = 'none';
    outputPanel.style.display = 'none';
    errorMessages.innerHTML = '';
}

function setRunning(isRunning) {
    runBtn.disabled = isRunning;
    btnText.style.display = isRunning ? 'none' : 'inline';
    btnLoading.style.display = isRunning ? 'inline' : 'none';
    if (isRunning) {
        setHeaderStatus('active', '🔄 Running Pipeline...');
    }
}

function animateStage(stage, status, label) {
    stages[stage].card.setAttribute('data-status', status);
    stages[stage].badge.textContent = label;
}

function setAllStagesError() {
    Object.keys(stages).forEach(key => {
        if (stages[key].card.getAttribute('data-status') === 'active' ||
            stages[key].card.getAttribute('data-status') === 'pending') {
            animateStage(key, 'error', 'Error');
        }
    });
}

function setHeaderStatus(type, text) {
    const dot = headerStatus.querySelector('.dot');
    dot.className = `dot dot-${type}`;
    headerStatus.querySelector('span:last-child').textContent = text;
}

function showError(message) {
    errorBanner.style.display = 'flex';
    errorMessages.innerHTML = `<p><strong>Error:</strong> ${escapeHtml(message)}</p>`;
    setHeaderStatus('error', '❌ Failed');
}

function showWarnings(errors) {
    errorBanner.style.display = 'flex';
    errorMessages.innerHTML = errors.map(e =>
        `<p>⚠️ ${escapeHtml(e)}</p>`
    ).join('');
}

function truncate(text, maxLen) {
    if (!text) return '';
    const clean = escapeHtml(text);
    return clean.length > maxLen ? clean.substring(0, maxLen) + '...' : clean;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
