"""
FILE NAME: Superpy

AUTHOR: Marcin Pietrzak
CONTACT: marcinpiet@gmail.com
DATE: Creation date, e.g., October 7, 2023

LICENSE: Appropriate license, e.g., MIT License

DESCRIPTION:
Superpy is a command-line interface tool
designed for supermarkets
to meticulously manage and monitor their inventory. 
This comprehensive management system 
allows for efficient control
over available resources and warehouse stock levels. 
It provides rapid and accurate updates 
of product assortments and delivers
detailed information regarding product availability. 
It’s an integral solution for businesses seeking 
precision and effectiveness in inventory tracking and management. 

VERSION: 2.01 EN. -  Full functionality.
"""
# Import necessary libraries/modules
import argparse # For command-line argument parsing
import csv # For CSV file handling
import os # For file system operations
from datetime import datetime, timedelta # For date and time manipulation
from prettytable import PrettyTable # For generating tabular data
from openpyxl import Workbook # For working with Excel files
import matplotlib.pyplot as plt # For plotting graphs
import main



# Define file paths for data storage
BOUGHT_FILE_PATH = 'bought.csv'
SOLD_FILE_PATH = 'sold.csv'
INVENTORY_FILE_PATH = 'inventory.csv'
TIME_SHIFT_FILE = 'time_shift.txt'


# Create a command-line argument parser with descriptions
parser = argparse.ArgumentParser(description='CLI tool for managing supermarket inventory.')
subparsers = parser.add_subparsers(dest='command', help='Super.py -CLI tool for managing supermarket inventory.- Available commands')

# Define subparsers for different commands and their arguments
# 'buy' command: Register the purchase of a product
buy_parser = subparsers.add_parser('buy', help='To register the purchase of a product.')
buy_parser.add_argument('product', type=str, help='Product name.')
buy_parser.add_argument('quantity', type=int, help='Product quantity.')
buy_parser.add_argument('price', type=float, help='Price per item.')
buy_parser.add_argument('date', type=str, help='Date of purchase. (YYYY-MM-DD)', nargs='?', default=None)
buy_parser.add_argument('--expiration_date', type=str, help='Product expiry date. (YYYY-MM-DD)', required=True)

# 'sell' command: Register the sale of a product
sell_parser = subparsers.add_parser('sell', help='To register the sale of a product.')
sell_parser.add_argument('product', type=str, help='Product name.')
sell_parser.add_argument('quantity', type=int, help='Product quantity.')
sell_parser.add_argument('price', type=float, help='Price per item.')
sell_parser.add_argument('date', type=str, help='Sale date. (YYYY-MM-DD)', nargs='?', default=None)

# 'report' command: Generate reports
report_parser = subparsers.add_parser('report', help='Generating reports.')
report_parser.add_argument('type', choices=['bought', 'sold', 'inventory'], help='Report type.') 

# 'export' command: Export data to XLSX or CSV
export_parser = subparsers.add_parser('export', help='Export data to XLSX or CSV.')
export_parser.add_argument('type', choices=['bought', 'sold', 'inventory'], help='Export type.')
export_parser.add_argument('--format', '-f', type=str, choices=['csv', 'xlsx'], default='xlsx', help='Export format.')
export_parser.add_argument('--output', '-o', type=str, help='Path to the output file.', nargs='?', default=None)

# 'advance-time' command: Change the date recognized as today
advance_time_parser = subparsers.add_parser('advance-time', help='Changes the date that Superpy recognizes as today.')
advance_time_parser.add_argument('days', type=str, help='Number of days ahead (+) or backwards. (-) or „now” to reset')

# 'report-revenue' command: Generate revenue report
revenue_report_parser = subparsers.add_parser('report-revenue', help='Generate revenue report.')
revenue_report_parser.add_argument('start_date', type=str, help='Starting date. (YYYY-MM-DD)')
revenue_report_parser.add_argument('end_date', type=str, help='End date. (YYYY-MM-DD)')

# 'export-revenue' command: Export revenue data to XLSX or CSV
export_revenue_parser = subparsers.add_parser('export-revenue', help='Export revenue data to XLSX or CSV.')
export_revenue_parser.add_argument('start_date', type=str, help='Starting date. (YYYY-MM-DD)')
export_revenue_parser.add_argument('end_date', type=str, help='End date. (YYYY-MM-DD)')
export_revenue_parser.add_argument('--format', '-f', type=str, choices=['csv', 'xlsx'], default='xlsx', help='Export format')
export_revenue_parser.add_argument('--output', '-o', type=str, help='Path to the output file.', nargs='?', default=None)

# 'report-profit' command: Generate profit report
profit_report_parser = subparsers.add_parser('report-profit', help='Generate profit report.')
profit_report_parser.add_argument('period', choices=['day', 'month', 'year', 'all', 'product'], help='Period for profit report.')
profit_report_parser.add_argument('value', type=str, nargs='?', default=None, help='Specific value for a period (YYYY-MM-DD for the day, YYYY-MM for the month, YYYY for a year, product name for the product)')

# 'export-profit' command: Export profit report to XLSX or CSV
export_profit_parser = subparsers.add_parser('export-profit', help='Export profit report to XLSX or CSV.')
export_profit_parser.add_argument('period', choices=['day', 'month', 'year', 'all', 'product'], help='Period for profit report.')
export_profit_parser.add_argument('value', type=str, nargs='?', default=None, help='Specific value for a period. (YYYY-MM-DD for the day, YYYY-MM for the month, YYYY for a year, product name for the product)')
export_profit_parser.add_argument('--format', '-f', type=str, choices=['csv', 'xlsx'], default='xlsx', help='Export format.')
export_profit_parser.add_argument('--output', '-o', type=str, help='Path to the output file.', nargs='?', default=None)


def calculate_inventory():
    # Calculate inventory based on purchases and sales data
    today = get_today()
    bought_data = read_csv(BOUGHT_FILE_PATH)
    sold_data = read_csv(SOLD_FILE_PATH)

    inventory = {}
    for row in bought_data:
        try:
            buy_date = datetime.strptime(row['date'], '%Y-%m-%d')
        except KeyError:
            custom_print("Invalid format of the bought file .csv - missing 'date'.")
            return

        expiration_date = datetime.strptime(row['expiration_date'], '%Y-%m-%d')

        if buy_date <= today and expiration_date >= today:
            product = row['product']
            quantity = int(row['quantity'])
            if product in inventory:
                inventory[product]['quantity'] += quantity
            else:
                inventory[product] = {'quantity': quantity, 'expiration_date': row['expiration_date']}
    
    for row in sold_data:
        sell_date = datetime.strptime(row['date'], '%Y-%m-%d')
        if sell_date <= today:
            product = row['product']
            quantity = int(row['quantity'])
            if product in inventory:
                inventory[product]['quantity'] -= quantity
                if inventory[product]['quantity'] <= 0:
                    del inventory[product]

    inventory_data = [{'product': key, 'quantity': value['quantity'], 'expiration_date': value['expiration_date']} for key, value in inventory.items()]
    update_csv(INVENTORY_FILE_PATH, inventory_data)

def custom_print(message):
    # Custom print function that considers the date context
    today = get_today()
    real_today = datetime.today()
    if today.date() != real_today.date():
        print(f"{message} (Date context: {today.strftime('%Y-%m-%d')})")
    else:
        print(message)

def get_time_shift():
    # Get the time shift value from the 'time_shift.txt' file or return 0 if not found
    try:
        with open(TIME_SHIFT_FILE, 'r') as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def set_time_shift(days):
    # Set the time shift value in the 'time_shift.txt' file
    with open(TIME_SHIFT_FILE, 'w') as file:
        file.write(str(days))

def reset_time_shift():
    # Reset the time shift value to 0
    set_time_shift(0)

def get_today():
    # Get the current date adjusted by the time shift
    return datetime.today() + timedelta(days=get_time_shift())

def generate_id(filepath):
    # Generate a unique ID based on existing data in the specified CSV file
    data = read_csv(filepath)
    if not data:
        return 1
    ids = [int(row['id']) for row in data]
    return max(ids) + 1

def write_csv(filepath, data, mode='a'):
    # Write data to a CSV file, creating it if it doesn't exist
    file_exists = os.path.isfile(filepath)
    with open(filepath, mode, newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id'] + list(data.keys()))
        if not file_exists or mode == 'w':
            writer.writeheader()
        writer.writerow({'id': generate_id(filepath), **data})

def update_csv(filepath, data):
    # Update a CSV file with new data
    with open(filepath, 'w', newline='') as file:
        if not data:
            return
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def read_csv(filepath):
    # Read data from a CSV file and return it as a list of dictionaries
    data = []
    try:
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                reader = csv.DictReader(file)
                data = list(reader)
    except Exception as e:
        custom_print(f"Error reading CSV file: {e}")
    return data

def export_xlsx(filepath, data):
    # Export data to an XLSX file
    try:
        wb = Workbook()
        ws = wb.active
        if data:
            ws.append(list(data[0].keys()))
            for row in data:
                ws.append(list(row.values()))
        wb.save(filepath)
    except Exception as e:
        custom_print(f"Error exporting to XLSX: {e}")

def export_csv(filepath, data):
     # Export data to a CSV file
    try:
        if not data:
            return
        with open(filepath, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        custom_print(f"Error exporting to CSV: {e}")

def export_data(filepath, data, format='xlsx'):
    # Export data to either XLSX or CSV format based on user choice
    if format == 'xlsx':
        export_xlsx(filepath, data)
    elif format == 'csv':
        export_csv(filepath, data)
def generate_revenue_report(start_date, end_date):
    try:
        # Read sold data from the 'sold.csv' file
        sold_data = read_csv(SOLD_FILE_PATH)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter sold data within the specified date range
        filtered_data = [row for row in sold_data if start_date <= datetime.strptime(row['date'], '%Y-%m-%d') <= end_date]
        
        # Calculate total revenue and display it in a PrettyTable
        total_revenue = sum(int(row['quantity']) * float(row['price']) for row in filtered_data)
        table = PrettyTable()
        table.field_names = ["Start Date", "End Date", "Total Revenue"]
        table.add_row([start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), total_revenue])
        custom_print(str(table))
    except Exception as e:
        custom_print(f"Error generating revenue report: {e}")

def export_revenue_data(start_date, end_date, filepath, format='xlsx'):
    try:
        # Read sold data from the 'sold.csv' file
        sold_data = read_csv(SOLD_FILE_PATH)
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

        # Filter sold data within the specified date range
        filtered_data = [row for row in sold_data if start_date <= datetime.strptime(row['date'], '%Y-%m-%d') <= end_date]
        
        # Calculate total revenue and export it in the chosen format
        total_revenue = sum(int(row['quantity']) * float(row['price']) for row in filtered_data)
        report_data = [{'Start Date': start_date.strftime('%Y-%m-%d'), 'End Date': end_date.strftime('%Y-%m-%d'), 'Total Revenue': total_revenue}]
        export_data(filepath, report_data, format=format)

    except Exception as e:
        custom_print(f"Error exporting revenue data: {e}")

def calculate_profit(period, value):
    try:
        bought_data = read_csv(BOUGHT_FILE_PATH)
        sold_data = read_csv(SOLD_FILE_PATH)
        
        profits = []
        
        for sold in sold_data:
            sell_date = datetime.strptime(sold['date'], '%Y-%m-%d')
            if period == 'day' and value and sell_date.strftime('%Y-%m-%d') != value:
                continue
            elif period == 'month' and value and sell_date.strftime('%Y-%m') != value:
                continue
            elif period == 'year' and value and sell_date.strftime('%Y') != value:
                continue
            elif period == 'product' and value and sold['product'] != value:
                continue
            for bought in bought_data:
                if bought['product'] == sold['product']:
                    profit = (float(sold['price']) - float(bought['price'])) * int(sold['quantity'])
                    profits.append({'product': sold['product'], 'date': sell_date, 'profit': profit})
                    break  
        return profits
    except (ValueError, KeyError) as e:
        custom_print(f"An error occurred while calculating profit: {e}")
        return []


def generate_profit_report(profits):
    table = PrettyTable()
    table.field_names = ["Product", "Date", "Profit"]
    
    total_profit = 0
    for profit in profits:
        table.add_row([profit['product'], profit['date'].strftime('%Y-%m-%d'), profit['profit']])
        total_profit += profit['profit']
    
    custom_print(str(table))
    custom_print(f"Total Profit: {total_profit}")
def plot_revenue(start_date, end_date):
    sold_data = read_csv(SOLD_FILE_PATH)
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')
    filtered_data = [row for row in sold_data if start_date <= datetime.strptime(row['date'], '%Y-%m-%d') <= end_date]
    grouped_data = {}
    for row in filtered_data:
        grouped_data[row['date']] = grouped_data.get(row['date'], 0) + int(row['quantity']) * float(row['price'])
        
    dates = sorted(grouped_data.keys())
    revenues = [grouped_data[date] for date in dates]
    
    # Plot revenue data using Matplotlib
    plt.plot(dates, revenues, marker='o')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.title(f'Revenue from {start_date} to {end_date}')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_profit(profits):
    products = [profit['product'] for profit in profits]
    profit_values = [profit['profit'] for profit in profits]

    # Plot profit data using Matplotlib
    plt.bar(products, profit_values)
    plt.xlabel('Products')
    plt.ylabel('Profit')
    plt.title('Profit per Product')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def report_inventory():
    # Generate a report of the current inventory
    inventory_data = read_csv(INVENTORY_FILE_PATH)
    table = PrettyTable()
    table.field_names = ["Product", "Quantity", "Expiration_date"]
    for row in inventory_data:
        table.add_row([row['product'], row['quantity'], row['expiration_date']])
    custom_print(str(table))





def main():
    # Parse command-line arguments and execute the corresponding command
    args = parser.parse_args()
    current_date = get_today().strftime('%Y-%m-%d')


    if args.command == 'buy':
        # Handle 'buy' command
        data = {
            'product': args.product,
            'quantity': args.quantity,
            'price': args.price,
            'date': args.date if args.date else current_date,
            'expiration_date': args.expiration_date,
        }
        write_csv(BOUGHT_FILE_PATH, data)
        calculate_inventory()

    elif args.command == 'sell':
        # Handle 'sell' command
        data = read_csv(BOUGHT_FILE_PATH)
        available_quantity = sum(int(row['quantity']) for row in data if row['product'] == args.product)

        if available_quantity < args.quantity:
            custom_print('Insufficient quantity in stock.')
            return

        data = {
            'product': args.product,
            'quantity': args.quantity,
            'price': args.price,
            'date': args.date if args.date else current_date,
        }
        write_csv(SOLD_FILE_PATH, data)
        calculate_inventory()

    elif args.command == 'report':
        # Handle 'report' command
        custom_print("Generating a report...")
        data = read_csv(BOUGHT_FILE_PATH if args.type == 'bought' else SOLD_FILE_PATH if args.type == 'sold' else INVENTORY_FILE_PATH)
        table = PrettyTable()
        if args.type == "inventory":
            calculate_inventory() 
            report_inventory()
        if data:
            table.field_names = list(data[0].keys())
            for row in data:
                table.add_row(list(row.values()))
        custom_print(str(table))

    elif args.command == 'export':
        # Handle 'export' command
        custom_print("Exporting data...")
        data = read_csv(BOUGHT_FILE_PATH if args.type == 'bought' else SOLD_FILE_PATH if args.type == 'sold' else INVENTORY_FILE_PATH)
        filepath = args.output or f"{args.type}_data.{args.format}"
        export_data(filepath, data, format=args.format)

    elif args.command == 'advance-time':
          # Handle 'advance-time' command
        if args.days == 'now':
            reset_time_shift()
        else:
            set_time_shift(get_time_shift() + int(args.days))
        custom_print(f"Current date set to: {get_today().strftime('%Y-%m-%d')}")
    elif args.command == 'report-revenue':
        # Handle 'report-revenue' command
        custom_print("Generating a revenue report...")
        generate_revenue_report(args.start_date, args.end_date)
        plot_revenue(args.start_date, args.end_date)

    elif args.command == 'export-revenue':
        # Handle 'export-revenue' command
        custom_print("Export a revenue report...")
        filepath = args.output or f"revenue_data.{args.format}"
        export_revenue_data(args.start_date, args.end_date, filepath, format=args.format)
    elif args.command == 'report-profit':
        # Handle 'report-profit' command
        custom_print("Generating a profit report...")
        profits = calculate_profit(args.period, args.value)
        generate_profit_report(profits)
        plot_profit(profits)

    elif args.command == 'export-profit':  # Support for the "export profit" command
        custom_print("Export the profit report...")
        profits = calculate_profit(args.period, args.value)
        filepath = args.output or f"profit_data.{args.format}"
        export_data(filepath, profits, format=args.format)

if __name__ == '__main__':
    main()
