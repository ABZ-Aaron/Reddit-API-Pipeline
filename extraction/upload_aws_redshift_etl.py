import psycopg2  
import json

# Load in configuration data from our JSON file
with open(f'{path}/extraction/secrets/secret_reddit.json', 'r') as f:
  config_data = json.load(f)

# Save our JSON data
HOST = config_data['HOST']
PORT = config_data['PORT']
USER = config_data['USER']
PASSWORD = config_data['PASSWORD']

con = psycopg2.connect(dbname = "dev", 
                       host= HOST, 
                       port= PORT, 
                       user= USER, 
                       password= PASSWORD)

