import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

# Connect to the database
try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    # Create a cursor to execute SQL queries
    cursor = connection.cursor()
    
    # Example query
    cursor.execute("SELECT NOW();")
    result = cursor.fetchone()
    print("Current Time:", result)

    # Close the cursor and connection
    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print(f"Failed to connect: {e}")
# main.py

from prompts import PROMPTS
from llm_interface import call_model
from preprocessing import clean_text
import yaml

def main():
    # Load config for prompt choice
    with open("config.yaml") as f:
        config = yaml.safe_load(f)

    sample_text = """
    Today we discussed project timelines and assigned John to lead the frontend redesign.
    Also, finalize the budget by next Wednesday.
    """

    cleaned_text = clean_text(sample_text)
    prompt_template = PROMPTS[config["prompt_type"]]
    prompt = prompt_template.format(text=cleaned_text)

    response = call_model(prompt)
    print("Model output:\n", response)

if __name__ == "__main__":
    main()
