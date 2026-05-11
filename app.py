from flask import Flask, render_template, request, jsonify, session
import os

from backend.analyzer import identify_food_item, get_nutrition_data, search_food_items, get_available_foods
from backend.classifier import classify_health_status, calculate_health_score, get_full_classification
from backend.recommender import get_recommendations, get_household_suggestions
from backend.database import save_food_log, get_daily_log, get_daily_totals, get_weekly_summary, get_recent_scans, register_user, authenticate_user, reset_password
from backend.food_dataset import get_food_by_name

# Initialize Flask app
# Vercel looks for 'app' as the entry point
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'snapeat_secret_key_123')

# ── Page Routes ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """Main dashboard page."""
    username = session.get('user_name', '')
    return render_template('index.html', username=username)

@app.route('/scan')
def scan():
    """QR/Manual scan interface."""
    return render_template('scanFood.html')

@app.route('/login')
def login():
    """Login page."""
    return render_template('loginPage.html')

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return render_template('loginPage.html')

@app.route('/signup')
def signup():
    """Signup page."""
    return render_template('signupPage.html')

@app.route('/forgot-password')
def forgot_password():
    """Forgot password page."""
    return render_template('forgotPassword.html')

@app.route('/history')
def history():
    """History Log page."""
    return render_template('historyLog.html')

@app.route('/reports')
def reports():
    """Health Reports page."""
    return render_template('healthReports.html')

@app.route('/analysis')
def analysis():
    """Analysis Results page (static demo)."""
    return render_template('analysisResults.html')

@app.route('/analysis/<food_name>')
def analysis_result(food_name):
    """Analysis Results page for a specific food item."""
    food = get_food_by_name(food_name)
    if food:
        nutrition = food["nutrition"]
        classification = get_full_classification(food_name)
        recommendations = get_recommendations(food_name)
        return render_template('analysisResults.html',
                               food=food,
                               classification=classification,
                               recommendations=recommendations)
    return render_template('analysisResults.html')

# ── API Routes ───────────────────────────────────────────────────────────────

@app.route('/api/auth/signup', methods=['POST'])
def api_signup():
    """Handle user registration."""
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    if register_user(name, email, password):
        return jsonify({"status": "success", "message": "User registered successfully"})
    else:
        return jsonify({"status": "error", "message": "Email already registered"}), 409

@app.route('/api/auth/login', methods=['POST'])
def api_login():
    """Handle user authentication."""
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = authenticate_user(email, password)
    if user:
        session['user_name'] = user['name']
        session['user_email'] = user['email']
        return jsonify({"status": "success", "user": {"name": user['name'], "email": user['email']}})
    else:
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

@app.route('/api/auth/forgot-password', methods=['POST'])
def api_forgot_password():
    """Handle password reset request."""
    data = request.json
    email = data.get('email')

    if reset_password(email):
        return jsonify({"status": "success", "message": "Reset link sent"})
    else:
        return jsonify({"status": "error", "message": "Email not found"}), 404

@app.route('/api/food/identify', methods=['POST'])
def identify_food():
    """
    Endpoint for identifying food from image/text data.
    Accepts JSON body with 'food_name' or multipart form with 'food_image'.
    """
    food_name = None
    image_data = None

    if request.is_json:
        food_name = request.json.get('food_name')
    else:
        food_name = request.form.get('food_name')
        if 'food_image' in request.files:
            file = request.files['food_image']
            if file and file.filename != '':
                image_data = file.read()

    # If we have neither name nor image, we can't do anything
    if not food_name and not image_data:
        return jsonify({
            "status": "error",
            "message": "Please provide a food name or upload an image.",
            "available_foods": get_available_foods()
        }), 400

    # Call identification with both name and image data
    result = identify_food_item(image_data=image_data, food_name=food_name)

    if result and result["status"] == "identified":
        food = result["food"]
        nutrition = food["nutrition"]
        health_status = classify_health_status(nutrition)
        health_score = calculate_health_score(nutrition)

        # Save to log
        log_entry = {
            "name": food["name"],
            "category": food["category"],
            "nutrition": nutrition,
            "health_status": health_status,
            "health_score": health_score
        }
        log_id = save_food_log("default", log_entry)

        return jsonify({
            "status": "success",
            "food_id": food["name"].lower().replace(" ", "_"),
            "food_name": food["name"],
            "log_id": log_id
        })

    return jsonify({
        "status": "error",
        "message": f"Food '{food_name}' not found in database.",
        "available_foods": get_available_foods()
    }), 404


@app.route('/api/food/details/<food_id>')
def food_details(food_id):
    """
    Retrieve full nutritional info, health classification,
    and recommendations for a food item.
    """
    food = get_food_by_name(food_id)

    if not food:
        return jsonify({
            "status": "error",
            "message": f"Food '{food_id}' not found.",
            "available_foods": get_available_foods()
        }), 404

    nutrition = food["nutrition"]
    health_status = classify_health_status(nutrition)
    health_score = calculate_health_score(nutrition)
    recommendations = get_recommendations(food_id, health_status)

    return jsonify({
        "status": "success",
        "food": {
            "name": food["name"],
            "category": food["category"],
            "image_url": food.get("image_url", ""),
            "nutrition": nutrition,
            "health_status": health_status,
            "health_score": health_score,
            "health_benefits": food["health_benefits"],
            "age_sensitivity": food.get("age_sensitivity", {}),
            "recommendations": recommendations
        }
    })


@app.route('/api/food/search')
def food_search():
    """Search for food items by name or category."""
    query = request.args.get('q', '')
    if not query:
        return jsonify({
            "status": "error",
            "message": "Provide a search query with ?q=",
            "available_foods": get_available_foods()
        }), 400

    results = search_food_items(query)
    return jsonify({"status": "success", "results": results, "count": len(results)})


@app.route('/api/food/list')
def food_list():
    """List all available food items in the dataset."""
    return jsonify({"status": "success", "foods": get_available_foods()})


@app.route('/api/user/log', methods=['GET'])
def user_log():
    """Get the daily food log for the current user."""
    user_id = request.args.get('user_id', 'default')
    date = request.args.get('date', None)

    log = get_daily_log(user_id, date)
    totals = get_daily_totals(user_id, date)

    return jsonify({"status": "success", "log": log, "totals": totals})


@app.route('/api/user/weekly')
def user_weekly():
    """Get the weekly summary for the current user."""
    user_id = request.args.get('user_id', 'default')
    summary = get_weekly_summary(user_id)
    return jsonify({"status": "success", "summary": summary})


@app.route('/api/user/recent')
def user_recent():
    """Get recent food scans."""
    user_id = request.args.get('user_id', 'default')
    limit = request.args.get('limit', 10, type=int)
    scans = get_recent_scans(user_id, limit)
    return jsonify({"status": "success", "scans": scans})


@app.route('/api/recommendations/<food_name>')
def food_recommendations(food_name):
    """Get healthier food alternatives for a given food."""
    recommendations = get_recommendations(food_name)
    return jsonify({"status": "success", "recommendations": recommendations})


@app.route('/api/household/<member_type>')
def household_suggestions(member_type):
    """Get food suggestions for a household member type."""
    suggestions = get_household_suggestions(member_type)
    return jsonify({"status": "success", "member_type": member_type, "suggestions": suggestions})


if __name__ == '__main__':
    # Run the app on 0.0.0.0 to allow access from other devices on the same network
    app.run(debug=True, host='0.0.0.0', port=5000)
