const sampleVideo = 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4';

window.analysisResult = window.analysisResult || {
  filename: 'ai_intro.mp4',
  duration: '15:20',
  scenes: 42,
  transcript_chunks: 128,
  summary: 'This presentation provides a comprehensive deep dive into the evolution of Artificial Intelligence, starting from early neural networks to modern transformer architectures and future applications of generative AI.',
  chapters: [
    { title: 'Introduction', timestamp: '00:00', description: 'Opening remarks and session overview defining the scope of the intelligence analysis.' },
    { title: 'History of Neural Networks', timestamp: '02:15', description: 'Tracing the lineage from perceptrons to backpropagation and the first deep architectures.' },
    { title: 'Modern Transformers', timestamp: '05:45', description: 'Breakdown of the Attention is All You Need paper and its impact on AI.' },
    { title: 'Generative Capabilities', timestamp: '10:30', description: 'Exploration of latent spaces and how diffusion models differ from autoregressive ones.' },
    { title: 'Future Outlook', timestamp: '14:00', description: 'Closing thoughts on AGI timelines and ethical considerations for the next decade.' }
  ],
  transcript: [
    { timestamp: '00:15', text: 'Welcome everyone to this presentation on the future of artificial intelligence.' },
    { timestamp: '01:20', text: 'Today we discuss how transformer models changed the landscape of language understanding.' },
    { timestamp: '02:05', text: 'Artificial Intelligence now powers search, recommendation, and generative experiences across the web.' },
    { timestamp: '05:15', text: 'The evolution from neural networks to attention-based models created a new wave of intelligent systems.' },
    { timestamp: '08:20', text: 'Vision models and multimodal reasoning continue to improve how machines understand videos and images.' }
  ],
  keywords: ['AI', 'Neural Network', 'Transformers', 'Vision', 'Multimodal'],
  video_url: sampleVideo,
  thumbnail: 'https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80',
  created_at: '2026-07-20T12:35:00Z',
  resolution: '1920x1080',
  fps: 29.97,
  video_codec: 'H.264',
  audio_codec: 'AAC',
  language: 'English',
  embedding_model: 'Sentence Transformers all-MiniLM-L6-v2',
  whisper_model: 'Whisper Large v3',
  vision_model: 'SmolVLM',
  processing_time: '02m 14s',
  total_frames: 27000,
  keyframes_extracted: 18,
  transcript_words: 418,
  embedding_dimension: 384,
  storage_used: '1.8 GB',
  keyframes: [
    { timestamp: '00:12', title: 'Introduction Slide', thumbnail: 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=80' },
    { timestamp: '02:26', title: 'Neural Network Diagram', thumbnail: 'https://images.unsplash.com/photo-1516321497487-e288fb19713f?auto=format&fit=crop&w=900&q=80' },
    { timestamp: '05:50', title: 'Transformer Overview', thumbnail: 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?auto=format&fit=crop&w=900&q=80' },
    { timestamp: '10:41', title: 'Generative AI Scene', thumbnail: 'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=900&q=80' }
  ],
  scenes: [
    { scene_number: 1, timestamp: '00:00', description: 'Speaker introduces the session and outlines the AI journey.', confidence: 97 },
    { scene_number: 2, timestamp: '02:15', description: 'Historical overview of neural network development and early learning models.', confidence: 92 },
    { scene_number: 3, timestamp: '05:45', description: 'Explanation of encoder-decoder attention and transformer architecture.', confidence: 95 },
    { scene_number: 4, timestamp: '10:30', description: 'Speaker standing beside presentation slide discussing multimodal future applications.', confidence: 96 }
  ],
  analysis_status: {
    transcription: 100,
    object_detection: 100,
    sentiment_scoring: 82
  },
  confidence: {
    summary: 95,
    transcript: 91,
    detection: 94
  }
};

const analysisResult = window.analysisResult;
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
  sceneCopy: document.getElementById('sceneCopy'),
  themeToggle: document.getElementById('themeToggle'),
  loadingShell: document.getElementById('loadingShell'),
  contentShell: document.getElementById('contentShell')
};

function parseTimestamp(value = '00:00') {
  const parts = String(value).trim().split(':').map(Number);
  if (parts.length === 3) return parts[0] * 3600 + parts[1] * 60 + parts[2];
  if (parts.length === 2) return parts[0] * 60 + parts[1];
  return 0;
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
  elements.summaryText.innerHTML = `<p>${escapeHtml(analysisResult.summary || 'No summary available yet.')}</p>`;
}

function renderChapters() {
  const chapters = Array.isArray(analysisResult.chapters) ? analysisResult.chapters : [];

  elements.chapterTimeline.innerHTML = chapters.map((chapter, index) => `
    <button class="chapter-chip cursor-pointer rounded-full border px-4 py-3 text-sm transition-all ${index === state.activeChapterIndex ? 'active' : ''}" data-index="${index}" data-time="${parseTimestamp(chapter.timestamp)}">
      <span class="block text-[11px] uppercase tracking-[0.16em] text-on-surface-variant">${escapeHtml(chapter.timestamp)}</span>
      <span class="block font-semibold mt-1">${escapeHtml(chapter.title || 'Untitled Chapter')}</span>
    </button>
  `).join('');

  elements.chapterList.innerHTML = chapters.map((chapter, index) => `
    <div class="relative flex gap-4 pl-1 group cursor-pointer chapter-item ${index === state.activeChapterIndex ? 'active' : ''}" data-index="${index}" data-time="${parseTimestamp(chapter.timestamp)}">
      <div class="mt-1 w-6 h-6 rounded-full border-4 border-white shadow-sm ${index === state.activeChapterIndex ? 'bg-primary' : 'bg-outline-variant'}"></div>
      <div class="flex-1 pb-5 border-b border-outline-variant/10">
        <button class="rounded-full px-3 py-1 text-[11px] font-semibold ${index === state.activeChapterIndex ? 'bg-primary text-white' : 'bg-surface-container-low text-on-surface-variant'}">${escapeHtml(chapter.timestamp)}</button>
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
  const transcript = Array.isArray(analysisResult.transcript) ? analysisResult.transcript : [];
  const query = state.currentTranscriptQuery.trim();

  elements.transcriptContainer.innerHTML = transcript.map((segment) => `
    <div class="transcript-line rounded-lg px-3 py-3 ${query ? 'active' : ''}" data-time="${parseTimestamp(segment.timestamp)}">
      <button class="text-xs font-semibold text-primary hover:text-primary-container" data-time="${parseTimestamp(segment.timestamp)}">${escapeHtml(segment.timestamp)}</button>
      <p class="mt-2 text-body-sm text-on-surface-variant">${highlightMatches(segment.text, query)}</p>
    </div>
  `).join('');

  elements.transcriptContainer.querySelectorAll('button[data-time]').forEach((button) => {
    button.addEventListener('click', () => jumpToTimestamp(button.dataset.time));
  });

  updateTranscriptHighlight();
}

function renderKeyframes() {
  const keyframes = Array.isArray(analysisResult.keyframes) ? analysisResult.keyframes : [];
  elements.keyframesGrid.innerHTML = keyframes.map((frame) => `
    <article class="scene-card glass-card rounded-xl p-3">
      <button class="video-button w-full text-left" data-time="${parseTimestamp(frame.timestamp)}">
        <img class="scene-thumb" src="${escapeHtml(frame.thumbnail || analysisResult.thumbnail || '')}" alt="${escapeHtml(frame.title || 'Detected keyframe')}" />
      </button>
      <div class="mt-3 flex items-center justify-between gap-2">
        <span class="text-xs font-semibold text-primary">${escapeHtml(frame.timestamp)}</span>
        <span class="text-xs text-on-surface-variant">${escapeHtml(frame.title || 'Scene preview')}</span>
      </div>
    </article>
  `).join('');

  elements.keyframesGrid.querySelectorAll('[data-time]').forEach((button) => {
    button.addEventListener('click', () => jumpToTimestamp(button.dataset.time));
  });
}

function renderScenes() {
  const scenes = Array.isArray(analysisResult.scenes) ? analysisResult.scenes : [];
  elements.scenesList.innerHTML = scenes.map((scene) => `
    <div class="glass-card rounded-xl p-4">
      <div class="flex items-center justify-between gap-2 mb-2">
        <div>
          <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant">Scene ${escapeHtml(scene.scene_number || 1)}</div>
          <div class="font-semibold text-primary">${escapeHtml(scene.timestamp || '00:00')}</div>
        </div>
        <button class="text-xs border rounded-full px-2 py-1 hover:bg-primary/10" data-copy="${escapeHtml(scene.description || '')}">Copy</button>
      </div>
      <p class="text-body-sm text-on-surface-variant mb-3">${escapeHtml(scene.description || '')}</p>
      <div>
        <div class="flex items-center justify-between text-xs mb-1">
          <span>Confidence</span>
          <span>${escapeHtml(scene.confidence || 0)}%</span>
        </div>
        <div class="confidence-bar">
          <div class="confidence-fill ${scoreClass(scene.confidence || 0)}" style="width:${Math.max(0, Math.min(100, scene.confidence || 0))}%"></div>
        </div>
      </div>
    </div>
  `).join('');

  elements.scenesList.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', () => copyToClipboard(button.dataset.copy));
  });
}

function renderMetadata() {
  const metadata = [
    ['Filename', analysisResult.filename],
    ['Duration', analysisResult.duration],
    ['Resolution', analysisResult.resolution],
    ['FPS', analysisResult.fps],
    ['Video Codec', analysisResult.video_codec],
    ['Audio Codec', analysisResult.audio_codec],
    ['Language', analysisResult.language],
    ['Embedding Model', analysisResult.embedding_model],
    ['Whisper Model', analysisResult.whisper_model],
    ['Vision Model', analysisResult.vision_model],
    ['Processing Time', analysisResult.processing_time],
    ['Created At', analysisResult.created_at]
  ];

  elements.metadataGrid.innerHTML = metadata.map(([label, value]) => `
    <div class="result-stat-card">
      <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant mb-2">${escapeHtml(label)}</div>
      <div class="font-mono-code text-sm font-semibold text-primary">${escapeHtml(value || '—')}</div>
    </div>
  `).join('');

  elements.fileNameLabel.textContent = analysisResult.filename || 'Video analysis';
}

function renderStatistics() {
  const stats = [
    ['Total Frames', analysisResult.total_frames],
    ['Keyframes Extracted', analysisResult.keyframes_extracted],
    ['Scenes', analysisResult.scenes],
    ['Transcript Words', analysisResult.transcript_words],
    ['Transcript Chunks', analysisResult.transcript_chunks],
    ['Embedding Dimension', analysisResult.embedding_dimension],
    ['Processing Time', analysisResult.processing_time],
    ['Storage Used', analysisResult.storage_used]
  ];

  elements.statsGrid.innerHTML = stats.map(([label, value]) => `
    <div class="result-stat-card">
      <div class="text-[11px] uppercase tracking-[0.16em] text-on-surface-variant mb-2">${escapeHtml(label)}</div>
      <div class="font-mono-code text-sm font-semibold text-primary">${escapeHtml(value || '—')}</div>
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
  const chapters = Array.isArray(analysisResult.chapters) ? analysisResult.chapters : [];
  let matchedIndex = 0;

  chapters.forEach((chapter, index) => {
    if (currentTime >= parseTimestamp(chapter.timestamp)) matchedIndex = index;
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
  const chapters = Array.isArray(analysisResult.chapters) ? analysisResult.chapters : [];
  const trackWidth = elements.progressTrack.clientWidth || 0;
  const duration = Number(elements.videoPlayer.duration) || 1;

  elements.progressTrack.querySelectorAll('.timeline-marker').forEach((marker) => marker.remove());

  chapters.forEach((chapter) => {
    const marker = document.createElement('button');
    marker.type = 'button';
    marker.className = 'timeline-marker';
    marker.dataset.title = chapter.title || 'Chapter';
    marker.dataset.time = chapter.timestamp || '00:00';
    const offset = Math.max(0, Math.min(100, (parseTimestamp(chapter.timestamp) / duration) * 100));
    marker.style.left = `${offset}%`;
    marker.addEventListener('click', () => jumpToTimestamp(parseTimestamp(chapter.timestamp)));
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
    const text = `${analysisResult.summary}\n\nTranscript:\n${analysisResult.transcript.map((line) => `${line.timestamp} ${line.text}`).join('\n')}\n`;
    exportFile('analysis-report.txt', text, 'text/plain');
    return;
  }

  if (type === 'pdf') {
    const pdf = `%PDF-1.4\n1 0 obj<< /Type /Catalog /Pages 2 0 R >>endobj\n2 0 obj<< /Type /Pages /Kids [3 0 R] /Count 1 >>endobj\n3 0 obj<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>endobj\n4 0 obj<< /Length 144 >>stream\nBT /F1 14 Tf 50 750 Td (${analysisResult.filename || 'analysis'}) Tj 0 -20 Td /F1 10 Tf (${analysisResult.summary || ''}) Tj ET\nendstream\nendobj\n5 0 obj<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>endobj\nxref\n0 6\n0000000000 65535 f \n0000000010 00000 n \n0000000063 00000 n \n0000000123 00000 n \n0000000242 00000 n \n0000001450 00000 n \ntrailer\n<< /Root 1 0 R /Size 6 >>\nstartxref\n1539\n%%EOF`;
    exportFile('analysis-report.pdf', pdf, 'application/pdf');
    return;
  }

  if (type === 'transcript') {
    const text = analysisResult.transcript.map((entry) => `${entry.timestamp} ${entry.text}`).join('\n\n');
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
      window.location.href = link.dataset.nav;
    });
  });
}

function bindActions() {
  elements.summaryCopy.addEventListener('click', () => copyToClipboard(analysisResult.summary));
  elements.transcriptCopy.addEventListener('click', () => copyToClipboard(analysisResult.transcript.map((entry) => `${entry.timestamp} ${entry.text}`).join('\n\n')));
  elements.sceneCopy.addEventListener('click', () => copyToClipboard(analysisResult.scenes.map((scene) => `${scene.scene_number} ${scene.timestamp} ${scene.description}`).join('\n')));

  document.getElementById('exportJson').addEventListener('click', () => exportReport('json'));
  document.getElementById('exportTxt').addEventListener('click', () => exportReport('txt'));
  document.getElementById('exportPdf').addEventListener('click', () => exportReport('pdf'));
  document.getElementById('exportTranscript').addEventListener('click', () => exportReport('transcript'));
  document.getElementById('copyLink').addEventListener('click', () => copyToClipboard(window.location.href));
  document.getElementById('copySummary').addEventListener('click', () => copyToClipboard(analysisResult.summary));
  document.getElementById('downloadReport').addEventListener('click', () => exportReport('json'));

  elements.transcriptSearch.addEventListener('input', (event) => {
    state.currentTranscriptQuery = event.target.value;
    renderTranscript();
  });

  elements.themeToggle.addEventListener('click', () => toggleTheme());

  document.getElementById('menuButton').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('show');
    document.getElementById('overlay').classList.toggle('show');
  });

  document.getElementById('overlay').addEventListener('click', () => {
    document.getElementById('sidebar').classList.remove('show');
    document.getElementById('overlay').classList.remove('show');
  });
}

function loadVideo() {
  const player = elements.videoPlayer;
  player.src = analysisResult.video_url || sampleVideo;
  player.poster = analysisResult.thumbnail || '';
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
}

function initialize() {
  toggleTheme(localStorage.getItem('videoMindTheme') || 'light');
  bindNavigation();
  bindActions();
  loadVideo();
  renderSummary();
  renderTranscript();
  renderChapters();
  renderKeyframes();
  renderScenes();
  renderMetadata();
  renderStatistics();

  window.setTimeout(() => {
    elements.loadingShell.classList.add('hidden');
    elements.contentShell.classList.remove('hidden');
  }, 400);
}

window.addEventListener('load', initialize);
