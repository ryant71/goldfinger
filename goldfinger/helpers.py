"""
Helper functions
"""

import json
from datetime import date, datetime, timedelta


def ounce_to_grams(ounces):
    return ounces * 28.3495


def pretty_print_json(json_dict):
    print(json.dumps(json_dict, indent=2))


def get_today_date():
    return date.today().strftime('%Y-%m-%d')


def get_days_ago_date(days_ago):
    d = datetime.now() - timedelta(days_ago)
    return d.strftime('%Y-%m-%d')


def days_diff(start_date, end_date):
    start = datetime.strptime(start_date, '%Y-%m-%d')
    end = datetime.strptime(end_date, '%Y-%m-%d')
    diff = end - start
    return diff.days
