 Real Estate CLI Assistant
A Command-Line Interface (CLI) Real Estate Assistant built using Python, designed to analyze property listings from CSV data files. This tool enables users to interact with real estate data through natural-language-style commands to uncover insights such as:

 Cheapest cities by price per Marla

 Most expensive areas in a selected city

 Average price or area per city

 Property listing trends over time

It performs data cleaning, exploratory data analysis (EDA), and on-demand visualizations, making it ideal for learning data science principles in a practical real estate context.

 Features
🔹 CLI-based natural language-style interaction

🔹 Cleans and standardizes noisy real estate data:

Converts inconsistent price formats (lakh, crore, arab)

Converts area units (sqft, kanal, marla)

Converts posted dates like "3 weeks ago" into timestamps

🔹 Calculates key metrics:

Price per Marla (PPM)

Average price and area per city

🔹 Handles outliers and missing data

🔹 Interactive graph prompts (matplotlib visualizations)

🔹 Supports user queries like:

"cheapest city"

"most expensive areas in Lahore"

"average price in Karachi"

"trend in listings"

 Technologies Used
 Python 3.x

 Pandas – for data manipulation

 NumPy – for numerical operations

 datetime & timedelta – for date parsing

 Matplotlib – for data visualizations

 Custom cleaning logic for textual and inconsistent real-world data

 CSV file handling

 Skills Demonstrated
Real-world data wrangling and preprocessing

Exploratory Data Analysis (EDA)

Building interactive CLI applications

Implementing custom data parsers for price, area, and dates

Creating visual dashboards on demand

Modular code design and reusability

Understanding of real estate market metrics

Dataset
The project uses a .csv file containing raw real estate listings with attributes like:

Location, city

Area (with units)

Price (in various text formats)

Listing date (e.g., "2 weeks ago")
