#  Vendor Performance Analysis — Data Analytics Project (SQL | Python | Power BI | AI-Assistance)
A real-world data analytics case study analyzing vendor performance in the retail/wholesale sector through the complete analytics pipeline: from data ingestion to insight generation and dashboard reporting.
<br>
### Project Overview
This project dives into the performance of vendors by evaluating their contribution to sales, profitability, inventory turnover, and operational efficiency. Through a structured ETL pipeline and deep statistical and visual analysis, we aimed to identify underperforming vendors, optimize procurement, and drive smarter business decisions.
<br>
### Key Outcome: 
Empower business stakeholders with data-backed strategies to increase profit, reduce unsold capital, and improve vendor relationships.

### Business Problem
In retail/wholesale operations, vendors are critical to profitability, supply chain continuity, and customer satisfaction. Poor vendor performance (e.g., late delivery, high cost, low stock turnover) can disrupt operations and reduce revenue. This project answers:

Who are the top and underperforming vendors?

Are purchases turning into sales effectively?

Are some vendors delivering high margins but low sales?

Which vendors have excessive unsold stock?

Is bulk purchasing helping reduce unit costs?

etc
<br>
<hr>

### Tools & Technologies
 We used a modern data stack to implement this analysis: <br>
<b>- MySQL:</b> Central relational database to store raw data and aggregated metrics. MySQL is a popular, reliable choice for data warehousing in analytics projects. <br>
<b>- Python:</b> Data ingestion, transformation and analysis were done in Python (using libraries like Pandas, NumPy, and SQLAlchemy). Python’s rich ecosystem (pandas, Matplotlib/Seaborn, etc.) lets us efficiently query MySQL and perform EDA. <br>
<b>- SQL:</b> Used within MySQL and via Python scripts to explore tables, clean data, join records, and build aggregate tables. SQL was essential for merging vendor, sales, and returns data in a structured way. <br>
<b>- Power BI:</b> For interactive visualization and dashboarding. Power BI’s user-friendly interface and robust integration (it can connect directly to MySQL) enable transforming raw data into meaningful insights
<br>
<b>- Jupyter Notebooks:</b> Development environment for writing Python code, EDA, and generating visual charts during analysis.
Version Control: The project (scripts, notebooks, report, and .pbix file) is maintained in a GitHub repository for reproducibility and collaboration.
<br>
<b>AI_Assistance:</b>
Leveraged AI tools like ChatGPT, DeepSeek, Claude, Gemini, and Copilot throughout the project lifecycle — from generating scripts and debugging errors to creating insightful charts, validating logic, and enhancing the final reporting and recommendations. These tools significantly accelerated analysis, improved code quality, and boosted strategic thinking.
<br>
<hr>

### Repository Structure

```
Vendor-Performance-Analysis/
│
├── Data/                              # Raw CSV files
├── logs/                              # ETL logs (Monitor ETL process for information, warning , error that helps in Debugging).
├── Scripts SQL_Python
    ├── ingestion_db.py                    # Python ETL script
    ├── get_vendors_final_summary.py       # script for final Summary Table for analysis and insights
├── Notebooks
    ├── vendor_performance_schema.sql      # SQL schema definition
    ├── Exploratory Data Analysis.ipynb    # Python EDA notebook - on all company's raw csv data files)
├── Vendor Performance Analysis.ipynb  # Additional analysis (EDA, cleaning, feature engineering, research questions & insights from vendors_final_summary)
├── Dashboards
    ├── Visualizing Insights.pbix          # Power BI dashboard file to visualize KPI's and insights.
├── Final Reporting.pdf                # Final report with findings and recommendations
├── .gitignore               # Avoid un-neccessary/restricted files and folders
└── README.md                          # Project overview and documentation (you're here!)
```
<br>
<hr>

### Workflow:
High-level workflow of the Vendor Performance Analysis project from problem definition through ETL, analysis, dashboarding, and reporting. <br>
##### Define the Problem:
We clarified the scope (vendor performance in retail/wholesale) and identified key vendor KPIs to track, following industry guidance on vendor metrics.

##### Data Ingestion (ETL):
Raw datasets (e.g. sales , purchases , Purchases_price, vendor_invoice) were ingested into MySQL using Python ETL scripts (ingestion_db.py). This involved parsing CSVs, creating normalized tables, and loading data into the database. This approach is consistent with best-practice pipelines where Python scripts populate a logical DB schema for analysis

##### Maininting logs: (for Ingestion, cleaning, and summary/aggregated table creation)
using seperate log files for ETL logs (Monitor ETL process for information, warning , error that helps in Debugging)

##### Data Cleaning & EDA:
Using SQL queries and Python, we examined database tables & cleaned data as per requirement. Tasks included removing duplicates, handling missing values, and maintaining formatting etc.

##### Feature Engineering: 
We calculated vendor-level metrics by aggregating transaction data. Key features included GrossProfit, ProfitMargin, Stock Turnover, Sales To Purchase Ratio etc. The aggregated summary table (Vendors_final_Summary) was created with these features.

##### Store Aggregated Metrics:
The Vendors_final_Summary table was written back into MySQL for efficient querying. Persisting the final aggregated table in the database allows the process to be automated for future data updates (new data can be ingested and summary refreshed automatically). 

##### Note : For vendors_finaly_summary table seperate script "get_vendors_final_summary.py" is written that can be automated for future data updates ( (new data can be ingested and summary refreshed automatically). 

##### Exploratory Data Analysis (EDA):
In Python (Pandas), we performed deeper analysis and visualization on the <b>aggregated data (vendors_final_summary)</b>. We used statistical plots (Seaborn, Matplotlib) and data slicing to answer research questionsthat helped to resolve business problem.
.
##### Visualization Dashboard:
A Power BI dashboard was built by connecting directly to the MySQL database. This interactive report allows business users to filter by vendor or category and view real-time charts of vendor KPIs, harnessing Power BI’s capabilities for intuitive dashboards.

##### Reporting:
Finally, we compiled a formal report (Final Reporting.pdf) summarizing findings. It includes charts, tables, and written analysis of key insights along with strategic recommendations for vendor management.

<hr>

### Some Key Insights: <br>
##### Profit Margin Disparity
Low-performing vendors have higher average profit margins (42.3%) than top-performing ones (23.0%) — suggesting premium pricing or lower costs.

##### StockTurnover vs. Profit
Stock turnover does not strongly impact gross profit (weak -0.04 correlation), but shows positive correlation with profit margin (0.40).

##### High Unsold Inventory
$35.2M unsold capital detected — indicating overstock, poor demand, or ineffective distribution strategies.

##### Top Vendor Dependency
Top 10 vendors account for 66% of purchases — high over-reliance risk. One vendor failure can significantly disrupt operations.

##### Bulk Purchase Advantage
Bulk buyers receive up to 72% lower per-unit cost — a strong incentive to encourage bulk buying through pricing strategy.

##### etc
<br>
<hr>

### Statistical Validation (Hypothesis Testing)
##### Objective: Is the profit margin of top vs. low-performing vendors statistically different?

##### Null Hypothesis (H₀): No significant difference

##### Alternative (H₁): There is a significant difference
##### Result: Reject H₀ — there is a statistically significant difference between the two.

<br>
<hr>

### Final Recommendations
✓ Re-evaluate pricing for ‘low sales but high margin brands’ to boost sales volume
without sacrificing profitability.<br>
✓ Diversify vendor partnerships to reduce dependency on a few suppliers and mitigate
supply chain risks.<br>
✓ Leverage bulk purchasing advantages to maintain competitive pricing while
optimizing inventory management.<br>
✓ Optimize slow-moving inventory by adjusting purchase quantities, launching
clearance sales, or revising storage strategies.<br>
✓ Enhance marketing and distribution strategies for low-performing vendors to drive
higher sales volumes without compromising profit margins & for top vendors,
negotiate better procurement costs, pricing stretegy or reduce overheads to improve
margins.<br>
✓ Enable Continuous Monitoring
Power BI dashboards cab be set to auto-refresh from MySQL for near real-time KPI tracking.<br>

- By implementing these recommendations, the company can achieve sustainable
profitability, mitigate risks, and enhance overall operational efficiency.
