"""
Helper functions
"""

import json

def ounce_to_grams(ounces):
    return ounces * 28.3495


def pretty_print_json(json_dict):
    print(json.dumps(json_dict, indent=2))
