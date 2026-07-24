const allowedTypes = ["video/mp4", "video/avi", "video/quicktime", "video/x-msvideo", "video/x-matroska", "video/mkv"];
const allowedExtensions = [".mp4", ".avi", ".mov", ".mkv"];
const maxFileSize = 2 * 1024 * 1024 * 1024;

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("video-input");
const browseButton = document.getElementById("browse-button");
const selectedPanel = document.getElementById("selected-file-panel");
const processButton = document.getElementById("process-video-btn");
const processingBlock = document.getElementById("processing-block");
const progressFill = document.getElementById("progress-fill");
const progressText = document.getElementById("progress-text");
const pipelineList = document.getElementById("pipeline-list");
const recentVideosList = document.getElementById("recent-videos-list");
const tipsText = document.getElementById("processing-tip");
const footerYear = document.getElementById("footer-year");
const fileNameEl = document.getElementById("file-name");
const fileTypeEl = document.getElementById("file-type");
const fileSizeEl = document.getElementById("file-size");
const fileDateEl = document.getElementById("file-date");
const thumbnailContainer = document.getElementById("thumbnail-container");
const videoPreview = document.getElementById("video-preview");
const currentFileLabel = document.getElementById("current-file-label");
const themeToggle = document.getElementById("theme-toggle");
const mobileMenuButton = document.getElementById("mobile-menu-button");
const sidebar = document.getElementById("sidebar");
const sidebarOverlay = document.getElementById("sidebar-overlay");
const toastContainer = document.getElementById("toast-container");
const clearSelectionButton = document.getElementById("clear-selection");

let selectedFile = null;
let processingInterval = null;
let currentStageIndex = 0;

const stages = [
    "Uploading...",
    "Extracting Audio...",
    "Detecting Scenes...",
    "Generating Descriptions...",
    "Building Embeddings...",
    "Completed"
];

const pipelineSteps = [
    "Upload",
    "Scene Detection",
    "Keyframes",
    "Whisper",
    "SmolVLM",
    "Embeddings",
    "Qdrant",
    "Done"
];

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

function formatDate(date) {
    return new Date(date).toLocaleString([], {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = "max-w-sm rounded-xl border bg-white/90 dark:bg-slate-900/90 px-4 py-3 shadow-lg backdrop-blur text-sm text-slate-800 dark:text-slate-100 toast-enter";
    toast.innerHTML = `<div class="flex items-center gap-2"><span class="material-symbols-outlined text-base">${type === "error" ? "error" : type === "success" ? "check_circle" : "info"}</span><span>${message}</span></div>`;
    toastContainer.appendChild(toast);
    setTimeout(() => toast.remove(), 2800);
}

function getFileExtension(name) {
    return name.slice(name.lastIndexOf(".")).toLowerCase();
}

function validateFile(file) {
    const extension = getFileExtension(file.name);
    const mimeType = file.type || "";

    if (!allowedExtensions.includes(extension) && !allowedTypes.includes(mimeType)) {
        showToast("Unsupported format. Please upload MP4, AVI, MOV, or MKV.", "error");
        return false;
    }

    if (file.size > maxFileSize) {
        showToast("File exceeds 2 GB limit.", "error");
        return false;
    }

    return true;
}

function updateRecentVideos() {
    const videos = JSON.parse(localStorage.getItem("recentVideos") || "[]");
    recentVideosList.innerHTML = "";

    if (!videos.length) {
        recentVideosList.innerHTML = '<div class="text-xs text-slate-500">No uploads yet.</div>';
        return;
    }

    videos.slice(0, 5).forEach((video) => {
        const item = document.createElement("div");
        item.className = "flex items-center gap-sm";
        item.innerHTML = `
            <div class="w-2 h-2 rounded-full bg-primary"></div>
            <span class="font-body-sm text-on-surface truncate max-w-[160px]">${video.name}</span>
            <span class="font-label-upper text-[10px] text-outline ml-auto">${video.time}</span>
        `;
        recentVideosList.appendChild(item);
    });
}

function saveRecentVideo(file) {
    const videos = JSON.parse(localStorage.getItem("recentVideos") || "[]");
    videos.unshift({
        name: file.name,
        time: "just now"
    });
    localStorage.setItem("recentVideos", JSON.stringify(videos.slice(0, 5)));
    updateRecentVideos();
}

function setTheme(mode) {
    document.documentElement.classList.toggle("dark", mode === "dark");
    localStorage.setItem("themePreference", mode);
    themeToggle.innerHTML = mode === "dark"
        ? '<span class="material-symbols-outlined text-primary">light_mode</span>'
        : '<span class="material-symbols-outlined text-primary">dark_mode</span>';
}

function initTheme() {
    const storedTheme = localStorage.getItem("themePreference") || "light";
    setTheme(storedTheme);
}

function resetProcessingUI() {
    clearInterval(processingInterval);
    if (progressFill) progressFill.style.width = "0%";
    if (progressText) progressText.textContent = "0%";
    currentStageIndex = 0;
    if (processingBlock) processingBlock.classList.add("hidden");
    if (processButton) {
        processButton.disabled = !selectedFile;
        processButton.classList.toggle("opacity-50", !selectedFile);
        processButton.classList.toggle("cursor-not-allowed", !selectedFile);
        processButton.innerHTML = '<span class="material-symbols-outlined">auto_awesome</span>Process Video';
    }
    if (pipelineList) {
        pipelineList.querySelectorAll("li").forEach((item, index) => {
            item.classList.remove("done", "pending");
            item.classList.add(index === 0 ? "done" : "pending");
        });
    }
}

function renderPipelineState(stageIndex) {
    if (!pipelineList || !tipsText) return;
    pipelineList.querySelectorAll("li").forEach((item, index) => {
        item.classList.remove("done", "pending");
        if (index < stageIndex) {
            item.classList.add("done");
        } else {
            item.classList.add("pending");
        }
    });
    const activeStage = stageIndex < pipelineSteps.length ? pipelineSteps[stageIndex] : pipelineSteps[pipelineSteps.length - 1];
    tipsText.textContent = activeStage;
}

function startProcessingSimulation() {
    if (!selectedFile || !processButton || !processingBlock || !progressFill || !progressText || !tipsText) return;

    processButton.disabled = true;
    processButton.classList.add("opacity-50", "cursor-not-allowed");
    processButton.innerHTML = '<span class="material-symbols-outlined">sync</span>Processing...';
    processingBlock.classList.remove("hidden");
    currentStageIndex = 0;

    const totalStages = stages.length;
    let percent = 0;

    renderPipelineState(0);
    tipsText.textContent = stages[0];

    processingInterval = setInterval(() => {
        currentStageIndex += 1;
        percent = Math.min(100, Math.round((currentStageIndex / totalStages) * 100));
        progressFill.style.width = `${percent}%`;
        progressText.textContent = `${percent}%`;

        if (currentStageIndex < totalStages) {
            renderPipelineState(currentStageIndex);
            tipsText.textContent = stages[currentStageIndex];
        }

        if (currentStageIndex >= totalStages) {
            clearInterval(processingInterval);
            showToast("Completed Successfully", "success");
            processButton.disabled = false;
            processButton.classList.remove("opacity-50", "cursor-not-allowed");
            processButton.innerHTML = '<span class="material-symbols-outlined">auto_awesome</span>Process Video';
            processingBlock.classList.add("hidden");
            renderPipelineState(pipelineSteps.length - 1);
            tipsText.textContent = "Completed";

            const formData = new FormData();
            formData.append("file", selectedFile);
            fetch("/upload", {
                method: "POST",
                body: formData
            }).catch(() => {
                showToast("Error: /upload is not available until the Flask backend is connected.", "error");
            });
        }
    }, 1400);
}

function updateSelectedFileUI(file) {
    selectedPanel.classList.remove("hidden");
    fileNameEl.textContent = file.name;
    fileTypeEl.textContent = file.type || getFileExtension(file.name).replace(".", "").toUpperCase();
    fileSizeEl.textContent = formatBytes(file.size);
    fileDateEl.textContent = formatDate(file.lastModified);
    currentFileLabel.textContent = file.name;

    processButton.disabled = false;
    processButton.classList.remove("opacity-50", "cursor-not-allowed");
    showToast("Video Uploaded", "success");

    const objectUrl = URL.createObjectURL(file);
    if (videoPreview) {
        videoPreview.src = objectUrl;
        videoPreview.load();
    }

    const video = document.createElement("video");
    video.preload = "metadata";
    video.src = objectUrl;
    video.muted = true;
    video.playsInline = true;

    video.onloadeddata = () => {
        const canvas = document.createElement("canvas");
        const context = canvas.getContext("2d");
        canvas.width = 320;
        canvas.height = 180;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        thumbnailContainer.innerHTML = `<img src="${canvas.toDataURL("image/png")}" class="w-full h-full object-cover" alt="Video thumbnail" />`;
    };

    saveRecentVideo(file);
}

function handleFileSelection(file) {
    if (!file) return;
    if (!validateFile(file)) return;
    selectedFile = file;
    updateSelectedFileUI(file);
}

browseButton.addEventListener("click", () => fileInput.click());
dropZone.addEventListener("click", (event) => {
    if (event.target === videoPreview || event.target.closest("button")) return;
    fileInput.click();
});
fileInput.addEventListener("change", (event) => {
    const [file] = event.target.files;
    handleFileSelection(file);
});

["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.add("drag-active");
    });
});

["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
        event.preventDefault();
        dropZone.classList.remove("drag-active");
    });
});

dropZone.addEventListener("drop", (event) => {
    const [file] = event.dataTransfer.files;
    handleFileSelection(file);
});

processButton.addEventListener("click", () => {
    if (!selectedFile) return;
    showToast("Processing Started", "info");
    startProcessingSimulation();
});

clearSelectionButton.addEventListener("click", () => {
    selectedFile = null;
    fileInput.value = "";
    selectedPanel.classList.add("hidden");
    videoPreview.classList.add("hidden");
    thumbnailContainer.innerHTML = '<div class="absolute inset-0 flex items-center justify-center bg-slate-900/30"><span class="material-symbols-outlined text-on-primary text-xl">movie</span></div>';
    fileNameEl.textContent = "No file selected";
    fileTypeEl.textContent = "-";
    fileSizeEl.textContent = "-";
    fileDateEl.textContent = "-";
    currentFileLabel.textContent = "No file selected";
    resetProcessingUI();
    showToast("Selection cleared", "info");
});

themeToggle.addEventListener("click", () => {
    const isDark = document.documentElement.classList.contains("dark");
    setTheme(isDark ? "light" : "dark");
});

mobileMenuButton.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    sidebarOverlay.classList.toggle("show");
});

sidebarOverlay.addEventListener("click", () => {
    sidebar.classList.remove("open");
    sidebarOverlay.classList.remove("show");
});

processButton.disabled = true;
processButton.classList.add("opacity-50", "cursor-not-allowed");
selectedPanel.classList.add("hidden");
processingBlock.classList.add("hidden");
updateRecentVideos();
footerYear.textContent = new Date().getFullYear();
initTheme();
