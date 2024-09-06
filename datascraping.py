from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import pandas as pd
import time

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)  # Increased timeout

# Open the webpage
driver.get("https://www.redbus.in/online-booking/uttar-pradesh-state-road-transport-corporation-upsrtc/?utm_source=rtchometile")

def collect_route_details():
    try:
        # Wait until the route elements are present
        route_elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@class='route']"))
        )
        
        route_details = []
        for element in route_elements:
            route_name = element.text  # Extract the route name
            route_link = element.get_attribute('href')  # Extract the route link
            route_details.append({'Route_name': route_name, 'Route_link': route_link})

        return route_details
    except Exception as e:
        print(f"An error occurred while collecting route details: {e}")
        return []

def navigate_and_collect_data():
    all_route_details = []

    for page_number in range(1, 6):  # Loop from page 1 to 5
        try:
            # Collect route details from the current page
            print(f"Collecting data from page {page_number}...")
            route_details = collect_route_details()
            all_route_details.extend(route_details)

            if page_number < 5:  # Don't attempt to click next on the last page
                # Locate the pagination container
                pagination_container = wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="root"]/div/div[4]/div[12]')
                ))

                # Locate the next page button within the container
                next_page_button = pagination_container.find_element(
                    By.XPATH, f'.//div[contains(@class, "DC_117_pageTabs") and text()="{page_number + 1}"]'
                )

                # Ensure the next page button is in view
                actions = ActionChains(driver)
                actions.move_to_element(next_page_button).perform()
                time.sleep(1)  # Wait for a bit after scrolling

                # Click the next page button
                next_page_button.click()

                # Wait for the page number to update to the next page
                wait.until(EC.text_to_be_present_in_element(
                    (By.XPATH, '//div[contains(@class, "DC_117_pageTabs DC_117_pageActive")]'), str(page_number + 1)
                ))
                print(f"Successfully navigated to page {page_number + 1}")

                # Wait for a short duration to ensure the next page loads completely
                time.sleep(3)

        except TimeoutException:
            print(f"TimeoutException: Page navigation or data collection failed on page {page_number}.")
        except NoSuchElementException:
            print(f"NoSuchElementException: Pagination element not found on page {page_number}.")
        except Exception as e:
            print(f"An error occurred while navigating or collecting data: {e}")

    return all_route_details

# Collect data across all pages
all_route_details = navigate_and_collect_data()

# Convert to DataFrame
dfup= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\up_route details_new.csv"

try:
    dfup.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfup = pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfup)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 
def scroll_and_collect():
    last_height = driver.execute_script("return document.body.scrollHeight")     
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:             
            break         
        last_height = new_height
#retrive the bus details
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 30)

Bus_names_up = []
Bus_types_up= []
Start_Time_up = []
End_Time_up = []
Ratings_up = []
Duration_up = []
Price_up = []
Seats_up = []
Route_names_up = []
Route_links_up = []



for i,r in dfup.iterrows():
    link=r["Route_link"]
    routes=r["Route_name"]

# Loop through each link
    driver.get(link)
    time.sleep(2)  

    # Click on elements to reveal bus details
    elements = driver.find_elements(By.XPATH, f"//a[contains(@href, '{link}')]")
    for element in elements:
        element.click()
        time.sleep(2)
        
    # click elements to views bus
    try:
        clicks = driver.find_element(By.XPATH, "//div[@class='button']")
        clicks.click()
    except:
        continue  
    time.sleep(2)
    
    scrolling = True
    while scrolling:
        old_page_source = driver.page_source
        
        # Use ActionChains to perform a PAGE_DOWN
        ActionChains(driver).send_keys(Keys.PAGE_DOWN).perform()
        
        time.sleep(5)  
        
        new_page_source = driver.page_source
        
        if new_page_source == old_page_source:
            scrolling = False

    # Extract bus details
    busname = driver.find_elements(By.XPATH, "//div[@class='travels lh-24 f-bold d-color']")
    bustype = driver.find_elements(By.XPATH, "//div[@class='bus-type f-12 m-top-16 l-color evBus']")
    departing_time = driver.find_elements(By.XPATH, "//*[@class='dp-time f-19 d-color f-bold']")
    reaching_time = driver.find_elements(By.XPATH, "//*[@class='bp-time f-19 d-color disp-Inline']")
    duration = driver.find_elements(By.XPATH, "//*[@class='dur l-color lh-24']")
    try:
        star_rating = driver.find_elements(By.XPATH,"//div[@class='clearfix row-one']/div[@class='column-six p-right-10 w-10 fl']")
    except:
        continue
    price = driver.find_elements(By.XPATH, '//*[@class="fare d-block"]')
    seat_availability = driver.find_elements(By.XPATH, "//div[contains(@class, 'seat-left')]")

    # Append data to respective lists
    for bus in busname:
        Bus_names_up.append(bus.text)
        Route_links_up.append(link)
        Route_names_up.append(routes)
    for bus_type_elem in bustype:
        Bus_types_up.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_up.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_up.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_up.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_up.append(ratings.text)
    for price_elem in price:
        Price_up.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_up.append(seats_elem.text)
        
print("Successfully Completed")
data_up = {
    "busname": Bus_names_up,
    "bustype": Bus_types_up,
    "departing_time": Start_Time_up,
    "duration": Duration_up,
    "reaching_time": End_Time_up,
    "price": Price_up,
    "seat_availability": Seats_up,
    "star_rating": Ratings_up,
    "R_name": Route_names_up,
    "link": Route_links_up}
df_next_up= pd.DataFrame(data_up)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\up_route_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_up.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_up)


