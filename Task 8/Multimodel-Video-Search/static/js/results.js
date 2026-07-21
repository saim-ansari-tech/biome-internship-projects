const urlParams = new URLSearchParams(window.location.search);
const videoId = urlParams.get('video_id');

// Will be populated from backend
let analysisResult = {};

const state = {
  currentFilter: 'all',
  currentTranscriptQuery: '',
  activeChapterIndex: 0,
  currentTime: 0
};

const elements = {
  videoPlayer: document.getElementById('videoPlayer'),
  progressFill: document.getElementById('progressFill'),
  progressTrack: document.getElementById('progressTrack'),
  currentTimeLabel: document.getElementById('currentTimeLabel'),
  summaryText: document.getElementById('summaryText'),
  chapterTimeline: document.getElementById('chapterTimeline'),
  chapterList: document.getElementById('chapterList'),
  transcriptContainer: document.getElementById('transcriptContainer'),
  transcriptSearch: document.getElementById('transcriptSearch'),
  keyframesGrid: document.getElementById('keyframesGrid'),
  scenesList: document.getElementById('scenesList'),
  metadataGrid: document.getElementById('metadataGrid'),
  statsGrid: document.getElementById('statsGrid'),
  fileNameLabel: document.getElementById('fileNameLabel'),
  summaryCopy: document.getElementById('summaryCopy'),
  transcriptCopy: document.getElementById('transcriptCopy'),
  themeToggle: document.getElementById('themeToggle'),
  loadingShell: document.getElementById('loadingShell'),
  contentShell: document.getElementById('contentShell')
};

function parseTimestamp(value = '00:00') {
  const parts = String(value).trim().split(':').map(Number);
  if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
  if (parts.length === 2) return parts[0] * 60 + parts[1];
  return Number(value) || 0;
}

function formatTimestamp(seconds = 0) {
  const safe = Math.max(0, Number(seconds) || 0);
  const h = Math.floor(safe / 3600);
  const m = Math.floor((safe % 3600) / 60);
  const s = Math.floor(safe % 60);
  return [h, m, s].map((part) => String(part).padStart(2, '0')).join(':');
}

function formatDisplayTime(value = '00:00') {
  return String(value).includes(':') ? String(value) : formatTimestamp(Number(value));
}

function scoreClass(level) {
  if (level >= 90) return 'score-high';
  if (level >= 75) return 'score-mid';
  return 'score-low';
}

function escapeHtml(value = '') {
  return String(value).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#039;');
}

function highlightMatches(text = '', query = '') {
  const clean = query.trim();
  if (!clean) return escapeHtml(text);
  const re = new RegExp(`(${escapeHtml(clean)})`, 'ig');
  return escapeHtml(text).replace(re, '<mark>$1</mark>');
}

function renderSummary() {
  const summary = analysisResult.summary || {};
  let summaryText = '';

  if (typeof summary === 'object' && summary.summary) {
    summaryText = summary.summary;
  } else if (typeof summary === 'string') {
    summaryText = summary;
  } else {
    summaryText = 'No summary available.';
  }

  elements.summaryText.innerHTML = `<p>${escapeHtml(summaryText)}</p>`;
}

function renderChapters() {
  const summary = analysisResult.summary || {};
  const chapters = summary.chapters || [];

  if (!chapters.length) {
    elements.chapterTimeline.innerHTML = '<p class="text-on-surface-variant">No chapters generated.</p>';
    elements.chapterList.innerHTML = '<p class="text-on-surface-variant">No chapters available.</p>';
    return;
  }

  elements.chapterTimeline.innerHTML = chapters.map((chapter, index) => `
    <button class="chapter-chip cursor-pointer rounded-full border px-4 py-3 text-sm transition-all ${index === state.activeChapterIndex ? 'active' : ''}" data-index="${index}" data-time="${parseTimestamp(chapter.start_time || 0)}">
      <span class="block text-[11px] uppercase tracking-[0.16em] text-on-surface-variant">${formatDisplayTime(chapter.start_time || 0)}</span>
      <span class="block font-semibold mt-1">${escapeHtml(chapter.title || 'Untitled Chapter')}</span>
    </button>
  `).join('');

  elements.chapterList.innerHTML = chapters.map((chapter, index) => `
    <div class="relative flex gap-4 pl-1 group cursor-pointer chapter-item ${index === state.activeChapterIndex ? 'active' : ''}" data-index="${index}" data-time="${parseTimestamp(chapter.start_time || 0)}">
      <div class="mt-1 w-6 h-6 rounded-full border-4 border-white shadow-sm ${index === state.activeChapterIndex ? 'bg-primary' : 'bg-outline-variant'}"></div>
      <div class="flex-1 pb-5 border-b border-outline-variant/10">
        <button class="rounded-full px-3 py-1 text-[11px] font-semibold ${index === state.activeChapterIndex ? 'bg-primary text-white' : 'bg-surface-container-low text-on-surface-variant'}">${formatDisplayTime(chapter.start_time || 0)}</button>
        <h4 class="font-body-base font-bold text-on-surface mt-2 mb-1">${escapeHtml(chapter.title || 'Untitled Chapter')}</h4>
        <p class="text-body-sm text-on-surface-variant">${escapeHtml(chapter.description || '')}</p>
      </div>
    </div>
  `).join('');

  elements.chapterTimeline.querySelectorAll('.chapter-chip').forEach((button) => {
    button.addEventListener('click', () => jumpToTimestamp(button.dataset.time));
  });

  elements.chapterList.querySelectorAll('.chapter-item').forEach((item) => {
    item.addEventListener('click', () => jumpToTimestamp(item.dataset.time));
  });
}

function renderTranscript() {
  const transcript = analysisResult.transcript || {};
  const segments = transcript.segments || [];
  const query = state.currentTranscriptQuery.trim();

  if (!segments.length) {
    elements.transcriptContainer.innerHTML = '<p class="text-on-surface-variant">No transcript available.</p>';
    return;
  }

  elements.transcriptContainer.innerHTML = segments.map((segment) => `
    <div class="transcript-line rounded-lg px-3 py-3 ${query ? 'active' : ''}" data-time="${parseTimestamp(segment.start || 0)}">
      <button class="text-xs font-semibold text-primary hover:text-primary-container" data-time="${parseTimestamp(segment.start || 0)}">${formatDisplayTime(segment.start || 0)} - ${formatDisplayTime(segment.end || 0)}</button>
      <p class="mt-2 text-body-sm text-on-surface-variant">${highlightMatches(segment.text, query)}</p>
    </div>
  `).join('');

  elements.transcriptContainer.querySelectorAll('button[data-time]').forEach((button) => {
    button.addEventListener('click', () => jumpToTimestamp(button.dataset.time));
  });

  updateTranscriptHighlight();
}

function renderKeyframes() {
  const scenes = analysisResult.scenes_metadata || [];

  if (!scenes.length) {
    elements.keyframesGrid.innerHTML = '<p class="text-on-surface-variant">No keyframes detected.</p>';
    return;
  }

  elements.keyframesGrid.innerHTML = scenes.map((scene, index) => `
    <article class="scene-card glass-card rounded-xl p-3">
      <button class="video-button w-full text-left" data-time="${parseTimestamp(scene.timestamp || 0)}">
        ${scene.image_path ? `<img class="scene-thumb" src="${escapeHtml(scene.image_path)}" alt="${escapeHtml(scene.description || 'Scene ' + (index + 1))}" onerror="this.style.display='none'; this.nextElementSibling.style.display='flex'" />` : ''}
        <div class="scene-thumb flex items-center justify-center bg-surface-container-low" style="${scene.image_path ? 'display:none' : ''}">
          <span class="material-symbols-outlined text-4xl text-on-surface-variant">image</span>
        </div>
      </button>
      <div class="mt-3 flex items-center justify-between gap-2">
        <span class="text-xs font-semibold text-primary">${formatDisplayTime(scene.timestamp || 0)}</span>
        <span class="text-xs text-on-surface-variant">Scene ${index + 1}</span>
      </div>
    </article>
  `).join('');

  elements.keyframesGrid.querySelectorAll('[data-time]').forEach((button) => {
    button.addEventListener('click', () => jumpToTimestamp(button.dataset.time));
  });
}

function renderScenes() {
  const scenes = analysisResult.scenes_metadata || [];

  if (!scenes.length) {
    elements.scenesList.innerHTML = '<p class="text-on-surface-variant">No scenes detected.</p>';
    return;
  }

  elements.scenesList.innerHTML = scenes.map((scene, index) => `
    <div class="glass-card rounded-xl p-4">
      <div class="flex items-center justify-between gap-2 mb-2">
        <div>
          <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant">Scene ${index + 1}</div>
          <div class="font-semibold text-primary">${formatDisplayTime(scene.timestamp || 0)}</div>
        </div>
        <button class="text-xs border rounded-full px-2 py-1 hover:bg-primary/10" data-copy="${escapeHtml(scene.description || '')}">Copy</button>
      </div>
      <p class="text-body-sm text-on-surface-variant mb-3">${escapeHtml(scene.description || 'No description available.')}</p>
    </div>
  `).join('');

  elements.scenesList.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', () => copyToClipboard(button.dataset.copy));
  });
}

function renderMetadata() {
  const transcript = analysisResult.transcript || {};
  const summary = analysisResult.summary || {};

  const metadata = [
    ['Filename', analysisResult.video_filename || 'Unknown'],
    ['Video ID', analysisResult.video_id ? analysisResult.video_id.substring(0, 8) + '...' : ''],
    ['Duration', analysisResult.duration || '--'],
    ['Resolution', analysisResult.resolution || '--'],
    ['FPS', analysisResult.fps || '--'],
    ['Video Codec', analysisResult.video_codec || '--'],
    ['Audio Codec', analysisResult.audio_codec || '--'],
    ['Language', transcript.language || '--'],
    ['Embedding Model', 'Sentence Transformers all-MiniLM-L6-v2'],
    ['Whisper Model', 'Whisper Small'],
    ['Vision Model', 'SmolVLM2-2.2B-Instruct'],
    ['Processing Time', analysisResult.processing_time || '--'],
    ['Created At', analysisResult.created_at || new Date().toLocaleString()]
  ];

  elements.metadataGrid.innerHTML = metadata.map(([label, value]) => `
    <div class="result-stat-card">
      <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant mb-2">${escapeHtml(label)}</div>
      <div class="font-mono-code text-sm font-semibold text-primary">${escapeHtml(value || '—')}</div>
    </div>
  `).join('');

  elements.fileNameLabel.textContent = analysisResult.video_filename || 'Video Analysis';
}

function renderStatistics() {
  const transcript = analysisResult.transcript || {};
  const segments = transcript.segments || [];
  const scenes = analysisResult.scenes_metadata || [];
  const chunks = analysisResult.chunks || [];

  const stats = [
    ['Total Segments', segments.length],
    ['Scenes Detected', scenes.length],
    ['Transcript Chunks', chunks.length],
    ['Transcript Words', segments.reduce((acc, s) => acc + (s.text || '').split(' ').length, 0)],
    ['Embedding Dimension', 384],
    ['Processing Time', analysisResult.processing_time || '--'],
    ['Storage Used', analysisResult.storage_used || '--']
  ];

  elements.statsGrid.innerHTML = stats.map(([label, value]) => `
    <div class="result-stat-card">
      <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant mb-2">${escapeHtml(label)}</div>
      <div class="font-mono-code text-sm font-semibold text-primary">${escapeHtml(value !== undefined ? String(value) : '—')}</div>
    </div>
  `).join('');
}

function updateProgressBar() {
  if (!elements.videoPlayer.duration) return;
  const ratio = (elements.videoPlayer.currentTime / elements.videoPlayer.duration) * 100;
  elements.progressFill.style.width = `${ratio}%`;
  elements.currentTimeLabel.textContent = `${formatTimestamp(elements.videoPlayer.currentTime)} / ${formatTimestamp(elements.videoPlayer.duration)}`;
}

function updateTranscriptHighlight() {
  const currentTime = elements.videoPlayer.currentTime || 0;
  const transcriptLines = Array.from(elements.transcriptContainer.querySelectorAll('.transcript-line'));

  if (!transcriptLines.length) return;

  let matchedIndex = -1;
  transcriptLines.forEach((line, index) => {
    const lineTime = Number(line.dataset.time || 0);
    if (currentTime >= lineTime) matchedIndex = index;
  });

  transcriptLines.forEach((line, index) => line.classList.toggle('active', index === matchedIndex));
}

function updateChapterHighlight() {
  const currentTime = elements.videoPlayer.currentTime || 0;
  const summary = analysisResult.summary || {};
  const chapters = summary.chapters || [];
  let matchedIndex = 0;

  chapters.forEach((chapter, index) => {
    if (currentTime >= parseTimestamp(chapter.start_time || 0)) matchedIndex = index;
  });

  state.activeChapterIndex = matchedIndex;
  renderChapters();
}

function jumpToTimestamp(timestampSeconds) {
  const player = elements.videoPlayer;
  if (!player) return;
  player.currentTime = Number(timestampSeconds) || 0;
  player.play();
}

function renderTimingMarkers() {
  const summary = analysisResult.summary || {};
  const chapters = summary.chapters || [];
  const duration = Number(elements.videoPlayer.duration) || 1;

  elements.progressTrack.querySelectorAll('.timeline-marker').forEach((marker) => marker.remove());

  chapters.forEach((chapter) => {
    const marker = document.createElement('button');
    marker.type = 'button';
    marker.className = 'timeline-marker';
    marker.dataset.title = chapter.title || 'Chapter';
    marker.dataset.time = chapter.start_time || 0;
    const offset = Math.max(0, Math.min(100, (parseTimestamp(chapter.start_time || 0) / duration) * 100));
    marker.style.left = `${offset}%`;
    marker.addEventListener('click', () => jumpToTimestamp(parseTimestamp(chapter.start_time || 0)));
    elements.progressTrack.appendChild(marker);
  });
}

function copyToClipboard(text) {
  if (!navigator.clipboard) return;
  navigator.clipboard.writeText(text);
}

function exportFile(filename, content, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);
}

function exportReport(type = 'json') {
  if (type === 'json') {
    exportFile('analysis-report.json', JSON.stringify(analysisResult, null, 2), 'application/json');
    return;
  }

  if (type === 'txt') {
    const transcript = analysisResult.transcript || {};
    const segments = transcript.segments || [];
    const summary = analysisResult.summary || {};
    const summaryText = typeof summary === 'object' ? (summary.summary || '') : summary;
    const text = `${summaryText}\n\nTranscript:\n${segments.map((line) => `${formatDisplayTime(line.start || line.timestamp || 0)} ${line.text}`).join('\n')}\n`;
    exportFile('analysis-report.txt', text, 'text/plain');
    return;
  }

  if (type === 'pdf') {
    const summary = analysisResult.summary || {};
    const summaryText = typeof summary === 'object' ? (summary.summary || '') : summary;
    const pdf = `%PDF-1.4\n1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n4 0 obj<< /Length 144 >>stream\nBT /F1 14 Tf 50 750 Td (${analysisResult.video_filename || 'analysis'}) Tj 0 -20 Td /F1 10 Tf (${summaryText}) Tj ET\nendstream\nendobj\n5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000063 00000 n \n0000000123 00000 n \n0000000242 00000 n \n0000001450 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n1539\n%%EOF`;
    exportFile('analysis-report.pdf', pdf, 'application/pdf');
    return;
  }

  if (type === 'transcript') {
    const transcript = analysisResult.transcript || {};
    const segments = transcript.segments || [];
    const text = segments.map((entry) => `${formatDisplayTime(entry.start || entry.timestamp || 0)} ${entry.text}`).join('\n\n');
    exportFile('transcript.txt', text, 'text/plain');
  }
}

function toggleTheme(mode = null) {
  const next = mode || (document.body.classList.contains('dark') ? 'light' : 'dark');
  document.body.classList.toggle('dark', next === 'dark');
  localStorage.setItem('videoMindTheme', next);
  elements.themeToggle.innerHTML = next === 'dark' ? '<span class="material-symbols-outlined">light_mode</span>' : '<span class="material-symbols-outlined">dark_mode</span>';
}

function bindNavigation() {
  document.querySelectorAll('[data-nav]').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      let href = link.dataset.nav;
      if (href.includes('dashboard')) href = '/';
      else if (href.includes('processing')) href = '/processing';
      else if (href.includes('search')) href = '/search';
      else if (href.includes('results')) href = '/results';
      window.location.href = href;
    });
  });
}

function bindActions() {
  if (elements.summaryCopy) {
    elements.summaryCopy.addEventListener('click', () => {
      const summary = analysisResult.summary || {};
      const text = typeof summary === 'object' ? (summary.summary || '') : summary;
      copyToClipboard(text);
    });
  }

  if (elements.transcriptCopy) {
    elements.transcriptCopy.addEventListener('click', () => {
      const transcript = analysisResult.transcript || {};
      const segments = transcript.segments || [];
      copyToClipboard(segments.map((entry) => `${formatDisplayTime(entry.start || entry.timestamp || 0)} ${entry.text}`).join('\n\n'));
    });
  }

  const sceneCopyBtn = document.getElementById('sceneCopy');
  if (sceneCopyBtn) {
    sceneCopyBtn.addEventListener('click', () => {
      const scenes = analysisResult.scenes_metadata || [];
      copyToClipboard(scenes.map((scene, i) => `${i + 1} ${formatDisplayTime(scene.timestamp || 0)} ${scene.description}`).join('\n'));
    });
  }

  const exportJson = document.getElementById('exportJson');
  if (exportJson) exportJson.addEventListener('click', () => exportReport('json'));

  const exportTxt = document.getElementById('exportTxt');
  if (exportTxt) exportTxt.addEventListener('click', () => exportReport('txt'));

  const exportPdf = document.getElementById('exportPdf');
  if (exportPdf) exportPdf.addEventListener('click', () => exportReport('pdf'));

  const exportTranscript = document.getElementById('exportTranscript');
  if (exportTranscript) exportTranscript.addEventListener('click', () => exportReport('transcript'));

  const copyLink = document.getElementById('copyLink');
  if (copyLink) copyLink.addEventListener('click', () => copyToClipboard(window.location.href));

  const copySummary = document.getElementById('copySummary');
  if (copySummary) copySummary.addEventListener('click', () => {
    const summary = analysisResult.summary || {};
    copyToClipboard(typeof summary === 'object' ? (summary.summary || '') : summary);
  });

  const downloadReport = document.getElementById('downloadReport');
  if (downloadReport) downloadReport.addEventListener('click', () => exportReport('json'));

  if (elements.transcriptSearch) {
    elements.transcriptSearch.addEventListener('input', (event) => {
      state.currentTranscriptQuery = event.target.value;
      renderTranscript();
    });
  }

  if (elements.themeToggle) {
    elements.themeToggle.addEventListener('click', () => toggleTheme());
  }

  const menuButton = document.getElementById('menuButton');
  if (menuButton) {
    menuButton.addEventListener('click', () => {
      document.getElementById('sidebar').classList.toggle('show');
      document.getElementById('overlay').classList.toggle('show');
    });
  }

  const overlay = document.getElementById('overlay');
  if (overlay) {
    overlay.addEventListener('click', () => {
      document.getElementById('sidebar').classList.remove('show');
      document.getElementById('overlay').classList.remove('show');
    });
  }
}

function loadVideo() {
  const player = elements.videoPlayer;
  // Use the actual video file from backend, not placeholder
  const videoUrl = analysisResult.video_url || `/video_file/${videoId}`;
  player.src = videoUrl;
  player.poster = '';
  player.addEventListener('loadedmetadata', () => {
    elements.currentTimeLabel.textContent = `00:00 / ${formatTimestamp(player.duration || 0)}`;
    renderTimingMarkers();
  });
  player.addEventListener('timeupdate', () => {
    state.currentTime = player.currentTime;
    updateProgressBar();
    updateTranscriptHighlight();
    updateChapterHighlight();
  });
  player.addEventListener('seeked', () => {
    updateProgressBar();
    updateTranscriptHighlight();
    updateChapterHighlight();
  });

  // Handle video load error - show message if video can't be played
  player.addEventListener('error', () => {
    console.error('Video load error');
    // Keep the player but it will show the browser's default error
  });
}

async function loadResults() {
  if (!videoId) {
    elements.fileNameLabel.textContent = 'No Video ID';
    elements.summaryText.innerHTML = '<p class="text-error">Please provide a video_id in the URL.</p>';
    elements.loadingShell.classList.add('hidden');
    elements.contentShell.classList.remove('hidden');
    return;
  }

  try {
    const response = await fetch(`/video/${videoId}`);
    const data = await response.json();

    if (!data.success || !data.video) {
      throw new Error(data.error || 'Video not found');
    }

    analysisResult = data.video;

    // Ensure summary is properly structured
    if (analysisResult.summary && typeof analysisResult.summary === 'object') {
      // Already structured correctly from backend
    } else if (analysisResult.summary && typeof analysisResult.summary === 'string') {
      // Try to parse if it's a JSON string
      try {
        const parsed = JSON.parse(analysisResult.summary);
        analysisResult.summary = parsed;
      } catch (e) {
        // Wrap in proper structure
        analysisResult.summary = {
          summary: analysisResult.summary,
          chapters: []
        };
      }
    }

    if (!analysisResult.summary) {
      analysisResult.summary = {
        summary: 'No summary available.',
        chapters: []
      };
    }

    renderAll();

    elements.loadingShell.classList.add('hidden');
    elements.contentShell.classList.remove('hidden');

  } catch (error) {
    console.error('Failed to load results:', error);
    elements.fileNameLabel.textContent = 'Error';
    elements.summaryText.innerHTML = `<p class="text-error">Failed to load results: ${escapeHtml(error.message)}</p>`;
    elements.loadingShell.classList.add('hidden');
    elements.contentShell.classList.remove('hidden');
  }
}

function renderAll() {
  loadVideo();
  renderSummary();
  renderChapters();
  renderTranscript();
  renderKeyframes();
  renderScenes();
  renderMetadata();
  renderStatistics();
}

function initialize() {
  toggleTheme(localStorage.getItem('videoMindTheme') || 'light');
  bindNavigation();
  bindActions();
  loadResults();
}

window.addEventListener('load', initialize);