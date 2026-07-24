const searchForm = document.getElementById('searchForm');
const searchInput = document.getElementById('searchInput');
const searchButton = document.getElementById('searchButton');
const voiceButton = document.getElementById('voiceButton');
const resultsGrid = document.getElementById('resultsGrid');
const loadingState = document.getElementById('loadingState');
const shellResults = document.getElementById('shellResults');
const emptyState = document.getElementById('emptyState');
const historyList = document.getElementById('historyList');
const recentList = document.getElementById('recentList');
const filterChips = Array.from(document.querySelectorAll('.filter-chip'));
const sortSelect = document.getElementById('sortSelect');
const pagination = document.getElementById('pagination');
const statsPanel = document.getElementById('statsPanel');
const insightText = document.getElementById('insightText');
const sidebar = document.getElementById('sidebar');
const overlay = document.getElementById('overlay');
const menuButton = document.getElementById('menuButton');
const themeToggle = document.getElementById('themeToggle');
const searchStatus = document.getElementById('searchStatus');
const topbarLinks = Array.from(document.querySelectorAll('.topbar-link'));
const sidebarLinks = Array.from(document.querySelectorAll('.sidebar-link'));

const PAGE_SIZE = 10;
let allResults = [];
let currentFilter = 'All';
let currentSort = 'Highest Similarity';
let currentPage = 1;
let activeRecognition = null;
let lastQuery = '';

const recentDefaults = ['AI', 'Robotics', 'Speaker', 'OpenCV', 'Neural Network'];
const historyKey = 'videoMindSearchHistory';
const themeKey = 'videoMindTheme';

function getHistory() {
  try {
    return JSON.parse(localStorage.getItem(historyKey)) || [];
  } catch {
    return [];
  }
}

function saveHistory(entries) {
  localStorage.setItem(historyKey, JSON.stringify(entries.slice(0, 10)));
}

function updateSearchHistory() {
  const history = getHistory();
  historyList.innerHTML = '';

  if (!history.length) {
    historyList.innerHTML = '<span class="history-chip">No recent searches yet</span>';
    return;
  }

  history.forEach((query) => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'history-chip';
    chip.textContent = query;
    chip.addEventListener('click', () => runSearch(query));
    historyList.appendChild(chip);
  });
}

function updateRecentSearches(query) {
  const history = getHistory();
  const next = [query, ...history.filter((entry) => entry !== query)].slice(0, 10);
  saveHistory(next);
  updateSearchHistory();

  const chips = Array.from(new Set([query, ...recentDefaults])).slice(0, 5);
  recentList.innerHTML = '';
  chips.forEach((term) => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'recent-chip';
    chip.textContent = term;
    chip.addEventListener('click', () => runSearch(term));
    recentList.appendChild(chip);
  });
}

function setLoadingState(isLoading) {
  searchButton.disabled = isLoading;
  searchButton.innerHTML = isLoading
    ? '<span class="material-symbols-outlined animate-spin">progress_activity</span> Searching...'
    : 'Search';
  loadingState.classList.toggle('active', isLoading);
  shellResults.classList.toggle('hidden', isLoading);
}

function escapeHtml(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function getConfidenceClass(confidence) {
  const score = Number(confidence) || 0;
  if (score >= 90) return 'high';
  if (score >= 75) return 'medium';
  return 'low';
}

function formatTimestamp(value) {
  const cleaned = String(value || '00:00:00').trim();
  return cleaned.startsWith('00:') ? cleaned : `00:${cleaned}`;
}

function filterResults() {
  const filter = currentFilter.toLowerCase();
  let filtered = allResults;

  if (filter !== 'all') {
    filtered = filtered.filter((result) => {
      if (!result.category) return false;
      return result.category.toLowerCase() === filter;
    });
  }

  filtered = filtered.slice().sort((a, b) => {
    switch (currentSort) {
      case 'Earliest Timestamp':
        return a.timestamp.localeCompare(b.timestamp);
      case 'Latest Timestamp':
        return b.timestamp.localeCompare(a.timestamp);
      case 'Scene Order':
        return Number(a.scene_number || 0) - Number(b.scene_number || 0);
      case 'Highest Similarity':
      default:
        return Number(b.similarity || 0) - Number(a.similarity || 0);
    }
  });

  return filtered;
}

function renderPagination(totalItems) {
  const totalPages = Math.max(1, Math.ceil(totalItems / PAGE_SIZE));
  currentPage = Math.min(currentPage, totalPages);
  pagination.innerHTML = '';

  const prev = document.createElement('button');
  prev.type = 'button';
  prev.className = 'page-button';
  prev.textContent = 'Previous';
  prev.disabled = currentPage === 1;
  prev.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage -= 1;
      renderResults();
    }
  });
  pagination.appendChild(prev);

  for (let i = 1; i <= totalPages; i += 1) {
    const item = document.createElement('button');
    item.type = 'button';
    item.className = `page-button ${i === currentPage ? 'active' : ''}`;
    item.textContent = String(i);
    item.addEventListener('click', () => {
      currentPage = i;
      renderResults();
    });
    pagination.appendChild(item);
  }

  const next = document.createElement('button');
  next.type = 'button';
  next.className = 'page-button';
  next.textContent = 'Next';
  next.disabled = currentPage === totalPages;
  next.addEventListener('click', () => {
    if (currentPage < totalPages) {
      currentPage += 1;
      renderResults();
    }
  });
  pagination.appendChild(next);
}

function renderResults() {
  const filteredResults = filterResults();
  const start = (currentPage - 1) * PAGE_SIZE;
  const pageResults = filteredResults.slice(start, start + PAGE_SIZE);

  resultsGrid.innerHTML = '';

  if (!pageResults.length) {
    emptyState.classList.remove('hidden');
    if (searchStatus) {
      searchStatus.textContent = `No matching content found for “${lastQuery || 'your search'}”.`;
    }
    pagination.innerHTML = '';
    return;
  }

  emptyState.classList.add('hidden');
  pageResults.forEach((result, index) => {
    const card = document.createElement('article');
    card.className = 'result-card visible';
    card.style.animationDelay = `${index * 70}ms`;
    card.innerHTML = `
      <div class="result-body">
        <img class="result-thumb" alt="${escapeHtml(result.title || 'Scene thumbnail')}" src="${escapeHtml(result.thumbnail || 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80')}" />
        <div class="result-content">
          <div class="result-meta-row">
            <span class="badge ${getConfidenceClass(result.confidence || result.similarity)}">${escapeHtml(result.confidence_label || 'Matched')}</span>
            <span class="result-score">Similarity ${escapeHtml(result.similarity || 0)}%</span>
          </div>
          <h4 class="result-title">${escapeHtml(result.title || 'Search Result')}</h4>
          <p class="result-description">${escapeHtml(result.description || 'No description available.')}</p>
          <div class="result-footer">
            <div>
              <div class="result-scene">Scene ${escapeHtml(result.scene_number || 0)}</div>
              <div class="result-timestamp">Timestamp ${formatTimestamp(result.timestamp || '00:00:00')}</div>
            </div>
            <button class="jump-button" data-time="${escapeHtml(result.timestamp || '00:00:00')}" type="button">Jump to Timestamp</button>
          </div>
        </div>
      </div>
    `;

    card.querySelector('.jump-button').addEventListener('click', () => {
      const time = card.querySelector('.jump-button').dataset.time;
      window.location.href = `player.html?time=${encodeURIComponent(time)}`;
    });

    resultsGrid.appendChild(card);
  });

  renderPagination(filteredResults.length);
}

function renderStats(stats = {}) {
  const speech = Number(stats.speech_matches || 0);
  const visual = Number(stats.visual_matches || 0);
  const ocr = Number(stats.ocr_matches || 0);
  const max = Math.max(speech, visual, ocr, 1);

  const bars = [
    { label: 'Speech', value: speech, max },
    { label: 'Visual', value: visual, max },
    { label: 'OCR', value: ocr, max }
  ];

  statsPanel.innerHTML = bars.map((entry) => `
    <div class="stat-row">
      <div class="stat-label">
        <span>${entry.label} Matches</span>
        <span>${entry.value}</span>
      </div>
      <div class="stat-bar">
        <div class="stat-fill" style="width:${(entry.value / entry.max) * 100}%"></div>
      </div>
    </div>
  `).join('');
}

function renderInsight(text) {
  insightText.textContent = text || 'The system is ready to analyze a new video query.';
}

function applyTheme(mode) {
  document.body.classList.toggle('dark', mode === 'dark');
  localStorage.setItem(themeKey, mode);
  themeToggle.innerHTML = mode === 'dark'
    ? '<span class="material-symbols-outlined">light_mode</span>'
    : '<span class="material-symbols-outlined">dark_mode</span>';
}

function syncActiveNav(pathname) {
  const current = pathname.split('/').pop() || 'search.html';
  topbarLinks.forEach((link) => {
    const href = link.getAttribute('href') || '';
    link.classList.toggle('active', href.endsWith(current));
  });
  sidebarLinks.forEach((link) => {
    const href = link.getAttribute('href') || '';
    link.classList.toggle('active', href.endsWith(current));
  });
}

async function runSearch(queryText) {
  const query = (queryText || searchInput.value || '').trim();
  if (!query) return;

  lastQuery = query;
  searchInput.value = query;
  setLoadingState(true);
  updateRecentSearches(query);

  try {
    const response = await fetch('/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });

    if (!response.ok) throw new Error('Search request failed.');

    const data = await response.json();
    allResults = Array.isArray(data.results) ? data.results : [];
    renderStats(data.stats || {});
    renderInsight(data.insight || '');
    currentPage = 1;
    renderResults();
  } catch (error) {
    allResults = [];
    renderStats({});
    renderInsight('Search is temporarily unavailable. Please try again in a moment.');
    emptyState.classList.remove('hidden');
    searchStatus.textContent = 'No matching content found.';
  } finally {
    setLoadingState(false);
  }
}

function startSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    alert('Speech recognition is not supported in this browser.');
    return;
  }

  activeRecognition = new SpeechRecognition();
  activeRecognition.lang = 'en-US';
  activeRecognition.interimResults = false;
  activeRecognition.maxAlternatives = 1;
  activeRecognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    searchInput.value = transcript;
    runSearch(transcript);
  };
  activeRecognition.onerror = () => {
    alert('Speech recognition could not be completed.');
  };
  activeRecognition.start();
}

searchForm.addEventListener('submit', (event) => {
  event.preventDefault();
  runSearch(searchInput.value);
});

filterChips.forEach((chip) => {
  chip.addEventListener('click', () => {
    currentFilter = chip.dataset.filter || 'All';
    filterChips.forEach((item) => item.classList.remove('active'));
    chip.classList.add('active');
    currentPage = 1;
    renderResults();
  });
});

sortSelect.addEventListener('change', (event) => {
  currentSort = event.target.value;
  currentPage = 1;
  renderResults();
});

document.querySelectorAll('.suggestion-chip').forEach((pill) => {
  pill.addEventListener('click', () => {
    searchInput.value = pill.textContent.trim().replace(/^'|'$/g, '');
    runSearch(searchInput.value);
  });
});

voiceButton.addEventListener('click', startSpeechRecognition);

menuButton.addEventListener('click', () => {
  sidebar.classList.toggle('show');
  overlay.classList.toggle('show');
});

overlay.addEventListener('click', () => {
  sidebar.classList.remove('show');
  overlay.classList.remove('show');
});

themeToggle.addEventListener('click', () => {
  const mode = document.body.classList.contains('dark') ? 'light' : 'dark';
  applyTheme(mode);
});

document.addEventListener('keydown', (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
    event.preventDefault();
    searchInput.focus();
  }

  if (event.key === 'Escape') {
    searchInput.value = '';
    searchInput.focus();
  }
});

window.addEventListener('load', () => {
  const savedTheme = localStorage.getItem(themeKey) || 'light';
  applyTheme(savedTheme);
  syncActiveNav(window.location.pathname);
  updateSearchHistory();
  renderStats({});
  renderInsight('');
  renderResults();
});
