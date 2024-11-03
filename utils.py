import base64
import os
from datetime import datetime
import pytz
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
bucket = client.bucket(bucket_name)  # Use the client to get the bucket

# Constants for filenames
DATA_FILE = 'data.json'
VERSION_FILE = 'version.txt'

# Function to get the current GCS generation ID
# Variable to store data in memory
data_in_memory = {}
data_modified = True  # Track if data has been modified


def get_cloud_generation():
    blob = bucket.blob(DATA_FILE)
    blob.reload()  # Make sure we have the latest metadata
    return blob.generation  # Returns unique generation ID as a string


# Function to load data from GCS if modified
def load_data():
    global data_in_memory, data_modified  # Use global variables

    if data_modified:
        # If data has been modified, pull from the cloud
        data_json = download_file()  # Fetch the latest data from GCS
        data_in_memory = json.loads(data_json)  # Store it in memory

        # Reset the modified flag
        data_modified = False

    return data_in_memory  # Return the data stored in memory


# Function to save data and update the cloud version
def save_data(data):
    global data_in_memory, data_modified  # Use global variables
    data_modified = True  # Set the modified flag
    data_in_memory = data  # Update the in-memory data

    # Convert to JSON and upload to GCS
    data_json = json.dumps(data, indent=4)
    upload_file(data_json)

    # Update the cached generation ID after upload
    current_generation = get_cloud_generation()
    with open(VERSION_FILE, 'w') as version_file:
        version_file.write(str(current_generation))


def download_file():
    blob = bucket.blob(DATA_FILE)
    return blob.download_as_text()


def upload_file(data):
    blob = bucket.blob(DATA_FILE)
    blob.upload_from_string(data, content_type='application/json')


LOG_FILE = 'log.txt'

def log(message: str):
    """Writes a log message with a timestamp to a log.txt file in the GCS bucket."""

    # Get the current time in UTC
    utc_now = datetime.now(pytz.utc)

    # Convert to EST
    est = pytz.timezone('America/New_York')
    est_now = utc_now.astimezone(est)

    # Format the time in 12-hour format with AM/PM
    timestamp = est_now.strftime('%Y-%m-%d %I:%M:%S %p')

    print(timestamp)
    log_entry = f"{timestamp} - {message}\n"

    # Create a blob object for the log file
    blob = bucket.blob(LOG_FILE)

    # Download the existing log data if the log file exists
    try:
        existing_log = blob.download_as_text()
    except Exception:
        existing_log = ""  # If the file doesn't exist, start with an empty string

    # Append the new log entry to the existing log data
    updated_log = existing_log + log_entry

    # Upload the updated log back to the GCS bucket
    blob.upload_from_string(updated_log, content_type='text/plain')



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