# Plagiarism Checker — BTech CSE Python Mini-Project

A modern, high-precision, 4-page web application for detecting text similarity and potential plagiarism using **Python**, **Flask**, **scikit-learn (TF-IDF Vectorizer)**, and **Cosine Similarity**.

---

## 1. Project Overview

The **Plagiarism Checker** allows students, educators, and researchers to compare two textual documents (either via direct copy-paste or `.txt` file uploads) and calculate an objective, mathematical similarity score.

Unlike basic keyword counters, this application employs **Natural Language Processing (NLP)**:
1. Preprocesses text (lowercasing, symbol normalization).
2. Tokenizes sentences into distinct word tokens.
3. Removes high-frequency English stop-words (`"the"`, `"is"`, `"at"`).
4. Transforms words into multi-dimensional vectors using **TF-IDF** (Term Frequency &ndash; Inverse Document Frequency).
5. Computes the **Cosine of the angle between vectors** to determine directional orientation rather than raw document length.
6. Returns an interactive similarity percentage, categorized as **Low (0&ndash;20%)**, **Moderate (20&ndash;50%)**, or **High (50&ndash;100%)**.

---

## 2. Technology Stack

- **Frontend:**
  - **HTML5:** Semantic document structure, accessible tags, and unique element IDs.
  - **Vanilla CSS3:** Modern dark navy (`#071426`) and cyan (`#12C8D8`) theme, flexbox/grid layouts, responsive breakpoints, and print styles.
  - **Vanilla JavaScript:** Real-time word and character counters, drag-and-drop file readers, one-click demo presets, form validation, and animated circular gauge meters.
- **Backend:**
  - **Python 3:** Core programming language.
  - **Flask:** Lightweight, beginner-friendly WSGI web framework for routing, session handling, and file streaming.
  - **scikit-learn:** `TfidfVectorizer` and `cosine_similarity` for machine learning and NLP calculations.
- **Data Persistence:**
  - In-memory processing. Documents are analyzed on the fly and never permanently stored or logged, ensuring strict academic privacy.

---

## 3. Project Folder Structure

```
plagiarism checker/
├── app.py                  # Main Flask application and similarity engine
├── requirements.txt        # Python dependency declarations
├── README.md               # Documentation and execution instructions
├── templates/              # HTML templates rendered by Jinja2
│   ├── index.html          # Page 1: Home Landing Page
│   ├── checker.html        # Page 2: Plagiarism Checker Working Interface
│   ├── results.html        # Page 3: Comparison Results Dashboard
│   └── how-it-works.html   # Page 4: NLP & Mathematical Pipeline Explanation
└── static/                 # Static web assets
    ├── css/
    │   └── style.css       # Complete responsive styling (Navy & Cyan theme)
    └── js/
        └── script.js       # Real-time counters, file readers, sample loaders
```

---

## 4. Website Pages Overview

1. **Page 1: Home (`/`) &mdash; `index.html`**
   - Clean navigation bar and project brand.
   - Hero banner: *"Detect Text Similarity. Protect Originality."*
   - Feature highlight cards for text comparison, TF-IDF vectorization, and instant cosine similarity.
   - Section covering the importance of checking text similarity in academic institutions.
   - Professional footer with academic credits.

2. **Page 2: Check Plagiarism (`/checker`) &mdash; `checker.html`**
   - Side-by-side comparison panels: **Document A** (Reference) and **Document B** (Suspect).
   - Direct text input with live word, character, and sentence counters.
   - `.txt` file upload button and drag-and-drop file reading.
   - One-click **Quick Demo Presets** (High, Moderate, Low similarity) for quick viva demonstrations.
   - Prominent **"Compare Documents"** button with a loading spinner animation.
   - Clear/Reset buttons and form validation alerts.
   - Disclaimer explaining that similarity does not automatically prove plagiarism.

3. **Page 3: Results (`/results`) &mdash; `results.html`**
   - Dynamic animated circular progress gauge displaying the actual similarity percentage.
   - Categorization badges:
     - **0&ndash;20%:** Low Similarity (Emerald Green)
     - **Above 20&ndash;50%:** Moderate Similarity (Amber Gold)
     - **Above 50&ndash;100%:** High Similarity (Coral Red)
   - Comparative statistics table (word count, characters, sentences, average word length).
   - Top overlapping vocabulary terms identified by TF-IDF feature weights.
   - Side-by-side snippet previews of Document A and Document B.
   - **"Print / Save PDF"** report export button.
   - Empty state prompt if accessed directly without running a comparison.

4. **Page 4: How It Works (`/how-it-works`) &mdash; `how-it-works.html`**
   - Visual 7-step flowchart from raw document input to final percentage.
   - Clear definitions and mathematical formulas for **NLP**, **TF-IDF**, and **Cosine Similarity**.
   - Fully calculated worked viva example comparing two similar sentences:
     - Sentence A: *"Machine learning is fascinating and powerful."*
     - Sentence B: *"Deep learning is powerful and fascinating."*
   - Limitations section explaining domain idioms, citations, and the essential need for human review.

---

## 5. Step-by-Step Installation & Execution Guide

### Prerequisites
- Python 3.8 or higher installed on your computer.

### Step 1: Open Terminal in the Project Directory
```bash
cd "/Users/adityamishra/plagiarism checker"
```

### Step 2: Create and Activate a Python Virtual Environment
```bash
# Create the virtual environment
python3 -m venv venv

# Activate on macOS / Linux:
source venv/bin/activate

# (Or on Windows PowerShell):
# .\venv\Scripts\Activate.ps1
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Run the Flask Web Application
```bash
python3 app.py
```

### Step 5: Open in Your Browser
Visit:
```
http://127.0.0.1:5001
```
*(Or the port displayed in your terminal output).*

---

## 6. How to Explain This Project During Your Viva

When presenting to your external examiner or college professor, follow these key talking points:

### Q1: Why did you use TF-IDF instead of simple word counting?
> **Answer:** Simple word counting treats all words equally. Words like *"the"*, *"is"*, and *"and"* appear very frequently in almost every document, which would falsely inflate similarity scores. **TF-IDF** downweights common words through Inverse Document Frequency and emphasizes unique, topic-specific keywords, providing a much truer assessment of shared content.

### Q2: Why Cosine Similarity instead of Euclidean Distance?
> **Answer:** Euclidean distance measures the geometric distance between two vector endpoints. If Document A is a 5-page chapter and Document B is a 50-page dissertation on the same subject, their Euclidean distance will be very large simply because of document length. **Cosine Similarity** measures the angle between the vectors, evaluating the *direction* rather than magnitude, which makes it invariant to document size.

### Q3: What is the mathematical formula for Cosine Similarity?
> **Answer:** 
> $$\text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$
> Where $\mathbf{A} \cdot \mathbf{B}$ is the dot product of the TF-IDF vectors, and $\|\mathbf{A}\|$ and $\|\mathbf{B}\|$ are the Euclidean norms (lengths) of the vectors.

### Q4: Does a high similarity score automatically mean someone committed plagiarism?
> **Answer:** No. As highlighted on our Results and How-It-Works pages, text similarity only measures mathematical token overlap. Legitimate factors like standard quotations with proper citations, common technical terminology (e.g., *"Object-Oriented Programming"*), and bibliographies can elevate similarity. A qualified human instructor must always inspect the flagged passages.

---

## 7. License & Academic Attribution
Created for BTech Computer Science & Engineering (Mini-Project). Free for educational and learning purposes.
