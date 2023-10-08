Superpy Usage Guide

FILE NAME: Superpy

AUTHOR: Marcin Pietrzak

CONTACT: marcinpiet@gmail.com

DATE: October 7, 2023

LICENSE: MIT License

DESCRIPTION:
Superpy is a command-line interface tool designed for supermarkets to meticulously manage and monitor their inventory.
This comprehensive management system allows for efficient control over available resources and warehouse stock levels.
It provides rapid and accurate updates of product assortments and delivers detailed information regarding product availability. 
It's an integral solution for businesses seeking precision and effectiveness in inventory tracking and management.

VERSION: 2.01 

Table of Contents
Introduction
Installation
Basic Usage
Buying Products
Selling Products
Generating Reports
Exporting Data
Advancing Time
Advanced Features
Generating Revenue Reports
Exporting Revenue Data
Generating Profit Reports
Exporting Profit Data
Conclusion


1. Introduction 
Superpy is a versatile command-line tool designed to help supermarkets manage their inventory efficiently.
 It offers various features for buying, selling, reporting, and exporting data related to products.
 This usage guide aims to provide step-by-step instructions and examples for Superpy's usage.


2. Installation 
Before you can start using Superpy, make sure you have Python 3.7 or higher installed on your system.
Additionally, you need to install the required Python packages by running the following command:

pip install prettytable openpyxl matplotlib

Once you have installed the necessary packages, you are ready to use Superpy.


3. Basic Usage.
 
Buying products.
 
To register the purchase of a product, use the following command:

python Super.py buy <product_name> <quantity> <price> [--date <purchase_date>] --expiration_date <expiration_date>
<product_name>: The name of the product you are buying.
<quantity>: The quantity of the product purchased.
<price>: The price per unit of the product.
[--date <purchase_date>] (Optional): The purchase date in the format YYYY-MM-DD. If not provided, the current date will be used.
--expiration_date <expiration_date>: The expiration date of the product in the format YYYY-MM-DD.

Example:
python Super.py buy Apples 100 0.5 --date 2023-09-28 --expiration_date 2023-10-10

Selling products.
To register the sale of a product, use the following command:

python Super.py sell <product_name> <quantity> <price> [--date <sale_date>]
<product_name>: The name of the product you are selling.
<quantity>: The quantity of the product sold.
<price>: The price per unit of the product.
[--date <sale_date>] (Optional): The sale date in the format YYYY-MM-DD. If not provided, the current date will be used.

Example:
python Super.py sell Apples 50 1.0 --date 2023-09-30

Generating reports. 

You can generate various types of reports using Superpy. Supported report types are 'bought', 'sold', and 'inventory'.

To generate a report, use the following command:

python Super.py report <report_type>
<report_type>: The type of report ('bought', 'sold', or 'inventory').

Example:
python Super.py report inventory


Exporting Data 
Superpy allows you to export data to CSV or XLSX format.

To export data, use the following command:

python Super.py export <data_type> [--format <output_format>] [--output <output_file>]
<data_type>: The type of data to export ('bought', 'sold', or 'inventory').
[--format <output_format>] (Optional): The output format ('csv' or 'xlsx'). Default is 'xlsx'.
[--output <output_file>] (Optional): The path to the output file. If not provided, a default filename will be used.

Example:
python Super.py export bought --format csv --output my_bought_data.csv


Advancing Time 
You can change the recognized "today" date using the advance-time command.

To advance time, use the following command:

python Super.py advance-time <days|now>
<days>: The number of days to advance (use '+' for forward and '-' for backward) or use 'now' to reset to the current date.

Example:
python Super.py advance-time +5


4. Advanced features.
 
Generating revenue reports. 
You can generate revenue reports for a specified date range.

To generate a revenue report, use the following command:

python Super.py report-revenue <start_date> <end_date>
<start_date>: The start date of the revenue report in the format YYYY-MM-DD.
<end_date>: The end date of the revenue report in the format YYYY-MM-DD.

Example:
python Super.py report-revenue 2023-09-01 2023-09-30

Exporting Revenue Data 
You can export revenue data to CSV or XLSX format.

To export revenue data, use the following command:

python Super.py export-revenue <start_date> <end_date> [--format <output_format>] [--output <output_file>]
<start_date>: The start date of the revenue report in the format YYYY-MM-DD.
<end_date>: The end date of the revenue report in the format YYYY-MM-DD.
[--format <output_format>] (Optional): The output format ('csv' or 'xlsx'). Default is 'xlsx'.
[--output <output_file>] (Optional): The path to the output file. If not provided, a default filename will be used.

Example:
python Super.py export-revenue 2023-09-01 2023-09-30 --format csv --output revenue_report.csv

Generating Profit Reports 
You can generate profit reports for different time periods or specific products.

To generate a profit report, use the following command:

python Super.py report-profit <period> [<value>]
<period>: The time period for the profit report ('day', 'month', 'year', 'all', or 'product').
[<value>] (Optional): The specific value for the time period (e.g., '2023-09-30' for a daily report or a product name for a product-specific report).

Example:
python Super.py report-profit day 2023-09-30

Exporting Profit Data 
You can export profit data to CSV or XLSX format.

To export profit data, use the following command:

python Super.py export-profit <period> [<value>] [--format <output_format>] [--output <output_file>]
<period>: The time period for the profit report ('day', 'month', 'year', 'all', or 'product').
[<value>] (Optional): The specific value for the time period (e.g., '2023-09-30' for a daily report or a product name for a product-specific report).
[--format <output_format>] (Optional): The output format ('csv' or 'xlsx'). Default is 'xlsx'.
[--output <output_file>] (Optional): The path to the output file. If not provided, a default filename will be used.

Example:
python Super.py export-profit month 2023-09 --format xlsx --output profit_report.xlsx


5. Conclusion 

Superpy is a powerful tool for supermarket inventory management. With its various features, you can efficiently track products, generate reports, and export data for analysis. This guide should help you get started with Superpy, but don't hesitate to explore more of its capabilities by checking out the available commands and options. For additional assistance, you can contact the author, Marcin Pietrzak, at marcinpiet@gmail.com.




