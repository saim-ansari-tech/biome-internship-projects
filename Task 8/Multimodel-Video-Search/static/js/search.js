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
let currentVideoId = null;
let availableVideos = [];

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

function formatTime(seconds) {
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${mins}:${secs.toString().padStart(2, '0')}`;
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
        return (a.start_time || 0) - (b.start_time || 0);
      case 'Latest Timestamp':
        return (b.start_time || 0) - (a.start_time || 0);
      case 'Scene Order':
        return Number(a.scene_number || 0) - Number(b.scene_number || 0);
      case 'Highest Similarity':
      default:
        return Number(b.score || b.similarity || 0) - Number(a.score || a.similarity || 0);
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
      searchStatus.textContent = `No matching content found for "${lastQuery || 'your search'}".`;
    }
    pagination.innerHTML = '';
    return;
  }

  emptyState.classList.add('hidden');
  pageResults.forEach((result, index) => {
    const card = document.createElement('article');
    card.className = 'result-card visible';
    card.style.animationDelay = `${index * 70}ms`;

    const startTime = formatTime(result.start_time || 0);
    const endTime = formatTime(result.end_time || 0);
    const score = ((result.score || result.similarity || 0) * 100).toFixed(1);

    card.innerHTML = `
      <div class="result-body">
        <div class="result-content" style="padding: 1rem;">
          <div class="result-meta-row">
            <span class="badge ${getConfidenceClass(score)}">${score}% Match</span>
            <span class="result-score">${startTime} - ${endTime}</span>
          </div>
          <h4 class="result-title">${escapeHtml(result.title || 'Search Result')}</h4>
          <p class="result-description">${escapeHtml(result.text || result.description || 'No description available.')}</p>
          <div class="result-footer">
            <div>
              <div class="result-timestamp">Timestamp: ${startTime} - ${endTime}</div>
            </div>
            <button class="jump-button" data-time="${result.start_time || 0}" type="button">Jump to Timestamp</button>
          </div>
        </div>
      </div>
    `;

    card.querySelector('.jump-button').addEventListener('click', () => {
      const time = card.querySelector('.jump-button').dataset.time;
      if (currentVideoId) {
        window.location.href = `/results?video_id=${currentVideoId}&time=${encodeURIComponent(time)}`;
      }
    });

    resultsGrid.appendChild(card);
  });

  renderPagination(filteredResults.length);
}

function renderStats(stats = {}) {
  const sources = allResults.length;
  const avgScore = sources > 0 ? (allResults.reduce((acc, r) => acc + (r.score || r.similarity || 0), 0) / sources * 100).toFixed(1) : 0;

  const bars = [
    { label: 'Results Found', value: sources, max: Math.max(sources, 10) },
    { label: 'Avg Confidence', value: avgScore, max: 100 },
  ];

  statsPanel.innerHTML = bars.map((entry) => `
    <div class="stat-row">
      <div class="stat-label">
        <span>${entry.label}</span>
        <span>${entry.value}${entry.label === 'Avg Confidence' ? '%' : ''}</span>
      </div>
      <div class="stat-bar">
        <div class="stat-fill" style="width:${Math.min(100, (entry.value / entry.max) * 100)}%"></div>
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
    link.classList.toggle('active', href.endsWith(current) || href === '/search');
  });
  sidebarLinks.forEach((link) => {
    const href = link.getAttribute('href') || '';
    link.classList.toggle('active', href.endsWith(current) || href === '/search');
  });
}

async function loadVideos() {
  try {
    const response = await fetch('/videos');
    const data = await response.json();

    if (data.success && data.videos) {
      availableVideos = data.videos;

      // Add video selector to search page if not exists
      let videoSelect = document.getElementById('videoSelect');
      if (!videoSelect) {
        videoSelect = document.createElement('select');
        videoSelect.id = 'videoSelect';
        videoSelect.className = 'video-select';
        videoSelect.style.cssText = 'width:100%; padding:0.75rem; margin-bottom:1rem; border-radius:999px; border:1px solid var(--outline); background:var(--surface); color:var(--text);';

        const searchShell = document.querySelector('.search-shell');
        if (searchShell) {
          searchShell.parentNode.insertBefore(videoSelect, searchShell);
        }
      }

      videoSelect.innerHTML = '<option value="">Select a processed video...</option>' +
        availableVideos.map(v => `<option value="${v.video_id}">${escapeHtml(v.video_filename)}</option>`).join('');

      videoSelect.addEventListener('change', (e) => {
        currentVideoId = e.target.value;
      });

      // Auto-select first video if only one
      if (availableVideos.length === 1) {
        currentVideoId = availableVideos[0].video_id;
        videoSelect.value = currentVideoId;
      }
    }
  } catch (error) {
    console.error('Failed to load videos:', error);
    insightText.textContent = 'Could not load video list. Please check if videos are processed.';
  }
}

async function runSearch(queryText) {
  const query = (queryText || searchInput.value || '').trim();
  if (!query) return;

  if (!currentVideoId) {
    // Check if video selector exists and has value
    const videoSelect = document.getElementById('videoSelect');
    if (videoSelect && videoSelect.value) {
      currentVideoId = videoSelect.value;
    } else {
      alert('Please select a video first from the dropdown above.');
      return;
    }
  }

  lastQuery = query;
  searchInput.value = query;
  setLoadingState(true);
  updateRecentSearches(query);

  try {
    const response = await fetch('/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ 
        video_id: currentVideoId,
        question: query,
        top_k: 10
      })
    });

    if (!response.ok) throw new Error('Search request failed.');

    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || 'Search failed');
    }

    // Convert sources to results format
    allResults = (data.sources || []).map((source, index) => ({
      title: `Result ${index + 1}`,
      description: source.text,
      text: source.text,
      start_time: source.start_time,
      end_time: source.end_time,
      score: source.score,
      similarity: (source.score * 100).toFixed(1),
      category: 'Transcript'
    }));

    renderStats();
    renderInsight(data.answer || `Found ${allResults.length} relevant moments.`);
    currentPage = 1;
    renderResults();

  } catch (error) {
    console.error('Search error:', error);
    allResults = [];
    renderStats({});
    renderInsight(`Error: ${error.message}`);
    emptyState.classList.remove('hidden');
    if (searchStatus) {
      searchStatus.textContent = 'Search failed. Please try again.';
    }
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

// Fix navigation links
function fixNavigation() {
  document.querySelectorAll('a[href]').forEach(link => {
    const href = link.getAttribute('href');
    if (href === 'dashboard.html') link.setAttribute('href', '/');
    if (href === 'index.html') link.setAttribute('href', '/');
    if (href === 'processing.html') link.setAttribute('href', '/processing');
    if (href === 'results.html') link.setAttribute('href', '/results');
    if (href === 'search.html') link.setAttribute('href', '/search');
  });
}

window.addEventListener('load', () => {
  const savedTheme = localStorage.getItem(themeKey) || 'light';
  applyTheme(savedTheme);
  syncActiveNav(window.location.pathname);
  updateSearchHistory();
  renderStats({});
  renderInsight('');
  renderResults();
  loadVideos();
  fixNavigation();
});