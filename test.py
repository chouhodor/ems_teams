# Imports the Google Cloud client library
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ems-teams.json"
client = storage.Client()
# Instantiates a client

# Creates a new bucket and uploads an object
new_bucket = client.create_bucket('event-file')