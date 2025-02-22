#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, jsonify
from get_meal import get_all_meals
from apscheduler.schedulers.background import BackgroundScheduler
import json
import os
import threading

app = Flask(__name__)
CACHE_FILE = "cached_recommendations.json"

def update_dining_hall_data():
    """ Updates dining hall data and ChatGPT recommendations together. """
    print("🔄 Starting data update...")
    dining_hall_data, recommended_halls, hall_explanations, meal_type = get_all_meals()

    # Save to cache
    cache_data = {
        "dining_hall_data": dining_hall_data,
        "recommended_halls": recommended_halls,
        "hall_explanations": hall_explanations,
        "meal_type": meal_type,
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache_data, f)

    print("✅ Dining hall data & ChatGPT recommendations updated.")

def async_update():
    """ Runs the update in a separate thread to avoid blocking requests. """
    thread = threading.Thread(target=update_dining_hall_data)
    thread.start()

@app.route('/update', methods=['POST'])
def manual_update():
    """ Triggers an asynchronous update and immediately returns a response. """
    async_update()
    return jsonify({"message": "Update started! Data will refresh soon."})

# Initial update at startup
update_dining_hall_data()

# Background Scheduler to update every 2 hours
scheduler = BackgroundScheduler()
scheduler.add_job(update_dining_hall_data, 'interval', hours=2)
scheduler.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8002)

