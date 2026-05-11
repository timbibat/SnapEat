# SnapEat - Software-Based Food Scanning System

## Project Overview
SnapEat is a comprehensive system that identifies food items, displays nutritional information, health classifications, and provides smart recommendations.

## Team Workflow & Responsibilities

### 1. Frontend Developer (HTML/CSS/JS)
- **Files**: `templates/`, `static/css/`, `static/js/`
- **Tasks**: 
    - Create responsive UI for scanning, dashboard, and logs.
    - Implement QR/Camera scanning logic in `static/js/scanner.js`.
    - Connect UI to backend APIs using `static/js/api.js`.

### 2. Backend Developer (Python/Flask/DB)
- **Files**: `app.py`, `backend/database.py`, `backend/analyzer.py`
- **Tasks**:
    - Manage Flask routes and API endpoints.
    - Handle database operations (Daily Log, Household Mode).
    - Integrate ML model outputs into API responses.

### 3. ML Developer (Machine Learning/Python)
- **Files**: `ml_models/`, `backend/classifier.py`, `backend/recommender.py`
- **Tasks**:
    - Train and export food identification models.
    - Implement health classification (1-10 scoring) logic.
    - Develop the recommendation engine for healthy alternatives.

## Getting Started
1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `python app.py`
3. Deploy: Push to GitHub and connect to Vercel.
