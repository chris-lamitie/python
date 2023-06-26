#!/usr/bin/env python3
#################################################
# Christopher Lamitie, 2023-06-23
# a reporting log parser written for educational purposes
# 
# what we are doing here is parsing csv log data into a summary format
# We have to figure out the name of the excahanges and total the byte
# sizes of multiple files on the same day, from the same excahnge
# we also have to sort the dates when they are out of order and 
# deal with error conditions like errant commas and file that have
# a different format.
#
# see the files test_data_[0-7] in the local directory for data
# and formatting items.
#################################################

# import other needed modules
import sys
import re
import os

# variables
debug = 0
file_format_exception = 0

# Get the current directory
current_directory = os.getcwd()

# Get the list of files and directories in the current directory but ignore python scripts
directory_contents = [item for item in os.listdir(current_directory) if not item.endswith('.py')]

# Print the directory contents
print("Here are the contents of the current directory:")
for item in directory_contents:
    print(item)
print(" ")

# Ask the user for input from the command line of the directory contents
user_input = input("Enter one of the file names from the above list: ")

print("Processing:",user_input)

with open(user_input, 'r') as file:
    # Read the contents of the file
    csv_input = file.read()

# Split the input into lines
log_lines = csv_input.splitlines()

# Reading the input data we are working with
if debug == 1:
    for row in log_lines:
        print(row)

# Testing if we have a file format exception to the norm
# we are expecting: date,process,host,log,bytes
# but may see: process,date,host,bytes,log
test_line = log_lines[0].split(',')
if debug == 1:
    print("log_lines[0]:",log_lines[0])
    print("test_line[0]:",test_line[0])
if test_line[0] == "process":
    # 'process' in the header field tells us we have a differnt input format
    file_format_exception = 1
    if debug == 1: 
        print("'process' found. We have an exception")
        
# Initialize an empty result list
log_results = []

# Iterate over the lines, starting from the second line because the first is a header row
for current_line in log_lines[1:]:
    # Use regular expressions to remove commas between double quotes
    current_line = re.sub(r'"([^"]*)"', lambda x: x.group(1).replace(',', ''), current_line)

    # Split the line using a comma as the delimiter
    line_elements = current_line.split(',')
    
    # Extract relevant values
    if file_format_exception == 1:
        log_date = line_elements[1]
        process = line_elements[0]
        host = line_elements[2]
        bytes_value = int(line_elements[3])
    else:
        log_date = line_elements[0]
        process = line_elements[1]
        host = line_elements[2]
        bytes_value = int(line_elements[4]) # this is the size of the gz log file on the current line we are reading
    
    # Extract the exchange name from the process value, splitting on the first "_"
    exchange = process.split('_')[0]

    # Check if the date-exchange combination already exists in the result
    existing_row = next((row for row in log_results if row[0] == log_date and row[1] == exchange), None)

    if existing_row:
        # If the row already exists, add the bytes_value to the existing total_bytes
        existing_row[2] += bytes_value
    else:
        # If the row doesn't exist, create a new row with the date, exchange, and bytes_value
        log_results.append([log_date, exchange, bytes_value])

# Print the header
print("date,exchange,total_bytes")

# Sort the totals list based on the date in ascending order
log_results = sorted(log_results, key=lambda x: x[0])

# Print the cumulative totals
for item in log_results:
    print(f'{item[0]},{item[1]},{item[2]}')
