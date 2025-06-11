#!pip install SQLAlchemy


# import sys
# print(sys.executable)   # This will tell you which Python installation your Jupyter is using (WHere is that installed -> must be at same location where jupyter is else not work)


#!{sys.executable} -m pip install SQLAlchemy
         # Why I did this?  Bcz I was getting ModukleNotFOund error even after installing above as My jupyter is using another python installation(Diferent path as see above) where above sqlalchemy module was not installed
         #  This ensures the packages are installed in the same environment that Jupyter is running.





# IMPORTING REQUIRED PYTHON LIBRARIES
# -----------------------------------------

import os  # Built-in module to interact with the operating system (for folder and file handling)
import pandas as pd  # Powerful library for reading, manipulating, and analyzing data
import time  # Module to track execution time for performance logging
import logging  # Module to create and write log files for tracking errors and activities
from sqlalchemy import create_engine   # create_engine Used to connect Python to MySQL databases using SQLAlchemy(-SQLAlchemy is a powerful Python library that lets you connect to databases and run SQL queries using both raw SQL and Pythonic ORM-style code.).
from sqlalchemy.engine import URL   # URL is a special helper class in SQLAlchemy used to safely and correctly build database connection strings — especially when your password or other parts contain special characters (like @, :, #, etc.).





# ===================  SETUP: Folder Paths & Logging ===================
# -----------------------------------------

# Path to the folder where your CSV files are stored
data_folder = "Company dataset"    #  Same directory where this pythln file is , so no need of full path

# Create a folder named 'logs' if it doesn't exist already (Else if already created , it get skipped)
log_folder = "logs"
os.makedirs(log_folder, exist_ok=True)  #    -> exist_ok -> Tells python Please create this folder... but if it already exists, that’s okay — don’t throw an error.
# Log file path inside the 'logs' folder  (Where we actually store logging (Erractivities happen) about ingesting files.
log_file = os.path.join(log_folder, "ingestion_log.log")   # Name it ingestion_log.log  (.log -> Openst in text mode like .txt)



# Configure the logging behavior and format
logging.basicConfig(
    filename=log_file,        # Where logs will be written
    filemode='a',             # 'a' means append mode (keeps old logs)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format -  how each log entry should look.  
    #     ( %(asctime)s -> when something happened,  %(levelname)s - What level of log it is (INFO, DEBUG, ERROR, CRITICAL, WARNING) %(message)s -> Whatever message you write like logging.info("Ingestion complete.")
 
    level=logging.DEBUG        # DEBUG -> Python will log everything, including DEBUG, INFO, WARNING, ERROR, and CRITICAL.
    #level=logging.INFO   -> This sets the minimum log level to INFO.(Limited).
)




# =========== CONNECT TO MYSQL USING SQLALCHEMY =============
# -----------------------------------------

try:
    # Use SQLAlchemy's URL builder
    url = URL.create(   
        drivername="mysql+mysqlconnector",
        username="root",
        password="UMMU@112244",  # Don't worry, it's safe here
        host="localhost",
        database="Inventory_db"
    )
    engine = create_engine(url)   # Connect to MySQL local server considering 'Inventory_db' database
    logging.info("Successfully connected to MySQL.")  # Added to log file 
except Exception as e:
    logging.error(f"Failed to connect to MySQL: {e}")  # added to log file created above
    raise  # Stop script if connection fails






# ============== Ingest dataframes (raw csv files) into database tables ==============
# -----------------------------------------------------------------------
def ingest_db(df, table_name, engine):  # Called inside below 'load_raw_data' function. -> Also used in other script file like get_vendors_final_summary.py.
    
    # df.to_sql(name=table_name, con=engine, index=False, if_exists='replace')  # --> Was unable to handle very large file like 30 lakhs or crore data records
    
    with engine.begin() as connection:   #  engine.begin() → Ensures transactions are handled properly
        df.to_sql(name=table_name, con=connection, index=False, if_exists='replace', chunksize=10000, method='multi')  
                 # chunksize=10000 → Sends data in smaller, safer batches
                 # method='multi' → Executes multiple inserts per batch (faster)




# ============== LOAD/PROCESS EACH CSV FILE IN THE FOLDER ==============
# -----------------------------------------
def load_raw_data():     # Using functional programming approach
    start_overall = time.time()
    
    # Loop through each file in the 'Company dataset' folder
    for filename in os.listdir(data_folder):
        if filename.endswith(".csv"):  # Check if the file is a CSV only
            file_path = os.path.join(data_folder, filename)  # Full file path
            table_name = filename.replace(".csv", "").lower()  # Same without .csv i.e., Table name = filename (cleaned)
    
            try:
                start_time = time.time()  # Start the stopwatch
    
                # Read the CSV file into a Pandas DataFrame
                df = pd.read_csv(file_path)
                logging.info(f"Reading file: {filename} | Shape: {df.shape}")    # into log file 
    
                # Upload DataFrame to MySQL as a new table or overwrite existing one
                ingest_db(df, table_name, engine)  # Calll to function that actually injects this to DB table
                
                total_time = round(time.time() - start_time, 2)  # Calculate total time taken in sec
                total_time_in_min = total_time / 60 
                logging.info(f"Ingested '{filename}' into MySQL table '{table_name}' in {total_time_in_min: .2f} min.")

            except Exception as e:
                logging.error(f"Error while ingesting '{filename}': { e}")


    end_overall = time.time()  # seconds
    total_min = (end_overall - start_overall)/60
    logging.info(f"\n=====================Total Time Taken: {total_min}minutes =====================")

    #===== Extra Info
    logging.info("All CSV files processed. Ingestion completed successfully.\n")  # Inside logging file
    print("All files have been processed. Check 'logs/ingestion_log.txt' for detailed logs.")    # Displayed to user so that he can check log file if he/she wants for details.


#======================== Calling it
if __name__ == "__main__":   # Run Only run this part of the script if the script is being run directly (like python ingestion_db.py in terminal)— not run when it’s imported somewhere else and then run that script (i.e, if it is called here directly then work, But when some else is imported our script like 'from ingestion_db import load_raw_data', then this part should not work.).
    load_raw_data()
#== ended here
