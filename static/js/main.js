// ===== Upload page logic =====
const uploadZone = document.getElementById("upload-zone");
const fileInput = document.getElementById("file-input");
const preview = document.getElementById("preview");
const submitBtn = document.getElementById("submit-btn");
const modeButtons = document.querySelectorAll(".toggle-group button");
const modeHiddenInput = document.getElementById("mode-hidden-input");
const modelSelectWrapper = document.getElementById("model-select-wrapper");

if (uploadZone) {
  uploadZone.addEventListener("click", () => fileInput.click());

  uploadZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    uploadZone.classList.add("dragover");
  });

  uploadZone.addEventListener("dragleave", () => {
    uploadZone.classList.remove("dragover");
  });

  uploadZone.addEventListener("drop", (e) => {
    e.preventDefault();
    uploadZone.classList.remove("dragover");
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      handleFileSelect(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files.length) handleFileSelect(e.target.files[0]);
  });
}

function handleFileSelect(file) {
  if (!file.type.match("image.*")) {
    alert("File harus berupa gambar (PNG/JPG/JPEG).");
    return;
  }
  const reader = new FileReader();
  reader.onload = (e) => {
    preview.src = e.target.result;
    preview.style.display = "block";
  };
  reader.readAsDataURL(file);
  submitBtn.disabled = false;
}

modeButtons.forEach((btn) => {
  btn.addEventListener("click", () => {
    modeButtons.forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    const selectedMode = btn.dataset.mode;
    modeHiddenInput.value = selectedMode;
    modelSelectWrapper.style.display = selectedMode === "single" ? "block" : "none";
  });
});

const uploadForm = document.getElementById("upload-form");
if (uploadForm) {
  uploadForm.addEventListener("submit", () => {
    submitBtn.disabled = true;
    submitBtn.textContent = "Memproses...";
  });
}

// ===== Animasi confidence bar & angka (dipanggil di result.html) =====
function animateConfidenceBars() {
  document.querySelectorAll(".confidence-bar-fill").forEach((bar) => {
    const targetWidth = bar.dataset.value + "%";
    requestAnimationFrame(() => {
      bar.style.width = targetWidth;
    });
  });

  document.querySelectorAll(".confidence-number").forEach((el) => {
    const target = parseFloat(el.dataset.value);
    let current = 0;
    const step = target / 40;
    const interval = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(interval);
      }
      el.textContent = current.toFixed(2) + "%";
    }, 16);
  });
}

document.addEventListener("DOMContentLoaded", () => {
  if (document.querySelector(".confidence-bar-fill")) {
    animateConfidenceBars();
  }
});

// ===== FAQ accordion (dipakai di halaman about) =====
document.querySelectorAll(".faq-question").forEach((question) => {
  question.addEventListener("click", () => {
    const item = question.parentElement;
    const wasOpen = item.classList.contains("open");

    document.querySelectorAll(".faq-item").forEach((i) => i.classList.remove("open"));

    if (!wasOpen) item.classList.add("open");
  });
});