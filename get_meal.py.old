#!/usr/bin/env python
# encoding: utf-8

import requests
from bs4 import BeautifulSoup
import datetime


def get_meal_title_class():
    current_hour = datetime.datetime.now().hour
    if 0 <= current_hour < 13:  # Morning (00:00 to 11:59)
        return "meal-title lunch"
    else:  # Afternoon (13:00 to 23:59)
        return "meal-title dinner"

def get_meal_info(url):
    meal_title_class = get_meal_title_class()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    meal_items = soup.find_all('li', {'class': 'menu-item'})
    meals = []

    for meal_item in meal_items:
        meal_title = meal_item.find('div', {'class': meal_title_class})
        if meal_title:
            meal = {}
            meal['name'] = meal_title.text.strip()

            allergens = meal_item.find_all('span', {'class': 'allergen'})
            allergens_list = []

            for allergen in allergens:
                allergens_list.append(allergen.text.strip())

            meal['allergens'] = allergens_list
            meals.append(meal)

    return meals

urls = {
    'Akers': 'https://eatatstate.msu.edu/menu/The%20Edge%20at%20Akers/all/',
    'Brody': 'https://eatatstate.msu.edu/menu/Brody%20Square/all/',
    'Case':'https://eatatstate.msu.edu/menu/South%20Pointe%20at%20Case/all/',
    'Holden': 'https://eatatstate.msu.edu/menu/Holden%20Dining%20Hall/all/',
    'Landon': 'https://eatatstate.msu.edu/menu/Heritage%20Commons%20at%20Landon/all/',
    'Owen': 'https://eatatstate.msu.edu/menu/Thrive%20at%20Owen/all/',
    'Shaw':'https://eatatstate.msu.edu/menu/The%20Vista%20at%20Shaw/all/',
    'Phillips': 'https://eatatstate.msu.edu/menu/The%20Gallery%20at%20Snyder%20Phillips/all/'
    }

all_meals = {}

def get_all_meals():
    for name, url in urls.items():
        date = datetime.date.today().strftime('%Y-%m-%d')
        url = url + date
        meals = get_meal_info(url)
        all_meals[name] = meals
    return all_meals

