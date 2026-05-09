from flask import Flask, render_template, request, jsonify
import os

# Initialize Flask app
# Vercel looks for 'app' as the entry point
app = Flask(__name__)

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/scan')
def scan():
    """QR/Manual scan interface."""
    return render_template('scan.html')

@app.route('/analysis')
def analysis():
    """Analysis Results page."""
    return render_template('analysisResults.html')

@app.route('/api/food/identify', methods=['POST'])
def identify_food():
    """
    Endpoint for identifying food from image/QR data.
    To be handled by the ML Developer.
    """
    return jsonify({"status": "success", "message": "Endpoint for food identification"})

@app.route('/api/food/details/<food_id>')
def food_details(food_id):
    """
    Retrieve nutritional info and health classification.
    To be handled by the Backend Developer.
    """
    return jsonify({"status": "success", "food_id": food_id})

if __name__ == '__main__':
    app.run(debug=True)
