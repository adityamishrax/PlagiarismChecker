/**
 * Plagiarism Checker - Frontend Interactive Controller
 * Handles real-time word counting, file uploads, sample preloading,
 * input validation, loading indicator states, and gauge animations.
 */

document.addEventListener('DOMContentLoaded', () => {
  initMobileNav();
  initTextCounters();
  initFileUploads();
  initDragAndDrop();
  initSampleLoader();
  initFormValidation();
  initResultsPageAnimations();
});

/* ===================================================================
   1. Mobile Navigation Toggle
   =================================================================== */
function initMobileNav() {
  const toggleBtn = document.getElementById('mobileNavToggle');
  const navMenu = document.getElementById('navMenu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const isOpen = navMenu.classList.contains('open');
      toggleBtn.setAttribute('aria-expanded', isOpen);
    });
  }
}

/* ===================================================================
   2. Live Word, Character, and Sentence Counters
   =================================================================== */
function updateCounts(textareaId, wordsId, charsId, sentencesId) {
  const textarea = document.getElementById(textareaId);
  const wordsEl = document.getElementById(wordsId);
  const charsEl = document.getElementById(charsId);
  const sentencesEl = document.getElementById(sentencesId);

  if (!textarea || !wordsEl || !charsEl) return;

  const text = textarea.value.trim();

  // Character Count
  const charCount = textarea.value.length;
  charsEl.textContent = charCount.toLocaleString();

  // Word Count (regex for unicode / alphanumeric words)
  const words = text ? text.match(/\b\w+\b/g) : null;
  const wordCount = words ? words.length : 0;
  wordsEl.textContent = wordCount.toLocaleString();

  // Sentence Count
  if (sentencesEl) {
    const sentences = text ? text.split(/[.!?]+/).filter(s => s.trim().length > 0) : [];
    sentencesEl.textContent = (wordCount > 0 ? Math.max(1, sentences.length) : 0).toLocaleString();
  }
}

function initTextCounters() {
  const docA = document.getElementById('docA_text');
  const docB = document.getElementById('docB_text');

  if (docA) {
    docA.addEventListener('input', () => {
      updateCounts('docA_text', 'wordsA', 'charsA', 'sentencesA');
    });
    // Run on initial page load if text was prefilled
    updateCounts('docA_text', 'wordsA', 'charsA', 'sentencesA');
  }

  if (docB) {
    docB.addEventListener('input', () => {
      updateCounts('docB_text', 'wordsB', 'charsB', 'sentencesB');
    });
    // Run on initial page load if text was prefilled
    updateCounts('docB_text', 'wordsB', 'charsB', 'sentencesB');
  }
}

/* ===================================================================
   3. File Upload Client-Side Reader (.txt only)
   =================================================================== */
function handleFileSelection(fileInput, targetTextareaId, wordsId, charsId, sentencesId, badgeId) {
  if (!fileInput || !fileInput.files || fileInput.files.length === 0) return;

  const file = fileInput.files[0];

  // Validate extension
  if (!file.name.toLowerCase().endsWith('.txt')) {
    alert(`Invalid file format: "${file.name}". Please upload a plain text (.txt) file.`);
    fileInput.value = '';
    return;
  }

  // Validate file size (2 MB limit)
  if (file.size > 2 * 1024 * 1024) {
    alert(`File is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum allowed size is 2 MB.`);
    fileInput.value = '';
    return;
  }

  const reader = new FileReader();
  reader.onload = (e) => {
    const textarea = document.getElementById(targetTextareaId);
    if (textarea) {
      textarea.value = e.target.result;
      updateCounts(targetTextareaId, wordsId, charsId, sentencesId);

      const badge = document.getElementById(badgeId);
      if (badge) {
        badge.textContent = `Loaded: ${file.name}`;
        badge.style.display = 'inline-block';
      }
    }
  };

  reader.onerror = () => {
    alert(`Error reading file "${file.name}". Please ensure the file is readable.`);
  };

  reader.readAsText(file, 'UTF-8');
}

function initFileUploads() {
  const fileA = document.getElementById('docA_file');
  const fileB = document.getElementById('docB_file');

  if (fileA) {
    fileA.addEventListener('change', () => {
      handleFileSelection(fileA, 'docA_text', 'wordsA', 'charsA', 'sentencesA', 'fileBadgeA');
    });
  }

  if (fileB) {
    fileB.addEventListener('change', () => {
      handleFileSelection(fileB, 'docB_text', 'wordsB', 'charsB', 'sentencesB', 'fileBadgeB');
    });
  }
}

/* ===================================================================
   4. Drag and Drop Support
   =================================================================== */
function initDragAndDrop() {
  const setupDropZone = (textareaId, wordsId, charsId, sentencesId, badgeId) => {
    const textarea = document.getElementById(textareaId);
    if (!textarea) return;

    ['dragenter', 'dragover'].forEach(eventName => {
      textarea.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        textarea.style.borderColor = 'var(--accent)';
      }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
      textarea.addEventListener(eventName, (e) => {
        e.preventDefault();
        e.stopPropagation();
        textarea.style.borderColor = '';
      }, false);
    });

    textarea.addEventListener('drop', (e) => {
      const dt = e.dataTransfer;
      const files = dt.files;
      if (files && files.length > 0) {
        const file = files[0];
        if (!file.name.toLowerCase().endsWith('.txt')) {
          alert('Only .txt text files can be dropped here.');
          return;
        }
        const reader = new FileReader();
        reader.onload = (event) => {
          textarea.value = event.target.result;
          updateCounts(textareaId, wordsId, charsId, sentencesId);
          const badge = document.getElementById(badgeId);
          if (badge) {
            badge.textContent = `Dropped: ${file.name}`;
            badge.style.display = 'inline-block';
          }
        };
        reader.readAsText(file, 'UTF-8');
      }
    });
  };

  setupDropZone('docA_text', 'wordsA', 'charsA', 'sentencesA', 'fileBadgeA');
  setupDropZone('docB_text', 'wordsB', 'charsB', 'sentencesB', 'fileBadgeB');
}

/* ===================================================================
   5. Quick Clear Functions
   =================================================================== */
window.clearDocument = function(targetKey) {
  if (targetKey === 'A' || targetKey === 'both') {
    const docA = document.getElementById('docA_text');
    const fileA = document.getElementById('docA_file');
    const badgeA = document.getElementById('fileBadgeA');
    if (docA) docA.value = '';
    if (fileA) fileA.value = '';
    if (badgeA) badgeA.style.display = 'none';
    updateCounts('docA_text', 'wordsA', 'charsA', 'sentencesA');
  }

  if (targetKey === 'B' || targetKey === 'both') {
    const docB = document.getElementById('docB_text');
    const fileB = document.getElementById('docB_file');
    const badgeB = document.getElementById('fileBadgeB');
    if (docB) docB.value = '';
    if (fileB) fileB.value = '';
    if (badgeB) badgeB.style.display = 'none';
    updateCounts('docB_text', 'wordsB', 'charsB', 'sentencesB');
  }
};

/* ===================================================================
   6. Preset Academic Sample Loader (For Easy College Viva Demo)
   =================================================================== */
function initSampleLoader() {
  const sampleButtons = document.querySelectorAll('[data-sample-type]');
  if (!sampleButtons.length) return;

  sampleButtons.forEach(btn => {
    btn.addEventListener('click', async () => {
      const sampleType = btn.getAttribute('data-sample-type');
      try {
        const response = await fetch(`/api/sample/${sampleType}`);
        if (!response.ok) throw new Error('Network error loading sample');
        const data = await response.json();

        const docA = document.getElementById('docA_text');
        const docB = document.getElementById('docB_text');

        if (docA && docB) {
          docA.value = data.docA;
          docB.value = data.docB;

          updateCounts('docA_text', 'wordsA', 'charsA', 'sentencesA');
          updateCounts('docB_text', 'wordsB', 'charsB', 'sentencesB');

          // Highlight loaded sample
          const feedback = document.getElementById('sampleFeedback');
          if (feedback) {
            feedback.textContent = `Loaded ${data.title}`;
            feedback.style.display = 'block';
            setTimeout(() => { feedback.style.display = 'none'; }, 4000);
          }
        }
      } catch (err) {
        console.error('Error fetching sample text:', err);
      }
    });
  });
}

/* ===================================================================
   7. Form Validation & Loading Indicator
   =================================================================== */
function initFormValidation() {
  const form = document.getElementById('comparisonForm');
  const loadingOverlay = document.getElementById('loadingOverlay');

  if (form) {
    form.addEventListener('submit', (e) => {
      const docA = document.getElementById('docA_text');
      const docB = document.getElementById('docB_text');
      const fileA = document.getElementById('docA_file');
      const fileB = document.getElementById('docB_file');

      const textA = docA ? docA.value.trim() : '';
      const textB = docB ? docB.value.trim() : '';
      const hasFileA = fileA && fileA.files && fileA.files.length > 0;
      const hasFileB = fileB && fileB.files && fileB.files.length > 0;

      // Validation: Document A must not be empty
      if (!textA && !hasFileA) {
        e.preventDefault();
        alert('Please enter or upload content for Document A before comparing.');
        if (docA) docA.focus();
        return false;
      }

      // Validation: Document B must not be empty
      if (!textB && !hasFileB) {
        e.preventDefault();
        alert('Please enter or upload content for Document B before comparing.');
        if (docB) docB.focus();
        return false;
      }

      // Show professional loading indicator during vectorization and comparison
      if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
      }

      return true;
    });
  }
}

/* ===================================================================
   8. Results Page Visual Gauge & Metric Animations
   =================================================================== */
function initResultsPageAnimations() {
  const circlePath = document.getElementById('gaugeCirclePath');
  const percentageEl = document.getElementById('animatedPercentage');

  if (!circlePath || !percentageEl) return;

  const targetPercentage = parseFloat(circlePath.getAttribute('data-target-percentage') || '0');

  // SVG Circle stroke animation: circumference = 2 * PI * r = 2 * PI * 15.9155 ≈ 100
  // Set initial stroke-dasharray to 0, 100
  circlePath.setAttribute('stroke-dasharray', '0, 100');

  // Trigger smooth transition
  setTimeout(() => {
    circlePath.setAttribute('stroke-dasharray', `${targetPercentage}, 100`);
  }, 100);

  // Counter number increment animation
  let currentVal = 0;
  const duration = 1200; // ms
  const frameRate = 30; // updates per sec
  const totalSteps = duration / (1000 / frameRate);
  const stepIncrement = targetPercentage / totalSteps;

  const counterInterval = setInterval(() => {
    currentVal += stepIncrement;
    if (currentVal >= targetPercentage) {
      currentVal = targetPercentage;
      clearInterval(counterInterval);
    }
    percentageEl.textContent = currentVal.toFixed(1) + '%';
  }, 1000 / frameRate);
}

/* ===================================================================
   9. Share & Print Utilities
   =================================================================== */
window.printReport = function() {
  window.print();
};

window.copyReportSummary = function(percentage, status) {
  const summaryText = `Plagiarism Checker Analysis Report\nSimilarity Score: ${percentage}%\nClassification: ${status}\nGenerated by BTech CSE Mini-Project Plagiarism Checker`;

  navigator.clipboard.writeText(summaryText).then(() => {
    const btn = document.getElementById('copySummaryBtn');
    if (btn) {
      const origText = btn.innerHTML;
      btn.innerHTML = '<span>✓ Copied to Clipboard</span>';
      setTimeout(() => { btn.innerHTML = origText; }, 2500);
    }
  }).catch(err => {
    console.error('Clipboard copy failed:', err);
  });
};
