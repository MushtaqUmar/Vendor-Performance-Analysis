# We have created this script seperately since this is repetetive task like if we get new vendor data we neeed to do these steps again from extracting required info, cleaning, adding new featuresn and finally add to server as new reqd table -> Hence we create this script and schedule it so that we don't need to do this task manually



# WHATEVER WE DO HERE WE HAVE DONE IT IN EXPLORATORY DATA ANALYSIS FILE AFTER OBSERVING WHAT CHANGES WE NEED TO DO. -> CHECK THERE WHEN YOU IT ANYTHING WHY AND HOW WE DO IT FOR EXPLANATION

import os
import pandas as pd
import numpy as np 
import time
import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# importing ingest_db() from ingestion_db.py(Already created you can see in same folder while ingesting raw csv files into mysql serverf database)  -> here to ingest vendors final summary into mysql server database.
from ingestion_db import ingest_db  # This one -> ingest_db(df, table_name, engine)



# ======================= Configure the logging behavior and format
logging.basicConfig(
    filename="logs/get_vendor_final_summary.log",        # Where logs will be written -> create file "get_vendor_final_summary.log" inside logs folder. (Same named log file as pyhon script file to get idea which logging file it is 
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',  
    level=logging.DEBUG,
    force=True  #  This forces reconfiguration : because when we import "from ingestion_db import ingest_db" above we have configuration there for that session and when we try this new logging for this python session it gets ignored because only one is executed (other gets ignored)
       # |> overrides the logging configuration for the current Python session.
      # It does NOT delete or replace previous log files created by other scripts. """
)



# ================== STEP 1: Function that will extract required/useful data from different tables and merge into single one to get overall vendors summary.
def create_vendors_final_summary(conn): # connection to mysql server database sent while calling this function
    
    vendors_final_summary = pd.read_sql_query("""WITH FreightSummary AS(
    SELECT VendorNumber, SUM(Freight) as FreightCost
    FROM vendor_invoice
    GROUP BY VendorNumber
    ),
    
    PurchaseSummary AS (SELECT 
    p.VendorNumber, p.VendorName, p.Brand, p.Description, p.PurchasePrice,
    pp.Price AS ActualPrice, pp.Volume,
    SUM(p.Quantity) AS TotalPurchaseQuantity,
    SUM(p.Dollars) AS TotalPurchaseDollars
    FROM purchases AS p
    INNER JOIN purchase_prices AS pp
    ON p.Brand = pp.Brand 
    WHERE p.PurchasePrice > 0  # Need those having price (No free i.e., no mistakenly added records)
    GROUP BY  p.VendorNumber, p.VendorName, p.Brand,p.Description, p.PurchasePrice, pp.Volume, pp.Price
    ),

    SalesSummary AS (SELECT
    VendorNo, Brand, 
    SUM(SalesQuantity) AS TotalSalesQuantity,
    SUM(SalesPrice) AS TotalSalesPrice,
    SUM(SalesDollars) AS TotalSalesDollars,
    SUM(ExciseTax) AS TotalExciseTax 
    FROM sales
    GROUP BY VendorNo, Brand
    )

    # Now fetch final summarey table from above CTE
    SELECT 
    ps.VendorNumber, ps.VendorName, ps.Brand, ps.Description, ps.PurchasePrice,
    ps.Volume, ps.ActualPrice,
    ps.TotalPurchaseQuantity,
    ps.TotalPurchaseDollars,
    ss.TotalSalesQuantity,
    ss.TotalSalesPrice,
    ss.TotalSalesDollars,
    ss.TotalExciseTax,
    fs.FreightCost
    FROM PurchaseSummary AS ps
    LEFT JOIN SalesSummary AS ss     # Left joinso that we can't skip those who have purchased products but have not sold anything yet.
    ON ps.VendorNumber = ss.VendorNo
    AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary AS fs
    ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC""", conn)
    
    return vendors_final_summary
# Function ended here






# =========== Data Wrangling (Cleaning, dormatting and new feature extraction) Now clean the resultant summary table for accurate results
def clean_data(df):  # take funal summary table as argument

    # changing datatype to float
    df['Volume'] = df['Volume'].astype('float')

    # Filling missing numeric values as 0
    df.fillna(0, inplace=True)


    # Removing spaces from categorical columns (columns like VendorName, Description have categorical entries)
    df['VendorName'] = df['VendorName'].str.strip()  # strip() will trim spaces
    df['Description'] = df['Description'].str.strip()  # there was no need but still we did it for any future entries.


    #========================= Adding new features based on present ones for bettr analysis ================================
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']  
    
     #======= Profit Margin of vendors (%)
    df['ProfitMargin'] = round(df['GrossProfit'] / df['TotalSalesDollars'] * 100, 2)   # Negative means LOss
    # It may have infinity since TotalSalesDollars in denomenator is 0 for some vendors - Handling it 
    # Replace inf, -inf with 0
    df['ProfitMargin'] = df['ProfitMargin'].replace([np.inf, -np.inf], 0)

    # ========= Column for 'StockTurnOver' : (or Inventory Turnover) means how many times a company sells and replaces its inventory during a specific period.
    df['StockTurnover'] = round(df['TotalSalesQuantity'] / df['TotalPurchaseQuantity'], 2)

    #======= Sales to Purchase Ratio:  It tells how much you are selling compared to how much you are buying.
    df['SalesToPurchaseRatio'] = df['TotalSalesDollars'] / df['TotalPurchaseDollars']

    # Finally return this cleaned and features rich dataframe(vendors_final_summary table)
    return df
#========== Ended here







#=============== Calling functions -> i.e., actually doing extraction reqd data, cleaning, data engineering, maintaining logs in logging file and finally put into mysql database

if __name__ == '__main__':  # -> What does rthis mean : Read same stuff in ingestion_db.py script

    #====================== Connection to mysql server database 'inventory_db' to ingest this summary sile so that whenever we need this for analysis or dashboarding etc we fetch from there only.
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
        logging.error(f"Failed to connect to MySQL: {e}")  # added to log file created above -> 
        raise  # Stop script if connection fails 

    start = time.time()  # Starting process
    #============= Calling above function to create vendors final summary data from existing tables & cleaning it
    with engine.connect() as conn:
        # Create summary
        logging.info("Creating Vendors Summary Table")
        summary_df = create_vendors_final_summary(conn)  # Calling above function created for this task
        # SHow demo in log file
        logging.info(summary_df.head() )

        # Clean it
        logging.info("Cleaning data...")
        clean_df =  clean_data(summary_df)  # Calling above created function for this task.
        # SHow demo in log file
        logging.info(clean_df.head() )
        

    # ================== Ingest into database finally ==================
    logging.info("Ingesting summary data into database...")
    ingest_db(clean_df, 'vendors_final_summary', engine) # Calling imported -> ingest_db(df, table_name, engine)

    end = time.time()
    total_min = (end - start) / 60
    logging.info(f'============= Vendors Sales final summary Ingested successfully  in {total_min} minutes =============')

# === __name__ == '__main__' block Ended here.











