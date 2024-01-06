from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os 
import warnings 
import re 
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from glob import glob

import pandas as pd
import matplotlib.pyplot as plt

options = Options()

# Insert the directory to your downloads 



options.add_argument("--start-maximized")
options.add_argument('log-level=3')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_experimental_option("detach", True)
options.add_experimental_option("prefs", {
    "download.default_directory": "../Python Automation/CSV_Files",
    "download.prompt_for_download": False,  # Enable download prompt (optional)
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})
# Insert the path to your chromedriver (In this case I had put the driver in a folder called correcter within my project folder Python Automation)
driver_path = os.path.abspath("../Python Automation/correcter/chromedriver")
options.add_argument(f"executable_path={driver_path}")

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(executable_path=driver_path), options=options)
load_dotenv()
gmail = Gmail()


# The URLS to the CSV download page and the Login page
csv_download_url = "https://global.americanexpress.com/myca/intl/download/canlac/download.do?request_type=&Face=en_CA&sorted_index=0"
login_url = "https://www.americanexpress.com/en-ca/account/login?inav=ca_utility_login"

# Retrieves sensitive information in this case the Username and Password for my AMEX Account from a .env file 
Username = os.getenv('USER_NAME')
Password = os.getenv('PASS')


required_url= ""

# Notes all the requirements for the specific email needed for this script 

query_params_1 = {
    'sender': 'DoNotReplyCA@welcome.americanexpress.com',
#   'newer_than': (2, 'days'),
    'exact_phrase': 'Your Statement is now ready'
}

# Removes all user warnings regarding the bs4 module 

warnings.filterwarnings("ignore", category=UserWarning, module="bs4")

# contains the emails that satisfy the query parameters
  
messages = gmail.get_messages(query=construct_query(query_params_1))

# prints each email that satisfies the parameters 

print(messages[0].sender)
print(messages[0].date)

# Converts the html message to string
stringified = str(messages[0].html)

# Using regex to match for the string that contains the url to login to my AMEX account
exp = re.compile(r'<a\s+href="([^"]+)"')
m = exp.search(stringified)
required_url = m.group(1)

print("Logging in")

# Wait for the login fields and button to load
driver.get(csv_download_url)
try:
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "eliloUserID"))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "eliloPassword"))
    )
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "loginSubmit"))
    )
except Exception:
    print(f"Ran into error waiting for the login form to load") 
    exit()

driver.find_element(By.NAME, 'eliloUserID').send_keys(Username)
driver.find_element(By.NAME, 'eliloPassword').send_keys(Password)
log = driver.find_element(By.ID, 'loginSubmit').click()
print("Finished logging in")

# Waits for the CSV option to be clickable 

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "CSV"))
)
CSV_element = driver.find_element(By.ID, 'CSV')
CSV_element.click()

# Waits for the account linked to my card to be clickable 

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "selectCard10"))
)
Account_element = driver.find_element(By.ID, 'selectCard10')
Account_element.click()

# Waits for the Current Month CSV file option to be clickable 

WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "radioid00"))
)
Month_element = driver.find_element(By.ID, 'radioid00')
Month_element.click()

date = ""
First = 0
if First == 0:
    date = driver.find_element(By.CLASS_NAME, 'stmt').text
    First = 1


# The JavaScript code to trigger the download
javascript_code = "formSubmit1('1', '7');"


driver.execute_script(javascript_code)


download_direct = '/Users/kevincharles/Downloads'

# Insert the directory to your destination folder 

destination_direct = '../Python Automation/CSV_Files'


found = glob(os.path.join(download_direct, '*ofx*'))
found = [f for f in found if os.path.isfile(f)]
found.sort(key=os.path.getmtime, reverse=True)

if found:
    latest_statement = found[0]
    print("Latest statement found:", latest_statement)
    
    current_path = os.path.join(download_direct, latest_statement)

    # Ensure 'date' is not an empty string before creating the destination path
    if date:
        final_dest = os.path.join(destination_direct, date + '.csv')
        shutil.move(current_path, final_dest)
        print("Success: File moved to", final_dest)
    else:
        print("Error: 'date' is empty.")
else:
    print("Error: No files found in Downloads folder.")



data = pd.read_csv(final_dest)
data = data.iloc[:, :-2]
data.columns = ["Date", "ID", "Expenditure","Location"]
driver.quit()

spent = 0
paid = 0 

for val in data['Expenditure']: 
    if val < 0: 
        paid += abs(val)
    else: 
        spent += val 

if (spent > paid): 
    print("You've spent ${:.2f} in excess".format((spent - paid)))
else: 
    print("You've paid off your statement")

labels = ['Spent', 'Paid']
Values = [ spent, paid]

light_red = '#FF9999'
light_blue = '#9999FF'

plt.pie(Values, labels=labels, autopct='%1.1f%%', startangle=90, colors=[light_red, light_blue])


title_font = {
    'family': 'sans-serif',  
    'color': 'blue',          
    'weight': 'bold',         
    'size': 20               
}

plt.title('Amex Card Expenditure', fontdict=title_font)
sentence = "Total Owed: ${:.2f}".format(spent - paid)
plt.text(-0.2, -1.6, sentence, ha='center', va='bottom', fontsize=12, color='black')

# Show the pie chart

plt.show()

