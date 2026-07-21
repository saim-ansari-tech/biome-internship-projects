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

function updateRecentVideos(videos) {
    recentVideosList.innerHTML = "";

    if (!videos || !videos.length) {
        recentVideosList.innerHTML = '<div class="text-xs text-slate-500">No processed videos yet. Upload one!</div>';
        return;
    }

    videos.slice(0, 5).forEach((video) => {
        const item = document.createElement("div");
        item.className = "flex items-center gap-sm cursor-pointer hover:bg-surface-container-high p-2 rounded-lg transition-all";
        item.onclick = () => window.location.href = `/results?video_id=${video.video_id}`;
        item.innerHTML = `
            <div class="w-2 h-2 rounded-full bg-primary"></div>
            <span class="font-body-sm text-on-surface truncate max-w-[160px]">${video.video_filename}</span>
            <span class="font-label-upper text-[10px] text-outline ml-auto">${video.summary ? video.summary.substring(0, 30) + '...' : 'Processed'}</span>
        `;
        recentVideosList.appendChild(item);
    });
}

async function loadProcessedVideos() {
    try {
        const response = await fetch('/videos');
        const data = await response.json();
        if (data.success && data.videos) {
            updateRecentVideos(data.videos);
        }
    } catch (error) {
        console.error("Failed to load videos:", error);
        recentVideosList.innerHTML = '<div class="text-xs text-slate-500">Could not load videos.</div>';
    }
}

function renderPipelineState(completedSteps) {
    if (!pipelineList) return;
    pipelineList.querySelectorAll("li").forEach((item, index) => {
        item.classList.remove("done", "pending");
        if (index < completedSteps) {
            item.classList.add("done");
        } else {
            item.classList.add("pending");
        }
    });
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
    showToast("Video selected", "success");

    const objectUrl = URL.createObjectURL(file);
    if (videoPreview) {
        videoPreview.src = objectUrl;
        videoPreview.classList.remove("hidden");
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
}

function handleFileSelection(file) {
    if (!file) return;
    if (!validateFile(file)) return;
    selectedFile = file;
    updateSelectedFileUI(file);
}

async function startProcessing() {
    if (!selectedFile) {
        showToast("Please select a video first.", "error");
        return;
    }

    processButton.disabled = true;
    processButton.classList.add("opacity-50", "cursor-not-allowed");
    processButton.innerHTML = '<span class="material-symbols-outlined">sync</span>Uploading...';
    processingBlock.classList.remove("hidden");
    tipsText.textContent = "Uploading video...";
    progressFill.style.width = "10%";
    progressText.textContent = "10%";
    renderPipelineState(1);

    const formData = new FormData();
    formData.append("video", selectedFile);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.error || "Upload failed.");
        }

        // Upload successful, processing started in background
        progressFill.style.width = "100%";
        progressText.textContent = "100%";
        tipsText.textContent = "Upload complete! Redirecting...";
        showToast("Upload successful! Processing started.", "success");

        // Redirect to processing page with video_id
        setTimeout(() => {
            window.location.href = `/processing?video_id=${result.video_id}`;
        }, 1000);

    } catch (error) {
        console.error("Upload error:", error);
        showToast(error.message || "Something went wrong.", "error");
        processButton.disabled = false;
        processButton.classList.remove("opacity-50", "cursor-not-allowed");
        processButton.innerHTML = '<span class="material-symbols-outlined">auto_awesome</span>Process Video';
        processingBlock.classList.add("hidden");
    }
}

function resetUI() {
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
    processButton.disabled = true;
    processButton.classList.add("opacity-50", "cursor-not-allowed");
    processButton.innerHTML = '<span class="material-symbols-outlined">auto_awesome</span>Process Video';
    processingBlock.classList.add("hidden");
    renderPipelineState(0);
    showToast("Selection cleared", "info");
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

// Event Listeners
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

processButton.addEventListener("click", startProcessing);

clearSelectionButton.addEventListener("click", resetUI);

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

// Initialize
processButton.disabled = true;
processButton.classList.add("opacity-50", "cursor-not-allowed");
selectedPanel.classList.add("hidden");
processingBlock.classList.add("hidden");
footerYear.textContent = new Date().getFullYear();
initTheme();
loadProcessedVideos();