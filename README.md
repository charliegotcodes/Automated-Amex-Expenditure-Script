# Automated Amex Statement Spending Report

This script automates the process of generating a spending report for your American Express account. It produces a pie chart that visually displays:

* The amount spent that has already been paid.
* The remaining balance that is left to be paid.
* The script connects to your Gmail account, retrieves the latest statement notification, downloads the transaction data, processes it, and creates the report.

__________________________________________________________________________________________________________________

# Features 

* Automatic Email Retrieval
  1. Utilizing Gmail API to access your inbox and locate your latest Amex statement email.
    
* CSV File Handling
  1. Downloads the latest CSV file from the Amex website
  2. Saves file with the statement date for easy reference
  3. Moves the file to a storage of all previous statements
     
* Data Analysis
  1. Process the CSV of the statement using Pandas
  2. Total Amount spent on the statement
  3. Total Amount paid so Far
 
* Visual Report
  1. Pie chart generation using Matplotlib
  2. Displays two categories of: Paid Amount, Remaining Balance

__________________________________________________________________________________________________________________

