"""
Plagiarism Checker - BTech CSE Mini-Project
Backend Application powered by Flask, TF-IDF Vectorization, and Cosine Similarity.
"""

import os
import re
import time
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize the Flask application
app = Flask(__name__)

# Secret key required for Flask session management and flash messages
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "plagiarism_checker_cse_project_secret_key_2026")

# Maximum upload file size: 2 Megabytes (sufficient for standard text documents)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2 MB limit
ALLOWED_EXTENSIONS = {'txt'}


def is_allowed_file(filename):
    """Check if the uploaded file has a permitted extension (.txt)."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def compute_text_statistics(text):
    """
    Compute basic descriptive text metrics:
    - Word count
    - Character count (with & without whitespace)
    - Sentence count
    - Average word length
    """
    cleaned = text.strip()
    if not cleaned:
        return {
            'word_count': 0,
            'char_count': 0,
            'char_no_space': 0,
            'sentence_count': 0,
            'avg_word_length': 0.0
        }

    words = re.findall(r'\b\w+\b', cleaned)
    word_count = len(words)
    char_count = len(cleaned)
    char_no_space = len(re.sub(r'\s+', '', cleaned))

    # Sentence splitting by period, exclamation, or question mark
    sentences = [s for s in re.split(r'[.!?]+', cleaned) if s.strip()]
    sentence_count = max(1, len(sentences)) if word_count > 0 else 0

    total_letters = sum(len(w) for w in words)
    avg_word_length = round(total_letters / word_count, 1) if word_count > 0 else 0.0

    return {
        'word_count': word_count,
        'char_count': char_count,
        'char_no_space': char_no_space,
        'sentence_count': sentence_count,
        'avg_word_length': avg_word_length
    }


def calculate_plagiarism(doc_a, doc_b):
    """
    Core Plagiarism Detection Algorithm:
    1. Normalizes text inputs.
    2. Generates TF-IDF (Term Frequency - Inverse Document Frequency) matrices.
    3. Calculates Cosine Similarity between the two document vectors.
    4. Identifies top overlapping vocabulary terms.
    5. Returns similarity percentage and categorization.
    """
    start_time = time.time()

    clean_a = doc_a.strip()
    clean_b = doc_b.strip()

    shared_terms = []

    # Exact match check
    if clean_a.lower() == clean_b.lower():
        similarity_score = 1.0
        percentage = 100.0
        words = re.findall(r'\b\w+\b', clean_a.lower())
        unique_words = list(dict.fromkeys(words))[:15]
        shared_terms = [{'term': w, 'weight': 1.0} for w in unique_words]
    else:
        try:
            # 1. Initialize TfidfVectorizer with standard English stop words removal
            vectorizer = TfidfVectorizer(
                stop_words='english',
                token_pattern=r'(?u)\b\w+\b',
                lowercase=True
            )
            # Fit and transform the two documents into numerical TF-IDF feature vectors
            tfidf_matrix = vectorizer.fit_transform([clean_a, clean_b])

            # Calculate Cosine Similarity between vector A (row 0) and vector B (row 1)
            # Cosine Similarity = (A . B) / (||A|| * ||B||)
            sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
            similarity_score = float(sim_matrix[0][0])
            percentage = round(similarity_score * 100, 2)

            # Extract overlapping keywords that contributed to similarity
            feature_names = vectorizer.get_feature_names_out()
            row_a = tfidf_matrix[0].toarray()[0]
            row_b = tfidf_matrix[1].toarray()[0]

            shared_terms = []
            for idx, feature in enumerate(feature_names):
                weight_a = row_a[idx]
                weight_b = row_b[idx]
                if weight_a > 0 and weight_b > 0:
                    # Combined relevance score
                    relevance = weight_a * weight_b
                    shared_terms.append({
                        'term': feature,
                        'weight': round(float(relevance), 4)
                    })

            # Sort shared terms by combined TF-IDF importance
            shared_terms = sorted(shared_terms, key=lambda x: x['weight'], reverse=True)[:15]

        except ValueError:
            # Fallback if text contains only stop words or symbols
            try:
                # Attempt vectorization without stop word removal
                vectorizer_fallback = TfidfVectorizer(
                    lowercase=True,
                    token_pattern=r'(?u)\b\w+\b'
                )
                tfidf_matrix = vectorizer_fallback.fit_transform([clean_a, clean_b])
                sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
                similarity_score = float(sim_matrix[0][0])
                percentage = round(similarity_score * 100, 2)
                shared_terms = []
            except Exception:
                # If both documents have zero alphanumeric words
                similarity_score = 0.0
                percentage = 0.0
                shared_terms = []

    # Clamp percentage to [0, 100]
    percentage = max(0.0, min(100.0, percentage))

    # Categorize the similarity level based on specified thresholds
    if percentage <= 20.0:
        status = "Low Similarity"
        status_category = "low"
        status_color = "#10B981"  # Emerald Green
        status_description = (
            "The two documents show minimal lexical and structural overlap. "
            "Any matched tokens represent common language conventions rather than copied substance."
        )
    elif percentage <= 50.0:
        status = "Moderate Similarity"
        status_category = "moderate"
        status_color = "#F59E0B"  # Amber Orange
        status_description = (
            "Notable lexical and conceptual overlap detected. This may arise from shared subject matter, "
            "standard quotes, common terminology, or partial paraphrasing. Review matches manually."
        )
    else:
        status = "High Similarity"
        status_category = "high"
        status_color = "#EF4444"  # Coral Red
        status_description = (
            "Significant textual and structural convergence detected. A large portion of vocabulary, "
            "phrasing, and sequence closely matches Document A. Detailed academic inspection recommended."
        )

    # Compute execution time
    elapsed_ms = round((time.time() - start_time) * 1000, 1)

    # Calculate individual statistics
    stats_a = compute_text_statistics(clean_a)
    stats_b = compute_text_statistics(clean_b)

    return {
        'similarity_percentage': percentage,
        'similarity_score': round(similarity_score, 4),
        'status': status,
        'status_category': status_category,
        'status_color': status_color,
        'status_description': status_description,
        'shared_terms': shared_terms,
        'stats_a': stats_a,
        'stats_b': stats_b,
        'elapsed_ms': elapsed_ms,
        'sample_a_snippet': clean_a[:500] + ('...' if len(clean_a) > 500 else ''),
        'sample_b_snippet': clean_b[:500] + ('...' if len(clean_b) > 500 else '')
    }


# ==========================================
# FLASK ROUTE DEFINITIONS
# ==========================================

@app.route('/')
def index():
    """Page 1: Home Landing Page."""
    return render_template('index.html', active_page='home')


@app.route('/checker')
def checker():
    """Page 2: Plagiarism Checker Working Interface."""
    return render_template('checker.html', active_page='checker')


@app.route('/compare', methods=['POST'])
def compare():
    """
    Document Comparison Processing Endpoint.
    Accepts text inputs or .txt file uploads, calculates similarity,
    stores results in session, and redirects to the results page.
    """
    doc_a = request.form.get('docA_text', '').strip()
    doc_b = request.form.get('docB_text', '').strip()

    # Handle Document A File Upload if provided
    file_a = request.files.get('docA_file')
    if file_a and file_a.filename:
        if not is_allowed_file(file_a.filename):
            flash("Document A: Only .txt files are supported.", "error")
            return redirect(url_for('checker'))
        try:
            # Read file in-memory without permanently storing on disk
            doc_a = file_a.read().decode('utf-8', errors='replace').strip()
        except Exception:
            flash("Document A: Could not read file content. Please ensure it is valid text.", "error")
            return redirect(url_for('checker'))

    # Handle Document B File Upload if provided
    file_b = request.files.get('docB_file')
    if file_b and file_b.filename:
        if not is_allowed_file(file_b.filename):
            flash("Document B: Only .txt files are supported.", "error")
            return redirect(url_for('checker'))
        try:
            # Read file in-memory without permanently storing on disk
            doc_b = file_b.read().decode('utf-8', errors='replace').strip()
        except Exception:
            flash("Document B: Could not read file content. Please ensure it is valid text.", "error")
            return redirect(url_for('checker'))

    # Input Validation: Both documents must have non-empty content
    if not doc_a or not doc_b:
        flash("Please provide content for both Document A and Document B before comparing.", "error")
        return redirect(url_for('checker'))

    if len(re.findall(r'\b\w+\b', doc_a)) == 0 or len(re.findall(r'\b\w+\b', doc_b)) == 0:
        flash("Both documents must contain at least one readable word or token.", "error")
        return redirect(url_for('checker'))

    # Perform TF-IDF and Cosine Similarity calculation
    result_data = calculate_plagiarism(doc_a, doc_b)

    # Store results in the session for secure retrieval on results page
    session['plagiarism_result'] = result_data

    return redirect(url_for('results'))


@app.route('/results')
def results():
    """
    Page 3: Comparison Results Dashboard.
    Reads comparison data from the session. If accessed without comparing,
    renders an informative empty state.
    """
    result_data = session.get('plagiarism_result')
    has_data = result_data is not None

    return render_template(
        'results.html',
        active_page='results',
        has_data=has_data,
        result=result_data or {}
    )


@app.route('/how-it-works')
def how_it_works():
    """Page 4: Algorithm & Mathematical Methodology Explanation."""
    return render_template('how-it-works.html', active_page='how_it_works')


@app.route('/clear-results')
def clear_results():
    """Clear session data and redirect to the checker page."""
    session.pop('plagiarism_result', None)
    return redirect(url_for('checker'))


# ==========================================
# REST API ENDPOINTS (FOR AJAX OR TESTING)
# ==========================================

@app.route('/api/compare', methods=['POST'])
def api_compare():
    """
    REST API endpoint to allow asynchronous comparison via JavaScript fetch().
    """
    data = request.get_json(silent=True) or {}
    doc_a = data.get('docA', '').strip()
    doc_b = data.get('docB', '').strip()

    if not doc_a or not doc_b:
        return jsonify({
            'success': False,
            'error': 'Both docA and docB are required and cannot be empty.'
        }), 400

    results_data = calculate_plagiarism(doc_a, doc_b)
    session['plagiarism_result'] = results_data

    return jsonify({
        'success': True,
        'data': results_data
    })


@app.route('/api/sample/<sample_type>')
def get_sample_texts(sample_type):
    """
    Helper API providing preset academic samples for live demonstration
    during college project viva.
    """
    samples = {
        'high': {
            'title': 'High Similarity Case (Verbatim & Paraphrased)',
            'docA': (
                "Artificial intelligence and machine learning are revolutionizing software development. "
                "Algorithms analyze enormous datasets to identify statistical patterns and make automated decisions. "
                "Supervised learning trains models on labeled ground truth data, while unsupervised learning discovers "
                "hidden patterns within unlabeled data clusters. Deep neural networks use multiple layers of nodes to "
                "extract abstract representations."
            ),
            'docB': (
                "Artificial intelligence and machine learning are transforming software development today. "
                "Algorithms examine massive datasets to detect statistical patterns and generate automated decisions. "
                "Supervised learning trains predictive models on labeled training data, whereas unsupervised learning "
                "identifies hidden structures in unlabeled clusters. Deep neural networks employ multiple layers to "
                "extract abstract features."
            )
        },
        'moderate': {
            'title': 'Moderate Similarity Case (Shared Subject with Distinct Phrasing)',
            'docA': (
                "Cloud computing provides on-demand access to computer system resources, especially data storage "
                "and computational power, without direct active management by the user. Major cloud deployment models "
                "include public cloud, private cloud, and hybrid cloud architectures. Security in the cloud requires "
                "robust encryption, identity access management, and regular compliance auditing."
            ),
            'docB': (
                "Modern distributed systems utilize cloud computing infrastructure to scale microservices globally. "
                "Engineers configure container orchestration platforms such as Kubernetes to balance high incoming "
                "traffic. While public clouds offer rapid deployment and lower hardware expenditures, hybrid cloud models "
                "enable enterprises to maintain strict regulatory compliance and safeguard sensitive customer records."
            )
        },
        'low': {
            'title': 'Low Similarity Case (Two Different Computer Science Disciplines)',
            'docA': (
                "Relational database management systems organize data into structured tables comprising rows and columns. "
                "Structured Query Language, commonly known as SQL, enables developers to execute complex joins, perform "
                "acid transactions, and maintain referential integrity through foreign keys across relational schemas."
            ),
            'docB': (
                "Mobile app development for Android involves building user interfaces using Kotlin and Jetpack Compose. "
                "Developers manage application lifecycles, handle asynchronous coroutines for network requests, and "
                "optimize touch gestures for high refresh rate touchscreen displays."
            )
        }
    }

    sample = samples.get(sample_type.lower())
    if not sample:
        return jsonify({'error': 'Sample type not found. Use high, moderate, or low.'}), 404

    return jsonify(sample)


# Error Handlers
@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle files exceeding maximum allowed size."""
    flash("Uploaded file exceeds the maximum permitted limit of 2MB.", "error")
    return redirect(url_for('checker'))


@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 Not Found error."""
    return render_template('index.html', error_msg="The requested page does not exist."), 404


if __name__ == '__main__':
    # Run development server on port 5001 for local testing
    port = int(os.environ.get('PORT', 5001))
    print(f"Starting Plagiarism Checker on http://127.0.0.1:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)
