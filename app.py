#!/usr/bin/env python
# encoding: utf-8
from flask import Flask, render_template
from get_meal import get_all_meals
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)

# Global variable to store the latest dining hall data
dining_hall_data = {}


def update_dining_hall_data():
    global dining_hall_data
    dining_hall_data = get_all_meals()
    print(dining_hall_data)


# Schedule the update_dining_hall_data function to run every hour
scheduler = BackgroundScheduler()
scheduler.add_job(update_dining_hall_data, 'interval', hours=2)
scheduler.start()


@app.route('/')
def dining_halls():
    return render_template('dining_halls.html', dining_hall_data=dining_hall_data)


if __name__ == '__main__':
    # Update the dining hall data before starting the app
    update_dining_hall_data()
    app.run(debug=True)

