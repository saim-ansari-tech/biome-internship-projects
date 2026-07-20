const pipelineSteps = [
  "Upload Video",
  "Extract Audio",
  "Speech-to-Text (Whisper)",
  "Scene Detection",
  "Keyframe Extraction",
  "Scene Description Generation",
  "Summary Generation",
  "Chapter Generation",
  "Text Chunking",
  "Embedding Generation",
  "Store in Qdrant",
  "Semantic Search Ready"
];

const workflow = [
  "Video",
  "Audio",
  "Whisper",
  "Transcript",
  "Chunks",
  "Embeddings",
  "Qdrant",
  "Ready"
];

const stepStates = new Map();
pipelineSteps.forEach((step, index) => {
  const state = index === 0 ? "running" : index < 2 ? "completed" : "pending";
  stepStates.set(step, state);
});

const stateColors = {
  pending: "bg-slate-100 text-slate-500",
  running: "bg-blue-100 text-blue-700",
  completed: "bg-emerald-100 text-emerald-700",
  failed: "bg-rose-100 text-rose-700"
};

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

let progressValue = 0;
let currentStepIndex = 0;
let timerSeconds = 0;
let timerInterval = null;
let processingStarted = true;
let stageSequence = [
  "Uploading video",
  "Extracting audio",
  "Running Whisper",
  "Detecting scenes",
  "Extracting keyframes",
  "Generating scene descriptions",
  "Generating summary",
  "Generating chapters",
  "Chunking text",
  "Generating embeddings",
  "Storing vectors in Qdrant",
  "Semantic search ready"
];

function formatTime(totalSeconds) {
  const hrs = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const mins = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const secs = String(totalSeconds % 60).padStart(2, "0");
  return `${hrs}:${mins}:${secs}`;
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

function updateCurrentStep(step) {
  currentStepIndex = pipelineSteps.indexOf(step);
  const stepText = step || pipelineSteps[0];
  ui.currentTask.textContent = stepText;
  renderPipeline();
  renderWorkflow();
}

function renderPipeline() {
  ui.stepList.innerHTML = "";

  pipelineSteps.forEach((step, index) => {
    const state = stepStates.get(step) || "pending";
    const item = document.createElement("div");
    item.className = `step-item flex items-center gap-md p-sm rounded-lg border ${state === "running" ? "running" : state === "completed" ? "completed" : state === "failed" ? "failed" : "pending"}`;

    let icon = "pending";
    let label = step;
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
        <p class="font-body-base text-body-base font-semibold">${label}</p>
        <p class="font-body-sm text-body-sm ${state === "completed" ? "text-emerald-700" : state === "running" ? "text-blue-700" : state === "failed" ? "text-rose-700" : "text-slate-500"}">${meta}</p>
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
  line.textContent = message;
  ui.logContainer.appendChild(line);
  ui.logContainer.scrollTop = ui.logContainer.scrollHeight;

  while (ui.logContainer.children.length > 8) {
    ui.logContainer.removeChild(ui.logContainer.firstChild);
  }
}

function completeStep(step) {
  if (stepStates.has(step)) stepStates.set(step, "completed");
  if (pipelineSteps.indexOf(step) > currentStepIndex) currentStepIndex = pipelineSteps.indexOf(step);
  renderPipeline();
}

function failStep(step) {
  if (stepStates.has(step)) stepStates.set(step, "failed");
  renderPipeline();
}

function updateCurrentTaskText(step) {
  ui.currentTask.textContent = step;
}

function finishProcessing() {
  clearInterval(timerInterval);
  updateProgress(100);
  completeStep("Semantic Search Ready");
  ui.cancelBtn.classList.add("hidden");
  ui.completionCard.classList.remove("hidden");
  ui.viewResultsBtn.classList.remove("hidden");
  appendLog("[INFO] Processing completed successfully");
}

function cancelProcessing() {
  const confirmed = window.confirm("Are you sure?");
  if (!confirmed) return;
  clearInterval(timerInterval);
  window.location.href = "../dashboard_1/index.html";
}

function startTimer() {
  timerInterval = setInterval(() => {
    timerSeconds += 1;
    ui.elapsedTime.textContent = formatTime(timerSeconds);
    ui.remainingTime.textContent = formatTime(Math.max(0, 120 - timerSeconds));
  }, 1000);
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
  const metadata = {
    fileName: "sample.mp4",
    duration: "00:02:30",
    resolution: "1920x1080",
    fps: "30",
    size: "245 MB",
    uploadTime: new Date().toLocaleString(),
    transcriptLength: "1340 chars"
  };

  ui.fileName.textContent = metadata.fileName;
  ui.duration.textContent = metadata.duration;
  ui.resolution.textContent = metadata.resolution;
  ui.fps.textContent = metadata.fps;
  ui.size.textContent = metadata.size;
  ui.uploadTime.textContent = metadata.uploadTime;
  ui.transcriptLength.textContent = metadata.transcriptLength;
}

function lockNavigationWhileProcessing() {
  ui.navItems.forEach((item) => {
    item.classList.add("nav-disabled");
  });
}

function setCurrentStepByIndex(index) {
  const step = pipelineSteps[index] || pipelineSteps[0];
  stepStates.set(step, "running");
  renderPipeline();
  updateCurrentStep(step);
}

function init() {
  ui.footerYear.textContent = new Date().getFullYear();
  initTheme();
  initVideoMeta();
  renderPipeline();
  renderWorkflow();
  updateProgress(0);
  updateCurrentStep("Upload Video");
  startTimer();
  appendLog("[INFO] Upload completed");
  appendLog("[INFO] Waiting for backend updates...");
  lockNavigationWhileProcessing();

  ui.cancelBtn.addEventListener("click", cancelProcessing);
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
