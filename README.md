# Automated-Amex-Expenditure-Script

This scripts job is to automatically produce a report of a pie chart that displays your current spending on your amex account with two categories of how much has been paid and how much is left to be paid. 

It accomplishes this by utilizing the gmail API to connect to your gmail and sift and find the most recent email of your new statement being available. After finding that email it navigates to the page to the download your current data as a CSV file. 

It then performs file handling by moving the downloaded file from the original download file to the destination directory and saving the file by the date of the statement that was scraped from the Amex Website during download. 

After moving the .CSV file we utilize the pandas dataframe to work with the data and extract the amount that has been spent and the amount that has been paid thus far on the statement. 

Then utilizing the matplotlib library we construct a pie chart and display our current spending and how much is left to be paid.
