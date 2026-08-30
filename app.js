const money = new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' });

const fallbackAssets = [
  { id: 'GROUNDS', name: 'Facility Grounds', group: 'Facility' },
  ...Array.from({ length: 75 }, (_, i) => ({ id: `IN-D${String(i + 1).padStart(2, '0')}`, name: `Dock Door ${i + 1}`, group: 'Inbound Dock Doors' })),
  ...Array.from({ length: 75 }, (_, i) => ({ id: `OUT-D${String(i + 101).padStart(3, '0')}`, name: `Dock Door ${i + 101}`, group: 'Outbound Dock Doors' })),
  ...Array.from({ length: 5 }, (_, i) => ({ id: `EPJ${String(i + 1).padStart(2, '0')}`, name: `EPJ${String(i + 1).padStart(2, '0')}`, group: 'PIT - Electric Pallet Jacks' })),
  { id: 'SD26', name: 'SD26', group: 'PIT - Forklifts & Reach Trucks' },
  { id: 'REACH', name: 'REACH', group: 'PIT - Forklifts & Reach Trucks' },
  ...Array.from({ length: 20 }, (_, i) => ({ id: `OP${String(i + 1).padStart(2, '0')}`, name: `OP${String(i + 1).padStart(2, '0')}`, group: 'PIT - Order Pickers' })),
  { id: 'REC-BAL-01', name: 'Cram-A-Lot Plastic Baler', group: 'Recycling Department' },
  { id: 'UTIL-COMP-01', name: 'Ingersoll Rand RSA11-22 Air Compressor', group: 'Facility Utilities' },
  { id: 'REC-AUG-01', name: 'Komar EM-15W Auger-Pak Trash Auger', group: 'Recycling Department' },
  { id: 'REC-GMX-01', name: 'GreenMax M-C300 Styrofoam Extruder', group: 'Recycling Department' },
  { id: 'REC-CON-01', name: 'Harris Above-Ground Conveyor', group: 'Recycling Department' },
  { id: 'REC-BAL-02', name: 'Harris 29N Series Cardboard Baler', group: 'Recycling Department' }
];

const fallbackManualParts = [
  { name: 'Crusher blade', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Crusher bearing UCF212', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Spherical roller bearing #22319', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Tapered roller bearing #32319', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: '16A drive chain', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Heater bands', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Hydraulic hose and fittings', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Main cylinder seal kit', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Door cylinder seal kit', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Adjustable shear blade', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Photocell', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Controller component', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Crusher motor', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Crusher gearbox', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Driving crusher', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Passive crusher', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Connection flange', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Inspection window safety switch', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Crusher bin', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Control box', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Transportation fan', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Wind pipe', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Silo', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Silo bracket', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Extruder motor M1', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Extruder motor M2', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Reducer 1', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Reducer 2', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Extruder screw', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Machine barrel', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Machine head flange', asset: 'GreenMax M-C300', source: 'M-C300 Instruction Manual' },
  { name: 'Oil fill port', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Hydraulic reservoir', asset: 'Cram-A-Lot HE-60', source: 'HE Series Specifications' },
  { name: 'Hydraulic pump', asset: 'Cram-A-Lot HE-60', source: 'HE Series Specifications' },
  { name: 'Programmable controller', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Automatic bale ejection system', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Full-bale warning indicator', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Advance warning indicator', asset: 'Cram-A-Lot HE-60', source: 'HE Series Brochure' },
  { name: 'Intake air filter', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Inlet valve', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Electric motor', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Compressor air end', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Belt drive', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Oil fine separator element', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Oil filter', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Oil cooler', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Air cooler', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Oil temperature regulator', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Cooling fan', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Cooling air inlet filter mat', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Pressure relief valve', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Minimum pressure check valve', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Oil level sight glass', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Final compression temperature sensor', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'System pressure sensor', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Emergency stop button', asset: 'Ingersoll Rand RSA11-22 Air Compressor', source: 'RSA11-22 Product Information' },
  { name: 'Solid-lube bearing support system', asset: 'Komar EM-15W Auger-Pak Trash Auger', source: 'Komar EM-15W manufacturer data' },
  { name: 'Chain and bearing lubrication system', asset: 'Komar EM-15W Auger-Pak Trash Auger', source: 'Komar EM-15W manufacturer data' }
];

function readStorage(key, fallback) {
  try {
    const stored = JSON.parse(localStorage.getItem(key));
    return Array.isArray(stored) ? stored : fallback;
  } catch {
    return fallback;
  }
}

function writeStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

async function fetchJson(url, options = {}) {
  const response = await fetch(url, {
    headers: { Accept: 'application/json', ...(options.headers || {}) },
    ...options
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.error || `Request failed: ${response.status}`);
  }

  return response.json();
}

async function getSession() {
  try {
    const data = await fetchJson('/api/session');
    return data;
  } catch {
    return { authenticated: false };
  }
}

function addSessionControls() {
  const header = document.querySelector('.brand-header');
  if (!header || document.getElementById('session-controls')) return;

  const controls = document.createElement('div');
  controls.id = 'session-controls';
  controls.innerHTML = `
    <span id="user-badge" class="user-badge">Signed in</span>
    <button type="button" id="logout-button" class="secondary-action">Logout</button>
  `;
  header.appendChild(controls);

  document.getElementById('logout-button').addEventListener('click', async () => {
    try {
      await fetchJson('/api/logout', { method: 'POST' });
    } catch {
      // no-op
    }
    window.location.href = '/login.html';
  });
}

async function requireAuth() {
  const page = document.body.dataset.page;
  if (page === 'login') {
    const session = await getSession();
    if (session.authenticated) {
      window.location.href = '/index.html';
    }
    return false;
  }

  const session = await getSession();
  if (!session.authenticated) {
    window.location.href = '/login.html';
    return false;
  }

  addSessionControls();
  const badge = document.getElementById('user-badge');
  if (badge) {
    badge.textContent = `${session.user.displayName || session.user.username} · ${session.user.role}`;
  }
  return true;
}

function bindLoginForms() {
  const loginForm = document.getElementById('login-form');
  const signupForm = document.getElementById('signup-form');
  const message = document.getElementById('auth-message');

  if (loginForm) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = document.getElementById('login-username').value.trim();
      const password = document.getElementById('login-password').value;

      try {
        await fetchJson('/api/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        window.location.href = '/index.html';
      } catch (error) {
        if (message) message.textContent = error.message || 'Login failed.';
      }
    });
  }

  if (signupForm) {
    signupForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      const username = document.getElementById('signup-username').value.trim();
      const displayName = document.getElementById('signup-display-name').value.trim();
      const password = document.getElementById('signup-password').value;

      try {
        await fetchJson('/api/signup', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password, displayName })
        });
        window.location.href = '/index.html';
      } catch (error) {
        if (message) message.textContent = error.message || 'Account creation failed.';
      }
    });
  }
}

function getAssetById(assetId) {
  return fallbackAssets.find((asset) => asset.id === assetId);
}

async function loadAssets() {
  try {
    const data = await fetchJson('/api/assets');
    return data.length ? data : fallbackAssets;
  } catch {
    return fallbackAssets;
  }
}

async function loadDashboard() {
  try {
    const data = await fetchJson('/api/dashboard');
    return data;
  } catch {
    const inventory = readStorage('fs-inventory', []);
    const spend = readStorage('fs-spending', []);
    const repairs = readStorage('fs-repairs', []);
    return {
      assetCount: fallbackAssets.length,
      inventoryValue: inventory.reduce((total, item) => total + (Number(item.quantity || 0) * Number(item.cost || 0)), 0),
      spendTotal: spend.reduce((total, item) => total + Number(item.amount || 0), 0),
      lowStockCount: inventory.filter((item) => Number(item.quantity || 0) <= Number(item.reorder || 0)).length,
      repairCount: repairs.filter((repair) => repair.status === 'Open').length
    };
  }
}

async function loadInventory(search = '') {
  try {
    const query = search ? `?q=${encodeURIComponent(search)}` : '';
    const data = await fetchJson(`/api/inventory${query}`);
    return Array.isArray(data) ? data : [];
  } catch {
    const items = readStorage('fs-inventory', []);
    const lowered = search.trim().toLowerCase();
    return lowered
      ? items.filter((item) => [item.partNumber, item.manufacturerPartNumber, item.name, item.asset, item.source].some((value) => String(value || '').toLowerCase().includes(lowered)))
      : [];
  }
}

async function loadRepairs(assetId) {
  try {
    const data = await fetchJson(`/api/repairs?assetId=${encodeURIComponent(assetId)}`);
    return Array.isArray(data) ? data : [];
  } catch {
    const repairs = readStorage('fs-repairs', []);
    return repairs.filter((repair) => repair.assetId === assetId);
  }
}

async function loadManualParts() {
  try {
    const data = await fetchJson('/api/manual-parts');
    return Array.isArray(data) ? data : fallbackManualParts;
  } catch {
    return fallbackManualParts;
  }
}

function buildAssetGroups(assets) {
  const grouped = assets.reduce((all, asset) => {
    const key = asset.group || 'Other';
    if (!all[key]) all[key] = [];
    all[key].push(asset);
    return all;
  }, {});

  const chips = (list) => list.map((asset) => `<a class="asset-chip" href="asset.html?id=${asset.id}">${asset.name}</a>`).join('');
  const pitAssets = Object.entries(grouped)
    .filter(([group]) => group.startsWith('PIT -'))
    .flatMap(([, list]) => list);

  const dropdown = (label, list) => `
    <details class="recycling-menu">
      <summary><span>${label}</span><small>${list.length} assets</small></summary>
      <div class="recycling-menu-content">${chips(list)}</div>
    </details>
  `;

  const sections = Object.entries(grouped)
    .filter(([group]) => !group.startsWith('PIT -'))
    .map(([group, list]) => {
      if (group === 'Recycling Department') return dropdown('Recycling', list);
      if (group === 'Inbound Dock Doors') return dropdown('Inbound Dock Doors', list);
      if (group === 'Outbound Dock Doors') return dropdown('Outbound Dock Doors', list);
      return `<section class="asset-group"><h3>${group}</h3><div>${chips(list)}</div></section>`;
    })
    .join('');

  return `${sections}${dropdown('PIT Equipment', pitAssets)}`;
}

async function showAssets() {
  const container = document.getElementById('asset-groups');
  if (!container) return;
  const assets = await loadAssets();
  container.innerHTML = buildAssetGroups(assets);
}

async function showAsset() {
  const assetId = new URLSearchParams(window.location.search).get('id');
  const assets = await loadAssets();
  const asset = assets.find((entry) => entry.id === assetId) || assets[0];

  if (!asset) return;

  const detail = document.getElementById('asset-detail');
  if (detail) {
    detail.innerHTML = `
      <div class="asset-record">
        <div class="asset-record-copy">
          <p class="eyebrow">Individual asset</p>
          <h1>${asset.name}</h1>
          <p><strong>Asset ID:</strong> ${asset.id} &nbsp; <strong>Area:</strong> ${asset.group} &nbsp; <strong>Status:</strong> Operational</p>
        </div>
        <span class="status-pill">Operational</span>
      </div>
    `;
  }

  const repairs = await loadRepairs(asset.id);
  const list = document.getElementById('repair-history');
  if (list) {
    list.innerHTML = repairs.length
      ? repairs.map((repair) => `
          <article class="history-item">
            <div>
              <strong>${repair.description}</strong>
              <p>${repair.status} · ${repair.date || repair.createdAt || '—'}</p>
            </div>
            <div class="expense">
              <strong>${money.format(Number(repair.cost || 0))}</strong>
            </div>
          </article>
        `).join('')
      : '<p class="empty-state">No repairs recorded for this asset.</p>';
  }

  const form = document.getElementById('repair-form');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const description = document.getElementById('repair-description').value.trim();
    const cost = Number(document.getElementById('repair-cost').value || 0);
    const status = document.getElementById('repair-status').value;

    if (!description) {
      document.getElementById('repair-note').textContent = 'Please add a repair description.';
      return;
    }

    try {
      await fetchJson('/api/repairs', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ assetId: asset.id, description, cost, status })
      });

      form.reset();
      document.getElementById('repair-note').textContent = `Repair saved for ${asset.name}.`;
      const refreshed = await loadRepairs(asset.id);
      list.innerHTML = refreshed.length
        ? refreshed.map((repair) => `
            <article class="history-item">
              <div>
                <strong>${repair.description}</strong>
                <p>${repair.status} · ${repair.date || repair.createdAt || '—'}</p>
              </div>
              <div class="expense">
                <strong>${money.format(Number(repair.cost || 0))}</strong>
              </div>
            </article>
          `).join('')
        : '<p class="empty-state">No repairs recorded for this asset.</p>';
    } catch {
      const repairsList = readStorage('fs-repairs', []);
      repairsList.unshift({
        assetId: asset.id,
        description,
        cost,
        status,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
      });
      writeStorage('fs-repairs', repairsList);
      form.reset();
      document.getElementById('repair-note').textContent = `Repair saved for ${asset.name}.`;
      const refreshed = repairsList.filter((repair) => repair.assetId === asset.id);
      list.innerHTML = refreshed.length
        ? refreshed.map((repair) => `
            <article class="history-item">
              <div>
                <strong>${repair.description}</strong>
                <p>${repair.status} · ${repair.date}</p>
              </div>
              <div class="expense">
                <strong>${money.format(Number(repair.cost || 0))}</strong>
              </div>
            </article>
          `).join('')
        : '<p class="empty-state">No repairs recorded for this asset.</p>';
    }
  });
}

async function showInventory() {
  const input = document.getElementById('inventory-search');
  const results = document.getElementById('inventory-results');
  const table = document.getElementById('inventory-table');
  const empty = document.getElementById('inventory-empty');
  const hint = document.getElementById('inventory-search-hint');

  if (!input || !results || !table || !empty || !hint) return;

  const render = async () => {
    const query = input.value.trim();
    const items = await loadInventory(query);

    table.replaceChildren();
    items.forEach((item) => {
      const row = document.createElement('tr');
      if (Number(item.quantity || 0) <= Number(item.reorder || 0)) row.classList.add('low-stock');

      const values = [
        item.partNumber || '—',
        item.name || 'Unnamed part',
        item.manufacturerPartNumber || '—',
        item.asset || 'General maintenance',
        Number(item.quantity || 0),
        money.format(Number(item.cost || 0))
      ];

      values.forEach((value) => {
        const cell = document.createElement('td');
        cell.textContent = value;
        row.appendChild(cell);
      });

      table.appendChild(row);
    });

    const hasResults = !!query && items.length > 0;
    results.hidden = !query || !hasResults;
    empty.hidden = !query || hasResults;
    hint.textContent = query
      ? (hasResults ? `${items.length} matching part${items.length === 1 ? '' : 's'}.` : 'No matching parts found.')
      : 'Parts remain hidden until you search.';
  };

  input.addEventListener('input', render);
  render();
}

async function showDashboard() {
  const stats = await loadDashboard();
  const elements = {
    assetCount: document.getElementById('asset-count'),
    inventoryValue: document.getElementById('inventory-value'),
    spendTotal: document.getElementById('spend-total'),
    lowStockCount: document.getElementById('low-stock-count'),
    repairCount: document.getElementById('repair-count')
  };

  if (elements.assetCount) elements.assetCount.textContent = stats.assetCount || fallbackAssets.length;
  if (elements.inventoryValue) elements.inventoryValue.textContent = money.format(Number(stats.inventoryValue || 0));
  if (elements.spendTotal) elements.spendTotal.textContent = money.format(Number(stats.spendTotal || 0));
  if (elements.lowStockCount) elements.lowStockCount.textContent = stats.lowStockCount || 0;
  if (elements.repairCount) elements.repairCount.textContent = stats.repairCount || 0;
}

async function showManualParts() {
  const container = document.getElementById('manual-parts');
  if (!container) return;
  const parts = await loadManualParts();
  container.innerHTML = parts.map((part) => `
    <article>
      <strong>${part.name}</strong>
      <span>${part.asset}</span>
      <small>${part.source}</small>
    </article>
  `).join('');
}

function initNavigationStates() {
  const nav = document.querySelector('.primary-nav');
  if (!nav) return;

  if (!nav.querySelector('a[href="documents.html"]')) {
    nav.insertAdjacentHTML('beforeend', '<a href="documents.html">Documents</a>');
  }

  if (!nav.querySelector('a[href="safety.html"]')) {
    nav.insertAdjacentHTML('beforeend', '<a href="safety.html">Safety</a>');
  }

  const pageMap = {
    documents: 'documents.html',
    safety: 'safety.html'
  };

  const page = document.body.dataset.page;
  const activeKey = pageMap[page];
  if (activeKey) {
    const activeLink = nav.querySelector(`a[href="${activeKey}"]`);
    if (activeLink) activeLink.classList.add('active');
  }
}

document.addEventListener('DOMContentLoaded', async () => {
  const page = document.body.dataset.page;
  initNavigationStates();

  if (page === 'login') {
    bindLoginForms();
    const session = await getSession();
    if (session.authenticated) {
      window.location.href = '/index.html';
    }
    return;
  }

  const authenticated = await requireAuth();
  if (!authenticated) return;

  if (page === 'dashboard') {
    showDashboard();
  }

  if (page === 'assets') {
    showAssets();
  }

  if (page === 'asset') {
    showAsset();
  }

  if (page === 'inventory') {
    showInventory();
  }

  if (page === 'documents') {
    showManualParts();
  }
});
