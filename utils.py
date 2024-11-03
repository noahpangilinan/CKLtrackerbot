import json
import numpy as np



# Function to load data (for bot use)

def load_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        # Return an empty dictionary or list if the file is empty or not valid JSON
        return {}
    except FileNotFoundError:
        # Return an empty dictionary if the file does not exist
        return {}
# Function to save data (for your use)
def save_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


def add_ckl_race(placements: list[tuple], race: str):
    data = load_data()

    # Keep track of new users added
    new_users = []

    # Process each placement
    for user, place in placements:
        # Check if the user doesn't exist in data and log them as new
        if user not in data:
            data[user] = {}
            new_users.append(user)  # Track new users

        # Add the race if it doesn't exist for the user
        if race not in data[user]:
            data[user][race] = []

        # Append the place to the user's race data
        data[user][race].append(int(place))

    # Save updated data
    save_data(data)




def format_user_race_data(dct):
    print(len(dct.items()))
    user_str = ""
    for race, placements in dct.items():  # dct.iteritems() in Python 2
        user_str += ("{}: {}".format(race, placements))
        user_str += "\n"
    return user_str

def get_avg_placement(user:str, track:str):
    data = load_data()
    return round(np.mean(data[user][track]), 2)

def points_dict():
    return {
    1 : 15,
    2 : 12,
    3 : 10,
    4 : 9,
    5 : 8,
    6 : 7,
    7 : 6,
    8 : 5,
    9 : 4,
    10 : 3,
    11 : 2,
    12 : 1}

def get_avg_points(user:str, track:str):
    data = load_data()
    placements_list = data[user][track]
    points_list = [*map(points_dict().get, placements_list, placements_list)]
    return round(np.mean(points_list), 2)


def find_worst_track_by_placement(user:str):
    data = load_data()
    return round(np.min(data[user]), 2)

def find_best_track_by_placement(user:str):
    data = load_data()
    return np.max(data[user])

# Function to prepare race data and track new users
def prepare_race_data(data, placements):
    new_users = []
    for user, _ in placements:
        if user not in data:
            new_users.append(user)  # Track new users
    return new_users