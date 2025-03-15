import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
from utils.load_crop_data import load_crop_data
from utils.parser import save_json

# Function to convert string to number if possible
def convert_to_number(value):
    try:
        if value.strip() == "":
            return ""
        if '.' in value:  
            return float(value)
        else:
            return int(value)  
    except ValueError:
        return value  

# Function to get the days of the current month (up to today)
def get_current_month_days():
    today = datetime.now()
    current_day = today.day
    # Return days from 1 to the current day (assuming future dates are not available)
    return list(range(1, current_day + 1))

# Path to ChromeDriver
driver_path = r"D:\chromedriver-win64\chromedriver-win64\chromedriver.exe" 

# Set Chrome options
options = Options()

# Set up the service object with ChromeDriver path
service = Service(driver_path)

# Initialize WebDriver with the Service object
driver = webdriver.Chrome(service=service, options=options)

# Load crop data from the file (crop_dict.txt)
crop_data = load_crop_data('crop_dict.txt')  # Ensure this file contains your crop data

# Get the days of the current month (up to today)
month_days = get_current_month_days()

# Iterate over each day in the current month
for day in month_days:
    try:
        # Open the government website
        url = "https://agmarknet.gov.in/PriceAndArrivals/CommodityWiseDailyReport.aspx"
        driver.get(url)

        # Click the link with the specific day
        elem = driver.find_element(By.LINK_TEXT, str(day))
        elem.click()

        # Wait for the "Submit" link to be present and click it
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cphBody_Submit_list"))
        )
        element.click()

        # Iterate through each crop's checkbox ID and select the checkbox
        for crop_name, crop_id in crop_data.items():
            print(f"Attempting to select checkbox for crop: {crop_name}, ID: {crop_id}")
            try:
                crop_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, crop_id))
                )
                if not crop_checkbox.is_selected():  
                    crop_checkbox.click()
                    print(f"Successfully selected checkbox for {crop_name}.")
                else:
                    print(f"Checkbox for {crop_name} was already selected.")
            except Exception as e:
                print(f"Could not select checkbox for {crop_name}: {e}")

        # Wait for the "Submit" button and click it
        submit_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cphBody_btnSubmit"))
        )
        submit_button.click()

        # Wait for the table with <tr> elements to be fully loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cphBody_GridView1"))
        )

        # Find all the <tr> elements within the table
        table_rows = driver.find_elements(By.XPATH, "//table[@id='cphBody_GridView1']//tr")

        # List to store the data in dictionary format
        data = []

        # Assuming the first row contains the column headers
        headers = [header.text for header in table_rows[0].find_elements(By.XPATH, ".//th")]

        # Loop through the rows and create a dictionary for each row
        for row in table_rows[1:]:  # Skip the header row
            row_data = [cell.text for cell in row.find_elements(By.XPATH, ".//td")]
            if row_data:  
                row_dict = {}
                for i, header in enumerate(headers):
                    if i < len(row_data):
                        row_dict[header] = convert_to_number(row_data[i])
                    else:
                        row_dict[header] = ""
                # Add the day (date) to each record
                row_dict["Date"] = day
                data.append(row_dict)

        # Save the data to a CSV file
        if data:
            # Determine the fieldnames; ensure "Date" is included
            fieldnames = headers.copy()
            if "Date" not in fieldnames:
                fieldnames.append("Date")
            csv_filename = f"crop_data_{day}.csv"
            with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            print(f"Data for day {day} has been saved to '{csv_filename}'.")
            save_json(csv_filename)
            print(f"Json saved.")
        else:
            print(f"No data available for day {day}.")

    except Exception as e:
        print(f"Error during interaction with the page for day {day}: {e}")

    # Optional: Wait to avoid being detected as a bot
    time.sleep(5)

# Quit the driver after processing all days
driver.quit()

# Wait for user input before exiting (if needed)
input("Press Enter to exit...")
