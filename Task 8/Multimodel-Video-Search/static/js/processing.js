const urlParams = new URLSearchParams(window.location.search);
const videoId = urlParams.get('video_id');

const ui = {
  title: document.getElementById("page-title"),
  appName: document.getElementById("app-name"),
  subtitle: document.getElementById("app-subtitle"),
  navItems: document.querySelectorAll(".sidebar-link"),
  activeNavText: document.getElementById("processing-nav"),
  stepList: document.getElementById("pipeline-steps"),
  currentTask: document.getElementById("current-task"),
  progressNumber: document.getElementById("progress-number"),
  progressLabel: document.getElementById("progress-label"),
  progressRing: document.getElementById("progress-ring"),
  elapsedTime: document.getElementById("elapsed-time"),
  remainingTime: document.getElementById("remaining-time"),
  framesProcessed: document.getElementById("frames-processed"),
  detectedScenes: document.getElementById("detected-scenes"),
  transcriptLength: document.getElementById("transcript-length"),
  logContainer: document.getElementById("log-container"),
  cancelBtn: document.getElementById("cancel-job"),
  completionCard: document.getElementById("completion-card"),
  viewResultsBtn: document.getElementById("view-results-btn"),
  footerYear: document.getElementById("footer-year"),
  themeToggle: document.getElementById("theme-toggle"),
  sidebar: document.getElementById("sidebar"),
  mobileMenuButton: document.getElementById("mobile-menu-button"),
  sidebarOverlay: document.getElementById("sidebar-overlay"),
  workflowRow: document.getElementById("workflow-row"),
  fileName: document.getElementById("file-name"),
  duration: document.getElementById("duration"),
  resolution: document.getElementById("resolution"),
  fps: document.getElementById("fps"),
  size: document.getElementById("size"),
  uploadTime: document.getElementById("upload-time")
};

const pipelineSteps = [
  { name: "Upload Video", status: "completed" },
  { name: "Extract Audio", status: "pending" },
  { name: "Speech-to-Text (Whisper)", status: "pending" },
  { name: "Scene Detection", status: "pending" },
  { name: "Keyframe Extraction", status: "pending" },
  { name: "Scene Description Generation", status: "pending" },
  { name: "Summary Generation", status: "pending" },
  { name: "Chapter Generation", status: "pending" },
  { name: "Text Chunking", status: "pending" },
  { name: "Embedding Generation", status: "pending" },
  { name: "Store in Qdrant", status: "pending" },
  { name: "Semantic Search Ready", status: "pending" }
];

const workflow = [
  "Video", "Audio", "Whisper", "Transcript", "Chunks", "Embeddings", "Qdrant", "Ready"
];

const stateColors = {
  pending: "bg-slate-100 text-slate-500",
  running: "bg-blue-100 text-blue-700",
  completed: "bg-emerald-100 text-emerald-700",
  failed: "bg-rose-100 text-rose-700"
};

let progressValue = 0;
let currentStepIndex = 0;
let timerSeconds = 0;
let timerInterval = null;
let pollInterval = null;
let processingComplete = false;

function formatTime(totalSeconds) {
  const hrs = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const mins = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const secs = String(totalSeconds % 60).padStart(2, "0");
  return `${hrs}:${mins}:${secs}`;
}

function formatBytes(bytes) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  let value = bytes;
  let index = 0;
  while (value >= 1024 && index < units.length - 1) {
    value /= 1024;
    index += 1;
  }
  return `${value.toFixed(value >= 10 || index === 0 ? 0 : 1)} ${units[index]}`;
}

function updateProgress(percent) {
  progressValue = Math.max(0, Math.min(100, percent));
  const radius = 110;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (progressValue / 100) * circumference;

  ui.progressNumber.textContent = `${progressValue}%`;
  ui.progressLabel.textContent = progressValue === 100 ? "Completed" : "Complete";
  ui.progressRing.style.strokeDasharray = circumference;
  ui.progressRing.style.strokeDashoffset = offset;
}

function updateCurrentStep(stepIndex) {
  currentStepIndex = stepIndex;
  const step = pipelineSteps[stepIndex];
  if (step) {
    ui.currentTask.textContent = step.name;
  }
  renderPipeline();
  renderWorkflow();
}

function renderPipeline() {
  ui.stepList.innerHTML = "";

  pipelineSteps.forEach((step, index) => {
    let state = "pending";
    if (index < currentStepIndex) state = "completed";
    else if (index === currentStepIndex) state = "running";

    const item = document.createElement("div");
    item.className = `step-item flex items-center gap-md p-sm rounded-lg border ${state === "running" ? "running" : state === "completed" ? "completed" : "pending"}`;

    let icon = "pending";
    let meta = "Waiting";

    if (state === "completed") {
      icon = "check";
      meta = "Completed";
    } else if (state === "running") {
      icon = "sync";
      meta = "Running";
    } else if (state === "failed") {
      icon = "error";
      meta = "Failed";
    }

    item.innerHTML = `
      <div class="w-9 h-9 rounded-full ${stateColors[state]} flex items-center justify-center text-[18px] shadow-sm">
        <span class="material-symbols-outlined">${icon}</span>
      </div>
      <div class="flex-1">
        <p class="font-body-base text-body-base font-semibold">${step.name}</p>
        <p class="font-body-sm text-body-sm ${state === "completed" ? "text-emerald-700" : state === "running" ? "text-blue-700" : "text-slate-500"}">${meta}</p>
      </div>
      ${state === "completed" ? '<span class="text-[10px] font-mono-code uppercase text-emerald-700">done</span>' : state === "failed" ? '<span class="text-[10px] font-mono-code uppercase text-rose-700">fail</span>' : ''}
    `;
    ui.stepList.appendChild(item);
  });
}

function renderWorkflow() {
  ui.workflowRow.innerHTML = "";
  workflow.forEach((item, index) => {
    const step = document.createElement("div");
    step.className = "workflow-step flex items-center gap-2 px-3 py-2 rounded-full text-xs font-semibold";

    if (index < currentStepIndex || currentStepIndex >= workflow.length) {
      step.classList.add("completed");
    } else if (index === currentStepIndex) {
      step.classList.add("active");
    } else {
      step.classList.add("pending");
    }

    step.textContent = item;
    ui.workflowRow.appendChild(step);
  });
}

function appendLog(message) {
  const line = document.createElement("p");
  line.className = "log-line text-primary opacity-80";
  line.textContent = `[${formatTime(timerSeconds)}] ${message}`;
  ui.logContainer.appendChild(line);
  ui.logContainer.scrollTop = ui.logContainer.scrollHeight;

  while (ui.logContainer.children.length > 50) {
    ui.logContainer.removeChild(ui.logContainer.firstChild);
  }
}

function mapStepToIndex(stepName, progress) {
  // Map backend step names to pipeline step indices
  const stepMap = {
    "Initializing": 0,
    "Upload Complete": 0,
    "Scene Detection": 3,
    "Keyframe Extraction": 4,
    "Scene Description": 5,
    "Scene Description (VLM)": 5,
    "Scene Description Complete": 5,
    "Audio Extraction": 1,
    "Audio Extraction Complete": 1,
    "Transcribing": 2,
    "Transcribing (Whisper)": 2,
    "Transcription Complete": 2,
    "Generating Summary": 6,
    "Summary Complete": 6,
    "Chunking": 8,
    "Chunking Transcript": 8,
    "Generating Embeddings": 9,
    "Storing in Qdrant": 10,
    "Finalizing": 11,
    "Complete": 11,
    "Failed": 11
  };

  for (const [key, value] of Object.entries(stepMap)) {
    if (stepName && stepName.toLowerCase().includes(key.toLowerCase())) {
      return value;
    }
  }

  // Fallback: estimate from progress
  return Math.floor((progress / 100) * pipelineSteps.length);
}

function finishProcessing() {
  clearInterval(timerInterval);
  clearInterval(pollInterval);
  processingComplete = true;
  updateProgress(100);
  updateCurrentStep(pipelineSteps.length - 1);
  ui.cancelBtn.classList.add("hidden");
  ui.completionCard.classList.remove("hidden");
  ui.viewResultsBtn.classList.remove("hidden");
  appendLog("Processing completed successfully!");
}

function failProcessing(errorMsg) {
  clearInterval(timerInterval);
  clearInterval(pollInterval);
  updateProgress(0);
  ui.currentTask.textContent = "Processing Failed";
  ui.currentTask.style.color = "#ef4444";
  appendLog(`ERROR: ${errorMsg}`);
  ui.cancelBtn.classList.remove("hidden");
  ui.viewResultsBtn.classList.add("hidden");
}

function cancelProcessing() {
  const confirmed = window.confirm("Are you sure you want to cancel?");
  if (!confirmed) return;
  clearInterval(timerInterval);
  clearInterval(pollInterval);
  window.location.href = "/";
}

function startTimer() {
  timerInterval = setInterval(() => {
    timerSeconds += 1;
    ui.elapsedTime.textContent = formatTime(timerSeconds);
    // Estimate remaining based on progress
    if (progressValue > 0 && progressValue < 100) {
      const remaining = Math.ceil((timerSeconds / progressValue) * (100 - progressValue));
      ui.remainingTime.textContent = formatTime(remaining);
    }
  }, 1000);
}

async function pollStatus() {
  if (!videoId) {
    appendLog("ERROR: No video ID found in URL");
    ui.currentTask.textContent = "Error: No Video ID";
    return;
  }

  try {
    const response = await fetch(`/status/${videoId}`);
    const data = await response.json();

    if (!data.success) {
      throw new Error(data.error || "Failed to get status");
    }

    const progress = data.progress || 0;
    const status = data.status;
    const step = data.step || "Processing";
    const metadata = data.metadata || {};

    updateProgress(progress);

    // Map step to pipeline index
    const stepIndex = mapStepToIndex(step, progress);
    updateCurrentStep(stepIndex);

    appendLog(`Status: ${step} (${progress}%)`);

    // Update metadata from backend
    if (metadata.fileName) ui.fileName.textContent = metadata.fileName;
    if (metadata.duration) ui.duration.textContent = metadata.duration;
    if (metadata.resolution) ui.resolution.textContent = metadata.resolution;
    if (metadata.fps) ui.fps.textContent = metadata.fps;
    if (metadata.size) ui.size.textContent = formatBytes(metadata.size);
    if (metadata.scenes !== undefined) ui.detectedScenes.textContent = metadata.scenes;
    if (metadata.frames !== undefined) ui.framesProcessed.textContent = metadata.frames;
    if (metadata.transcriptLength !== undefined) ui.transcriptLength.textContent = metadata.transcriptLength;
    if (metadata.uploadTime) ui.uploadTime.textContent = new Date(parseInt(metadata.uploadTime) * 1000).toLocaleString();

    if (status === "completed") {
      finishProcessing();
      return;
    }

    if (status === "failed") {
      failProcessing(data.error || "Unknown error");
      return;
    }

  } catch (error) {
    appendLog(`Poll error: ${error.message}`);
  }
}

function applyTheme(mode) {
  const isDark = mode === "dark";
  document.documentElement.classList.toggle("dark", isDark);
  document.body.classList.toggle("dark", isDark);
  localStorage.setItem("themePreference", mode);
  ui.themeToggle.innerHTML = isDark
    ? '<span class="material-symbols-outlined text-primary">light_mode</span>'
    : '<span class="material-symbols-outlined text-primary">dark_mode</span>';
}

function initTheme() {
  const savedTheme = localStorage.getItem("themePreference") || "light";
  applyTheme(savedTheme);
}

function initVideoMeta() {
  // Will be updated from backend polling
  ui.fileName.textContent = videoId ? `Video ${videoId.substring(0, 8)}...` : "Unknown";
  ui.duration.textContent = "--:--";
  ui.resolution.textContent = "--";
  ui.fps.textContent = "--";
  ui.size.textContent = "--";
  ui.uploadTime.textContent = new Date().toLocaleString();
  ui.transcriptLength.textContent = "--";
  ui.detectedScenes.textContent = "0";
  ui.framesProcessed.textContent = "0";
}

function lockNavigationWhileProcessing() {
  ui.navItems.forEach((item) => {
    item.classList.add("nav-disabled");
  });
}

function init() {
  ui.footerYear.textContent = new Date().getFullYear();
  initTheme();
  initVideoMeta();
  renderPipeline();
  renderWorkflow();
  updateProgress(0);
  updateCurrentStep(0);
  startTimer();
  appendLog("Upload completed");
  appendLog("Waiting for backend updates...");
  lockNavigationWhileProcessing();

  // Start polling backend every 2 seconds
  if (videoId) {
    pollStatus(); // Initial poll
    pollInterval = setInterval(pollStatus, 2000);
  } else {
    appendLog("ERROR: No video_id in URL. Please upload a video first.");
    ui.currentTask.textContent = "Error: No Video ID";
  }

  ui.cancelBtn.addEventListener("click", cancelProcessing);

  ui.viewResultsBtn.addEventListener("click", () => {
    if (videoId) {
      window.location.href = `/results?video_id=${videoId}`;
    }
  });

  ui.themeToggle.addEventListener("click", () => {
    const nextMode = document.body.classList.contains("dark") ? "light" : "dark";
    applyTheme(nextMode);
  });

  ui.mobileMenuButton.addEventListener("click", () => {
    ui.sidebar.classList.toggle("-translate-x-full");
    ui.sidebarOverlay.classList.toggle("hidden");
  });

  ui.sidebarOverlay.addEventListener("click", () => {
    ui.sidebar.classList.add("-translate-x-full");
    ui.sidebarOverlay.classList.add("hidden");
  });
}

init();