"""
Automated Test Suite for Plagiarism Checker Web Application
Verifies all 4 routes, TF-IDF calculation, file uploads, edge cases, and session state.
"""

import unittest
import io
from app import app, calculate_plagiarism, compute_text_statistics

class PlagiarismCheckerTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client with testing mode and session cookies enabled."""
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'test-secret-key-123'
        self.client = app.test_client()

    def test_page_1_index_route(self):
        """Verify Page 1 (Home) renders correctly with 200 status."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Detect Text Similarity", html)
        self.assertIn("Protect Originality", html)
        self.assertIn("Check Plagiarism", html)
        self.assertIn("How It Works", html)

    def test_page_2_checker_route(self):
        """Verify Page 2 (Checker) renders with both panels and counters."""
        response = self.client.get('/checker')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Document A", html)
        self.assertIn("Document B", html)
        self.assertIn("docA_text", html)
        self.assertIn("docB_text", html)
        self.assertIn("Compare Documents", html)

    def test_page_3_results_empty_state(self):
        """Verify Page 3 (Results) displays an informative empty state when opened directly."""
        response = self.client.get('/results')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("No Document Comparison Data Found", html)
        self.assertIn("Go to Plagiarism Checker", html)

    def test_page_4_how_it_works_route(self):
        """Verify Page 4 (How It Works) renders the 7-step pipeline and math definitions."""
        response = self.client.get('/how-it-works')
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("The 7-Step Detection Pipeline", html)
        self.assertIn("TF-IDF Vectorization", html)
        self.assertIn("Cosine Similarity", html)
        self.assertIn("Machine learning is fascinating and powerful", html)

    def test_algorithm_identical_documents(self):
        """Verify that identical documents return exactly 100.0% similarity."""
        text = "Operating systems manage hardware resources and provide common services for application software."
        res = calculate_plagiarism(text, text)
        self.assertEqual(res['similarity_percentage'], 100.0)
        self.assertEqual(res['status_category'], 'high')

    def test_algorithm_completely_different_documents(self):
        """Verify that completely different documents return low similarity."""
        docA = "Relational database tables utilize structured query language for relational integrity."
        docB = "Photosynthesis in green plants converts sunlight into organic chemical energy."
        res = calculate_plagiarism(docA, docB)
        self.assertLessEqual(res['similarity_percentage'], 20.0)
        self.assertEqual(res['status_category'], 'low')

    def test_compare_form_submission_and_results(self):
        """Verify that submitting text via POST /compare calculates similarity and redirects to /results."""
        docA = "Cloud computing delivers virtual servers, databases, and networking over the internet."
        docB = "Cloud computing provides virtualized servers, storage, and networking across the internet."
        
        response = self.client.post('/compare', data={
            'docA_text': docA,
            'docB_text': docB
        }, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Similarity Analysis Report", html)
        self.assertIn("Cosine Match", html)
        self.assertIn("Total Word Count", html)

    def test_compare_file_upload(self):
        """Verify that uploading .txt files works seamlessly."""
        file_a_content = io.BytesIO(b"Data structures organize information efficiently in computer memory.")
        file_b_content = io.BytesIO(b"Algorithms process data structures efficiently to solve computational problems.")

        response = self.client.post('/compare', data={
            'docA_text': '',
            'docB_text': '',
            'docA_file': (file_a_content, 'sampleA.txt'),
            'docB_file': (file_b_content, 'sampleB.txt')
        }, content_type='multipart/form-data', follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Similarity Analysis Report", html)

    def test_api_sample_endpoints(self):
        """Verify the sample text APIs for quick college viva demonstration."""
        for sample_type in ['high', 'moderate', 'low']:
            res = self.client.get(f'/api/sample/{sample_type}')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertIn('docA', data)
            self.assertIn('docB', data)

    def test_empty_input_validation(self):
        """Verify empty input redirects back with flash error."""
        response = self.client.post('/compare', data={
            'docA_text': '',
            'docB_text': ''
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        html = response.data.decode('utf-8')
        self.assertIn("Please provide content for both Document A and Document B", html)

if __name__ == '__main__':
    unittest.main()
