import base64
import os

import numpy as np
import json
from google.cloud import storage


# Load credentials from environment variable
credentials_json = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if credentials_json:
    credentials = json.loads(base64.b64decode(credentials_json))
    # Save the JSON file temporarily for the client to use
    with open("credentials.json", "w") as cred_file:
        json.dump(credentials, cred_file)
# Initialize Google Cloud Storage bucket
client = storage.Client.from_service_account_json("credentials.json")

bucket_name = "rit_ckl_stats"
bucket = storage.client.bucket(bucket_name)

# Constants for filenames
DATA_FILE = 'data.json'
VERSION_FILE = 'version.txt'

# Function to get the current GCS generation ID
def get_cloud_generation():
    blob = bucket.blob(DATA_FILE)
    blob.reload()  # Make sure we have the latest metadata
    return blob.generation  # Returns unique generation ID as a string

# Function to load the data (checks for cloud updates first)
def load_data():
    try:
        # Get the cloud generation ID
        current_generation = get_cloud_generation()

        # Check if we have a stored version ID and compare
        try:
            with open(VERSION_FILE, 'r') as version_file:
                cached_generation = version_file.read().strip()
        except FileNotFoundError:
            cached_generation = None

        # If versions differ, download the new data
        if cached_generation != current_generation:
            data_json = download_file()  # Fetch the latest data from GCS
            data = json.loads(data_json)

            # Save data and update the cached generation ID
            with open(DATA_FILE, 'w') as data_file:
                json.dump(data, data_file, indent=4)
            with open(VERSION_FILE, 'w') as version_file:
                version_file.write(current_generation)
        else:
            # Load from the local file if versions match
            with open(DATA_FILE, 'r') as data_file:
                data = json.load(data_file)

        return data

    except json.JSONDecodeError:
        return {}
    except FileNotFoundError:
        return {}

# Function to save data and update the cloud version
def save_data(data):
    # Convert to JSON and upload to GCS
    data_json = json.dumps(data, indent=4)
    upload_file(data_json)

    # Update the cached generation ID after upload
    current_generation = get_cloud_generation()
    with open(VERSION_FILE, 'w') as version_file:
        version_file.write(current_generation)

def download_file():
    blob = bucket.blob(DATA_FILE)
    return blob.download_as_text()

def upload_file(data):
    blob = bucket.blob(DATA_FILE)
    blob.upload_from_string(data, content_type='application/json')



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