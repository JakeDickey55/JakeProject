import psycopg2
import requests
import time
import os
from datetime import datetime

# Environment variable for database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable is not set.")

# API URL for fetching crypto data
API_url = "https://api.coinlore.net/api/global/"

def connect_to_db():
    retries = 5
    while retries > 0:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            print("Connected to the database.")
            return conn
        except psycopg2.OperationalError as e:
            print(f"Database connection failed: {e}. Retrying in 1 second...")
            retries -= 1
            time.sleep(1)
    raise Exception("Failed to connect to the database after multiple attempts.")

def grabbing_crypto_data():
    try:
        response = requests.get(API_url)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list) and data:
            return data[0]
        print("Unexpected API response format.")
    except requests.RequestException as e:
        print(f"Error fetching data from API: {e}")
    return None


def insert_crypto_data(conn, data):
    if not data:
        print("No data to insert.")
        return
    
    cursor = conn.cursor()
    try:
        print("Data to be inserted:", data)
        
        cursor.execute(
            """
            INSERT INTO crypto_market_data (
                coins_count, active_markets, total_mcap, total_volume,
                btc_dominance, eth_dominance, mcap_change, volume_change, avg_change_percent
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.get('coins_count'),
                data.get('active_markets'),
                data.get('total_mcap'),
                data.get('total_volume'),
                data.get('btc_d'),
                data.get('eth_d'),
                data.get('mcap_change'),
                data.get('volume_change'),
                data.get('avg_change_percent')
            )
        )
        conn.commit()
        print(f"Data inserted successfully at {datetime.now()}")
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inserting data: {e}")
    finally:
        cursor.close()

def main():
    print("Starting application...")
    
    while True:  # Add infinite loop
        try:
            conn = connect_to_db()
            print("Fetching crypto data...")
            data = grabbing_crypto_data()
            
            if data:
                print("Inserting data into database...")
                insert_crypto_data(conn, data)
            else:
                print("No data received from API")
                
            conn.close()
            print("Database connection closed.")
            
            # Wait for 5 minutes before the next fetch
            print("Waiting 5 minutes before next update...")
            time.sleep(300)  # 300 seconds = 5 minutes
            
        except Exception as e:
            print(f"An error occurred: {e}")
            print("Retrying in 30 seconds...")

if __name__ == "__main__":
    main()