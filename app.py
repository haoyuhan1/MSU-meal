#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template, jsonify
import json
import os
import datetime
import requests

app = Flask(__name__)
CACHE_FILE = "cached_recommendations.json"

def load_cached_data():
    """ Reloads the cache file every time the page is accessed and filters meals based on time. """
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cached_data = json.load(f)

        # Determine whether to show Lunch or Dinner
        current_hour = datetime.datetime.now().hour
        meal_type = "lunch" if current_hour < 13 else "dinner"

        print(f"🔄 Filtering meals for: {meal_type}")

        # Filter dining hall data to only include the correct meal type
        filtered_data = {}
        for hall, venues in cached_data.get("dining_hall_data", {}).items():
            filtered_data[hall] = {}
            for venue, meals in venues.items():
                filtered_meals = [
                    meal for meal in meals if "type" in meal and meal.get("type") == meal_type
                ]

                if not filtered_meals:
                    print(f"⚠️ No {meal_type} meals found for: {hall} - {venue}")

                filtered_data[hall][venue] = filtered_meals

        return {
            "dining_hall_data": filtered_data,
            "recommended_halls": cached_data.get("recommended_halls", []),
            "hall_explanations": cached_data.get("hall_explanations", {}),
            "meal_type": meal_type  # Pass the selected meal type to the template
        }

    print("⚠️ No cached data found!")
    return {"dining_hall_data": {}, "recommended_halls": [], "hall_explanations": {}, "meal_type": ""}

@app.route('/')
def dining_halls():
    cached_data = load_cached_data()
    return render_template(
        'dining_halls.html',
        dining_hall_data=cached_data["dining_hall_data"],
        recommended_halls=cached_data["recommended_halls"],
        hall_explanations=cached_data["hall_explanations"],
        meal_type=cached_data["meal_type"]
    )

@app.route('/force_update', methods=['POST'])
def force_update():
    """ Manually triggers an update in the scheduler and immediately returns a response. """
    try:
        response = requests.post("http://localhost:8002/update", timeout=10)
        if response.status_code == 200:
            return jsonify({"message": "Update triggered successfully!"})
        else:
            return jsonify({"error": "Failed to trigger update"}), 500
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)

