/* ==========================================================================
   SpecStream AI - Application Controller (Interactive Web UI)
   ========================================================================== */

let currentCatalog = null;
let activeItemIdxForTaxonomy = null;
let currentExportFormat = 'bmecat';
let currentExportContent = '';
let selectedLocalFile = null;
let configuredApiKey = sessionStorage.getItem('specstream_api_key') || '';

document.addEventListener('DOMContentLoaded', () => {
  // Load initial sample catalog
  loadSampleCatalog('industrial_fasteners');

  // Set API key input if stored
  const keyInput = document.getElementById('geminiApiKeyInput');
  if (keyInput && configuredApiKey) {
    keyInput.value = configuredApiKey;
  }

  // Explicit event listener binding for header buttons
  const apiKeyBtn = document.getElementById('apiKeySettingsBtn');
  if (apiKeyBtn) {
    apiKeyBtn.addEventListener('click', openApiKeyModal);
  }

  // Drag and drop dropzone listeners
  const dropzone = document.getElementById('dropzoneCard');
  if (dropzone) {
    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.classList.add('drag-over');
    });
    dropzone.addEventListener('dragleave', () => {
      dropzone.classList.remove('drag-over');
    });
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('drag-over');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        onFileSelected(e.dataTransfer.files[0]);
      }
    });
  }
});

// --- AI API Key Modal Handlers ---
function openApiKeyModal() {
  const modal = document.getElementById('apiKeyModal');
  if (modal) modal.classList.add('active');
}

function closeApiKeyModal() {
  const modal = document.getElementById('apiKeyModal');
  if (modal) modal.classList.remove('active');
}

function saveApiKey() {
  const keyInput = document.getElementById('geminiApiKeyInput');
  if (keyInput) {
    configuredApiKey = keyInput.value.trim();
    sessionStorage.setItem('specstream_api_key', configuredApiKey);
    alert("AI Model settings saved!");
  }
  closeApiKeyModal();
}

window.openApiKeyModal = openApiKeyModal;
window.closeApiKeyModal = closeApiKeyModal;
window.saveApiKey = saveApiKey;

// --- Sample Catalog Loader ---
async function loadSampleCatalog(sampleId) {
  resetFileSelection();
  try {
    const res = await fetch(`/api/sample/${sampleId}`);
    if (!res.ok) throw new Error("Failed to load sample catalog");
    const data = await res.json();
    currentCatalog = data;
    renderCatalogWorkbench();
  } catch (err) {
    console.error("Error loading sample catalog:", err);
    alert("Error loading sample catalog dataset.");
  }
}

// --- File Select & Upload Handlers ---
function handleFileSelect(event) {
  const files = event.target.files;
  if (files && files.length > 0) {
    onFileSelected(files[0]);
  }
}

function onFileSelected(file) {
  selectedLocalFile = file;

  // Hide default state, show selected file card
  document.getElementById('uploadDefaultState').style.display = 'none';
  const selectedState = document.getElementById('uploadSelectedState');
  selectedState.style.display = 'block';

  // Format file size
  const sizeKb = (file.size / 1024).toFixed(1);
  const ext = file.name.split('.').pop().toUpperCase();

  // Set file details in UI
  document.getElementById('selectedFileName').textContent = file.name;
  document.getElementById('selectedFileDetails').textContent = `Size: ${sizeKb} KB • ${ext} Document`;
  document.getElementById('selectedFileBadgeIcon').textContent = ext === 'CSV' ? '📊' : (ext === 'PDF' ? '📄' : '🖼️');

  // Automatically start transformation
  startSelectedFileTransformation();
}

function resetFileSelection() {
  selectedLocalFile = null;
  const fileInput = document.getElementById('fileInput');
  if (fileInput) fileInput.value = '';

  document.getElementById('uploadDefaultState').style.display = 'block';
  document.getElementById('uploadSelectedState').style.display = 'none';
  document.getElementById('extractionProgress').style.display = 'none';
}

async function startSelectedFileTransformation() {
  if (!selectedLocalFile) return;

  const transformBtn = document.getElementById('transformBtn');
  const progressDiv = document.getElementById('extractionProgress');
  const progressText = document.getElementById('progressStepText');
  const progressBar = document.getElementById('progressBarFill');
  const progressPercent = document.getElementById('progressPercent');

  transformBtn.disabled = true;
  transformBtn.innerHTML = `⚡ Ingesting Catalog...`;
  progressDiv.style.display = 'block';

  // Step 1: Parsing Layout
  progressText.textContent = configuredApiKey 
    ? "1. Gemini Multimodal LLM reading visual catalog layout & items..."
    : "1. AI layout-agnostic chunker segmenting product entities...";
  progressBar.style.width = "35%";
  progressPercent.textContent = "35%";

  const formData = new FormData();
  formData.append('file', selectedLocalFile);
  if (configuredApiKey) {
    formData.append('api_key', configuredApiKey);
  }

  try {
    // Step 2: Enforcing Pydantic Schema
    setTimeout(() => {
      progressText.textContent = "2. Enforcing Pydantic schema validation & quality rules...";
      progressBar.style.width = "70%";
      progressPercent.textContent = "70%";
    }, 400);

    const res = await fetch('/api/extract', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) throw new Error("Failed to parse uploaded document");

    // Step 3: Vector Embeddings
    progressText.textContent = "3. Vector embeddings eCl@ss 7.1 classification match...";
    progressBar.style.width = "95%";
    progressPercent.textContent = "95%";

    const data = await res.json();

    setTimeout(() => {
      currentCatalog = data;
      renderCatalogWorkbench();

      progressBar.style.width = "100%";
      progressPercent.textContent = "100%";
      progressText.textContent = "✓ AI Ingestion & transformation complete!";
      transformBtn.disabled = false;
      transformBtn.innerHTML = `⚡ Re-transform Catalog`;
    }, 300);

  } catch (err) {
    console.error("Error extracting document:", err);
    alert("Extraction error: Could not process file layout.");
    transformBtn.disabled = false;
    transformBtn.innerHTML = `⚡ Transform Catalog with AI`;
  }
}

// --- Render Main Workbench (Document + Extracted Table) ---
function renderCatalogWorkbench() {
  if (!currentCatalog) return;

  // Render Document Viewer
  const docBadge = document.getElementById('docTypeBadge');
  if (docBadge) {
    docBadge.textContent = (currentCatalog.file_type || 'DOCUMENT').toUpperCase();
  }

  const headerTitle = document.getElementById('docHeaderTitle');
  if (headerTitle) {
    headerTitle.textContent = currentCatalog.title || 'Extracted Supplier Catalog';
  }

  const bboxList = document.getElementById('docBboxList');
  if (bboxList) {
    bboxList.innerHTML = '';
    (currentCatalog.bounding_boxes || []).forEach(box => {
      const boxDiv = document.createElement('div');
      boxDiv.className = 'doc-bbox-overlay';
      boxDiv.innerHTML = `
        <span class="doc-bbox-tag">${box.label}</span>
        <div style="font-size: 0.8rem; font-weight: 600; color: #1e3a8a;">Region ${box.item_idx + 1}: Extracted Feature Box</div>
        <div style="font-size: 0.75rem; color: #64748b;">Visual OCR Position: [X:${box.x}%, Y:${box.y}%]</div>
      `;
      boxDiv.addEventListener('mouseenter', () => highlightTableRow(box.item_idx));
      boxDiv.addEventListener('mouseleave', () => unhighlightTableRow(box.item_idx));
      bboxList.appendChild(boxDiv);
    });
  }

  const rawText = document.getElementById('docRawTextPreview');
  if (rawText && currentCatalog.doc_preview) {
    rawText.textContent = currentCatalog.doc_preview.raw_text || '';
  }

  // Render Extracted Table Grid & Stats
  renderTableRows();
  updateSummaryStats();
}

// --- Render Table Grid Rows ---
function renderTableRows() {
  const tbody = document.getElementById('catalogTableBody');
  if (!tbody || !currentCatalog) return;

  tbody.innerHTML = '';

  currentCatalog.items.forEach((item, idx) => {
    const val = (currentCatalog.validations && currentCatalog.validations[idx]) 
      ? currentCatalog.validations[idx] 
      : { status: 'VALID', issues: [] };

    const tr = document.createElement('tr');
    tr.id = `table-row-${idx}`;

    let statusBadgeHtml = '';
    if (val.status === 'VALID') {
      statusBadgeHtml = `<span class="badge badge-valid">VALID</span>`;
    } else if (val.status === 'WARNING') {
      const toolTipMsg = val.issues.map(i => i.message).join(' | ');
      statusBadgeHtml = `<span class="badge badge-warning" title="${toolTipMsg}">WARNING</span>`;
    } else {
      const toolTipMsg = val.issues.map(i => i.message).join(' | ');
      statusBadgeHtml = `<span class="badge badge-error" title="${toolTipMsg}">ERROR</span>`;
    }

    tr.innerHTML = `
      <td>${statusBadgeHtml}</td>
      <td>
        <input class="cell-input" style="width: 110px; font-family: var(--font-mono);" value="${item.supplier_item_id || ''}" onchange="updateItemField(${idx}, 'supplier_item_id', this.value)">
      </td>
      <td>
        <input class="cell-input" style="width: 220px;" value="${escapeHtml(item.title || '')}" onchange="updateItemField(${idx}, 'title', this.value)">
      </td>
      <td>
        <input class="cell-input" type="number" step="0.01" style="width: 80px;" value="${item.price || 0}" onchange="updateItemField(${idx}, 'price', parseFloat(this.value))">
      </td>
      <td>
        <input class="cell-input" style="width: 60px; text-transform: uppercase;" value="${item.uom || 'C62'}" onchange="updateItemField(${idx}, 'uom', this.value)">
      </td>
      <td>
        <input class="cell-input" style="width: 110px;" value="${escapeHtml(item.mpn || '')}" onchange="updateItemField(${idx}, 'mpn', this.value)">
      </td>
      <td>
        <button class="eclass-tag" onclick="openTaxonomyModalFor(${idx})">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          ${item.eclass_code || '23-11-01-01'}
        </button>
      </td>
      <td>
        <button class="btn btn-outline" style="padding: 0.2rem 0.5rem; font-size: 0.75rem; color: #991b1b;" onclick="deleteItemRow(${idx})">Delete</button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}

function escapeHtml(text) {
  return String(text).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

// --- Live Item Field Update & Re-validation ---
async function updateItemField(idx, field, value) {
  if (!currentCatalog || !currentCatalog.items[idx]) return;
  currentCatalog.items[idx][field] = value;

  // Revalidate item against Pydantic backend rules
  try {
    const res = await fetch('/api/validate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(currentCatalog.items[idx])
    });
    if (res.ok) {
      const valResult = await res.json();
      currentCatalog.validations[idx] = valResult;
    }
  } catch (err) {
    console.error("Revalidation error:", err);
  }

  renderTableRows();
  updateSummaryStats();
}

function addNewItemRow() {
  if (!currentCatalog) return;
  const newItem = {
    supplier_item_id: `SKU-${Date.now().toString().slice(-4)}`,
    title: "New Catalog Item Component",
    description: "Detailed technical specification description for new item.",
    price: 15.00,
    currency: "EUR",
    uom: "C62",
    mpn: `MPN-${Date.now().toString().slice(-4)}`,
    manufacturer: "Standard Supplier",
    specs: {},
    keywords: ["component"],
    eclass_code: "23-11-01-01"
  };
  currentCatalog.items.push(newItem);
  currentCatalog.validations.push({ status: 'VALID', score: 100, issues: [] });
  renderTableRows();
  updateSummaryStats();
}

function deleteItemRow(idx) {
  if (!currentCatalog) return;
  currentCatalog.items.splice(idx, 1);
  currentCatalog.validations.splice(idx, 1);
  renderTableRows();
  updateSummaryStats();
}

// --- Summary Stats Update ---
function updateSummaryStats() {
  if (!currentCatalog) return;

  const total = currentCatalog.items.length;
  let validCount = 0;
  let warningCount = 0;
  let totalScoreSum = 0;

  currentCatalog.validations.forEach(val => {
    if (val.status === 'VALID') validCount++;
    else if (val.status === 'WARNING') warningCount++;
    totalScoreSum += (val.score !== undefined ? val.score : 80);
  });

  const avgScore = total > 0 ? Math.round(totalScoreSum / total) : 100;

  document.getElementById('statTotalItems').textContent = total;
  document.getElementById('statValidItems').textContent = validCount;
  document.getElementById('statWarningItems').textContent = warningCount;
  document.getElementById('statQualityScore').textContent = `${avgScore}%`;
}

function highlightTableRow(idx) {
  const row = document.getElementById(`table-row-${idx}`);
  if (row) row.style.backgroundColor = '#eff6ff';
}

function unhighlightTableRow(idx) {
  const row = document.getElementById(`table-row-${idx}`);
  if (row) row.style.backgroundColor = '';
}

// --- eCl@ss Vector Search Modal ---
async function openTaxonomyModalFor(idx) {
  activeItemIdxForTaxonomy = idx;
  const item = currentCatalog.items[idx];
  
  const modal = document.getElementById('taxonomyModal');
  const resultsContainer = document.getElementById('vectorMatchResultsList');
  if (!modal || !resultsContainer) return;

  resultsContainer.innerHTML = '<div style="padding: 1rem; text-align: center; color: #64748b;">Computing vector embeddings...</div>';
  modal.classList.add('active');

  try {
    const res = await fetch('/api/match-eclass', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: item.title,
        description: item.description,
        specs: item.specs || {},
        keywords: item.keywords || []
      })
    });
    if (!res.ok) throw new Error("Vector search error");
    const matches = await res.json();

    resultsContainer.innerHTML = '';
    matches.forEach(match => {
      const card = document.createElement('div');
      card.className = 'vector-match-card';
      card.innerHTML = `
        <div class="match-info">
          <h4>${match.code} - ${match.name}</h4>
          <p>${match.segment} &bull; ${match.description}</p>
          <div style="font-size: 0.75rem; color: #2563eb; margin-top: 0.25rem;">
            Matched terms: ${match.matched_terms.join(', ')}
          </div>
        </div>
        <div style="display: flex; align-items: center; gap: 1rem;">
          <span class="confidence-chip">${match.confidence}% match</span>
          <button class="btn btn-primary" style="padding: 0.35rem 0.75rem; font-size: 0.8rem;" onclick="selectEClassCode('${match.code}')">Select</button>
        </div>
      `;
      resultsContainer.appendChild(card);
    });

  } catch (err) {
    console.error("Error performing vector search:", err);
    resultsContainer.innerHTML = '<div style="color: #991b1b; padding: 1rem;">Error performing vector search.</div>';
  }
}

function selectEClassCode(code) {
  if (activeItemIdxForTaxonomy !== null && currentCatalog && currentCatalog.items[activeItemIdxForTaxonomy]) {
    currentCatalog.items[activeItemIdxForTaxonomy].eclass_code = code;
    updateItemField(activeItemIdxForTaxonomy, 'eclass_code', code);
  }
  closeTaxonomyModal();
}

function closeTaxonomyModal() {
  const modal = document.getElementById('taxonomyModal');
  if (modal) modal.classList.remove('active');
  activeItemIdxForTaxonomy = null;
}

// --- BMEcat XML & Multi-Format Export Modal ---
async function openExportModal() {
  if (!currentCatalog || !currentCatalog.items) return;
  const modal = document.getElementById('exportModal');
  if (modal) modal.classList.add('active');
  await fetchExportContent(currentExportFormat);
}

async function switchExportTab(format) {
  currentExportFormat = format;

  document.getElementById('tabBmecatBtn').className = format === 'bmecat' ? 'btn btn-primary' : 'btn btn-outline';
  document.getElementById('tabCxmlBtn').className = format === 'cxml' ? 'btn btn-primary' : 'btn btn-outline';
  document.getElementById('tabCsvBtn').className = format === 'csv' ? 'btn btn-primary' : 'btn btn-outline';

  await fetchExportContent(format);
}

async function fetchExportContent(format) {
  const codeBlock = document.getElementById('codeExportPreview');
  if (!codeBlock || !currentCatalog) return;

  codeBlock.textContent = 'Generating export stream...';

  try {
    const res = await fetch('/api/export', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        items: currentCatalog.items,
        format: format,
        config: {
          supplier_name: currentCatalog.supplier_name || 'Standard Supplier Inc.',
          catalog_id: currentCatalog.catalog_id || 'CAT-2026-001'
        }
      })
    });
    if (!res.ok) throw new Error("Export error");
    const data = await res.json();
    currentExportContent = data.content;
    codeBlock.textContent = currentExportContent;
  } catch (err) {
    console.error("Export error:", err);
    codeBlock.textContent = "Error generating export document.";
  }
}

function closeExportModal() {
  const modal = document.getElementById('exportModal');
  if (modal) modal.classList.remove('active');
}

function copyExportToClipboard() {
  if (!currentExportContent) return;
  navigator.clipboard.writeText(currentExportContent);
  alert("Export content copied to clipboard!");
}

function downloadExportFile() {
  if (!currentExportContent) return;
  const ext = currentExportFormat === 'csv' ? 'csv' : 'xml';
  const blob = new Blob([currentExportContent], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `catalog_export_${currentExportFormat}.${ext}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}
