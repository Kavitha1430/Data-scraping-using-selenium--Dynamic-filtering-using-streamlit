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

#kadamba
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
driver.get("https://www.redbus.in/online-booking/ktcl/?utm_source=rtchometile")

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

    for page_number in range(1, 5):  # Loop from page 1 to 5
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
dfkd= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\kadamba_bus_route.csv"

try:
    dfkd.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfkd= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfkd)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_kd = []
Bus_types_kd= []
Start_Time_kd = []
End_Time_kd = []
Ratings_kd = []
Duration_kd = []
Price_kd = []
Seats_kd = []
Route_names_kd = []
Route_links_kd = []



for i,r in dfkd.iterrows():
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
        Bus_names_kd.append(bus.text)
        Route_links_kd.append(link)
        Route_names_kd.append(routes)
    for bus_type_elem in bustype:
        Bus_types_kd.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_kd.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_kd.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_kd.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_kd.append(ratings.text)
    for price_elem in price:
        Price_kd.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_kd.append(seats_elem.text)
        
print("Successfully Completed")

data_kd = {
    "busname": Bus_names_kd,
    "bustype": Bus_types_kd,
    "departing_time": Start_Time_kd,
    "duration": Duration_kd,
    "reaching_time": End_Time_kd,
    "price": Price_kd,
    "seat_availability": Seats_kd,
    "star_rating": Ratings_kd,
    "R_name": Route_names_kd,
    "link": Route_links_kd}
df_next_kd= pd.DataFrame(data_kd)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\kd_route_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_kd.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_kd)

#south bengal
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
driver.get("https://www.redbus.in/online-booking/south-bengal-state-transport-corporation-sbstc/?utm_source=rtchometile")

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
dfsb = pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\sb_rote details_new.csv"

try:
    dfsb.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfsb = pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfsb)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit()  #00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

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

Bus_names_sb = []
Bus_types_sb= []
Start_Time_sb = []
End_Time_sb = []
Ratings_sb = []
Duration_sb = []
Price_sb = []
Seats_sb = []
Route_names_sb = []
Route_links_sb = []



for i,r in dfsb.iterrows():
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
        Bus_names_sb.append(bus.text)
        Route_links_sb.append(link)
        Route_names_sb.append(routes)
    for bus_type_elem in bustype:
        Bus_types_sb.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_sb.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_sb.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_sb.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_sb.append(ratings.text)
    for price_elem in price:
        Price_sb.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_sb.append(seats_elem.text)
        
print("Successfully Completed")

data_sb = {
    "busname": Bus_names_sb,
    "bustype": Bus_types_sb,
    "departing_time": Start_Time_sb,
    "duration": Duration_sb,
    "reaching_time": End_Time_sb,
    "price": Price_sb,
    "seat_availability": Seats_sb,
    "star_rating": Ratings_sb,
    "R_name": Route_names_sb,
    "link": Route_links_sb}
df_next_sb= pd.DataFrame(data_sb)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\sb_route_details.csv"


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
print(df_next_sb)

#telangana

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
driver.get("https://www.redbus.in/online-booking/tsrtc/?utm_source=rtchometile")

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

    for page_number in range(1, 4):  # Loop from page 1 to 5
        try:
            # Collect route details from the current page
            print(f"Collecting data from page {page_number}...")
            route_details = collect_route_details()
            all_route_details.extend(route_details)

            if page_number < 3:  # Don't attempt to click next on the last page
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
dftl = pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\tl_rote details_new.csv"

try:
    dftl.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dftl = pd.read_csv(path)
    print("Collected Bus Data:")
    print(dftl)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_tl = []
Bus_types_tl= []
Start_Time_tl = []
End_Time_tl = []
Ratings_tl = []
Duration_tl = []
Price_tl = []
Seats_tl = []
Route_names_tl = []
Route_links_tl = []



for i,r in dftl.iterrows():
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
        Bus_names_tl.append(bus.text)
        Route_links_tl.append(link)
        Route_names_tl.append(routes)
    for bus_type_elem in bustype:
        Bus_types_tl.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_tl.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_tl.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_tl.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_tl.append(ratings.text)
    for price_elem in price:
        Price_tl.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_tl.append(seats_elem.text)
        
print("Successfully Completed")

data_tl = {
    "busname": Bus_names_tl,
    "bustype": Bus_types_tl,
    "departing_time": Start_Time_tl,
    "duration": Duration_tl,
    "reaching_time": End_Time_tl,
    "price": Price_tl,
    "seat_availability": Seats_tl,
    "star_rating": Ratings_tl,
    "R_name": Route_names_tl,
    "link": Route_links_tl}
df_next_tl= pd.DataFrame(data_tl)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\tl_route_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_tl.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_tl)

#himachal pradesh

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
driver.get("https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile")

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
dfhm= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\hm_rote details_new.csv"

try:
    dfhm.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfhm = pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfhm)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_hm = []
Bus_types_hm= []
Start_Time_hm = []
End_Time_hm = []
Ratings_hm = []
Duration_hm = []
Price_hm = []
Seats_hm = []
Route_names_hm = []
Route_links_hm = []



for i,r in dfhm.iterrows():
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
        Bus_names_hm.append(bus.text)
        Route_links_hm.append(link)
        Route_names_hm.append(routes)
    for bus_type_elem in bustype:
        Bus_types_hm.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_hm.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_hm.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_hm.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_hm.append(ratings.text)
    for price_elem in price:
        Price_hm.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_hm.append(seats_elem.text)
        
print("Successfully Completed")

data_hm = {
    "busname": Bus_names_hm,
    "bustype": Bus_types_hm,
    "departing_time": Start_Time_hm,
    "duration": Duration_hm,
    "reaching_time": End_Time_hm,
    "price": Price_hm,
    "seat_availability": Seats_hm,
    "star_rating": Ratings_hm,
    "R_name": Route_names_hm,
    "link": Route_links_hm}
df_next_hm= pd.DataFrame(data_hm)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\hm_route_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_hm.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_hm)

#assam

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
driver.get("https://www.redbus.in/online-booking/astc/?utm_source=rtchometile")

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
dfas= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\as_route details_new.csv"

try:
    dfas.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfas = pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfas)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_as = []
Bus_types_as= []
Start_Time_as = []
End_Time_as = []
Ratings_as = []
Duration_as = []
Price_as = []
Seats_as = []
Route_names_as = []
Route_links_as = []



for i,r in dfas.iterrows():
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
        Bus_names_as.append(bus.text)
        Route_links_as.append(link)
        Route_names_as.append(routes)
    for bus_type_elem in bustype:
        Bus_types_as.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_as.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_as.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_as.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_as.append(ratings.text)
    for price_elem in price:
        Price_as.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_as.append(seats_elem.text)
        
print("Successfully Completed")

data_as = {
    "busname": Bus_names_as,
    "bustype": Bus_types_as,
    "departing_time": Start_Time_as,
    "duration": Duration_as,
    "reaching_time": End_Time_as,
    "price": Price_as,
    "seat_availability": Seats_as,
    "star_rating": Ratings_as,
    "R_name": Route_names_as,
    "link": Route_links_as}
df_next_as= pd.DataFrame(data_as)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\as_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_as.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_as)

#andhra pradesh

#andhra
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
driver.get("https://www.redbus.in/online-booking/apsrtc/?utm_source=rtchometile")

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
dfap= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\ap_route details_new.csv"

try:
    dfap.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfap= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfap)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_ap = []
Bus_types_ap= []
Start_Time_ap = []
End_Time_ap = []
Ratings_ap = []
Duration_ap = []
Price_ap = []
Seats_ap = []
Route_names_ap = []
Route_links_ap = []



for i,r in dfap.iterrows():
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
        Bus_names_ap.append(bus.text)
        Route_links_ap.append(link)
        Route_names_ap.append(routes)
    for bus_type_elem in bustype:
        Bus_types_ap.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_ap.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_ap.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_ap.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_ap.append(ratings.text)
    for price_elem in price:
        Price_ap.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_ap.append(seats_elem.text)
        
print("Successfully Completed")

data_ap = {
    "busname": Bus_names_ap,
    "bustype": Bus_types_ap,
    "departing_time": Start_Time_ap,
    "duration": Duration_ap,
    "reaching_time": End_Time_ap,
    "price": Price_ap,
    "seat_availability": Seats_ap,
    "star_rating": Ratings_ap,
    "R_name": Route_names_ap,
    "link": Route_links_ap}
df_next_ap= pd.DataFrame(data_ap)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\ap_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_ap.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_ap)

#kerala

#kerala
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
driver.get("https://www.redbus.in/online-booking/ksrtc-kerala/?utm_source=rtchometile")

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

    for page_number in range(1, 3):  # Loop from page 1 to 5
        try:
            # Collect route details from the current page
            print(f"Collecting data from page {page_number}...")
            route_details = collect_route_details()
            all_route_details.extend(route_details)

            if page_number < 2:  # Don't attempt to click next on the last page
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
dfkl= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\kl_route details_new.csv"

try:
    dfkl.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfkl= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfkl)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_kl = []
Bus_types_kl= []
Start_Time_kl = []
End_Time_kl = []
Ratings_kl = []
Duration_kl = []
Price_kl = []
Seats_kl = []
Route_names_kl = []
Route_links_kl = []



for i,r in dfkl.iterrows():
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
        Bus_names_kl.append(bus.text)
        Route_links_kl.append(link)
        Route_names_kl.append(routes)
    for bus_type_elem in bustype:
        Bus_types_kl.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_kl.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_kl.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_kl.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_kl.append(ratings.text)
    for price_elem in price:
        Price_kl.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_kl.append(seats_elem.text)
        
print("Successfully Completed")

data_kl = {
    "busname": Bus_names_kl,
    "bustype": Bus_types_kl,
    "departing_time": Start_Time_kl,
    "duration": Duration_kl,
    "reaching_time": End_Time_kl,
    "price": Price_kl,
    "seat_availability": Seats_kl,
    "star_rating": Ratings_kl,
    "R_name": Route_names_kl,
    "link": Route_links_kl}
df_next_kl= pd.DataFrame(data_kl)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\kl_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_kl.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_kl)

#rajasthan

#rajasthan
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
driver.get("https://www.redbus.in/online-booking/rsrtc/?utm_source=rtchometile")

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

    for page_number in range(1, 4):  # Loop from page 1 to 5
        try:
            # Collect route details from the current page
            print(f"Collecting data from page {page_number}...")
            route_details = collect_route_details()
            all_route_details.extend(route_details)

            if page_number < 3:  # Don't attempt to click next on the last page
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
dfrj= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\rj_route details_new.csv"

try:
    dfrj.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfrj= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfrj)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_rj = []
Bus_types_rj= []
Start_Time_rj = []
End_Time_rj = []
Ratings_rj = []
Duration_rj = []
Price_rj = []
Seats_rj = []
Route_names_rj = []
Route_links_rj = []



for i,r in dfrj.iterrows():
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
        Bus_names_rj.append(bus.text)
        Route_links_rj.append(link)
        Route_names_rj.append(routes)
    for bus_type_elem in bustype:
        Bus_types_rj.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_rj.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_rj.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_rj.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_rj.append(ratings.text)
    for price_elem in price:
        Price_rj.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_rj.append(seats_elem.text)
        
print("Successfully Completed")

data_rj = {
    "busname": Bus_names_rj,
    "bustype": Bus_types_rj,
    "departing_time": Start_Time_rj,
    "duration": Duration_rj,
    "reaching_time": End_Time_rj,
    "price": Price_rj,
    "seat_availability": Seats_rj,
    "star_rating": Ratings_rj,
    "R_name": Route_names_rj,
    "link": Route_links_rj}
df_next_rj= pd.DataFrame(data_rj)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\rj_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_rj.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_rj)

#uttar pradesh

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
    dfup= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfup)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\up_bus_details.csv"


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

#west bengal
#west bengal
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
driver.get("https://www.redbus.in/online-booking/wbtc-ctc/?utm_source=rtchometile")

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
dfwb= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\wb_route details_new.csv"

try:
    dfwb.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfwb= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfwb)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_wb = []
Bus_types_wb= []
Start_Time_wb = []
End_Time_wb = []
Ratings_wb = []
Duration_wb = []
Price_wb = []
Seats_wb = []
Route_names_wb = []
Route_links_wb = []



for i,r in dfwb.iterrows():
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
        Bus_names_wb.append(bus.text)
        Route_links_wb.append(link)
        Route_names_wb.append(routes)
    for bus_type_elem in bustype:
        Bus_types_wb.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_wb.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_wb.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_wb.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_wb.append(ratings.text)
    for price_elem in price:
        Price_wb.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_wb.append(seats_elem.text)
        
print("Successfully Completed")

data_wb = {
    "busname": Bus_names_wb,
    "bustype": Bus_types_wb,
    "departing_time": Start_Time_wb,
    "duration": Duration_wb,
    "reaching_time": End_Time_wb,
    "price": Price_wb,
    "seat_availability": Seats_wb,
    "star_rating": Ratings_wb,
    "R_name": Route_names_wb,
    "link": Route_links_wb}
df_next_wb= pd.DataFrame(data_wb)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\wb_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_wb.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:  
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_wb)

#chandigarh

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
driver.get("https://www.redbus.in/online-booking/chandigarh-transport-undertaking-ctu")

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
dfch= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\ch_route details_new.csv"

try:
    dfch.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfch= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfch)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_ch = []
Bus_types_ch= []
Start_Time_ch = []
End_Time_ch = []
Ratings_ch = []
Duration_ch = []
Price_ch = []
Seats_ch = []
Route_names_ch = []
Route_links_ch = []



for i,r in dfch.iterrows():
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
        Bus_names_ch.append(bus.text)
        Route_links_ch.append(link)
        Route_names_ch.append(routes)
    for bus_type_elem in bustype:
        Bus_types_ch.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_ch.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_ch.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_ch.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_ch.append(ratings.text)
    for price_elem in price:
        Price_ch.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_ch.append(seats_elem.text)
        
print("Successfully Completed")

data_ch = {
    "busname": Bus_names_ch,
    "bustype": Bus_types_ch,
    "departing_time": Start_Time_ch,
    "duration": Duration_ch,
    "reaching_time": End_Time_ch,
    "price": Price_ch,
    "seat_availability": Seats_ch,
    "star_rating": Ratings_ch,
    "R_name": Route_names_ch,
    "link": Route_links_ch}
df_next_ch= pd.DataFrame(data_ch)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\ch_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_ch.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:  
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_ch)

#hyderabad


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
driver.get("https://www.redbus.in/online-booking/hrtc/?utm_source=rtchometile")

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
dfhr= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\hr_route details_new.csv"

try:
    dfhr.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfhr= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfhr)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_hr = []
Bus_types_hr= []
Start_Time_hr = []
End_Time_hr = []
Ratings_hr = []
Duration_hr = []
Price_hr = []
Seats_hr = []
Route_names_hr = []
Route_links_hr = []



for i,r in dfhr.iterrows():
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
        Bus_names_hr.append(bus.text)
        Route_links_hr.append(link)
        Route_names_hr.append(routes)
    for bus_type_elem in bustype:
        Bus_types_hr.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_hr.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_hr.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_hr.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_hr.append(ratings.text)
    for price_elem in price:
        Price_hr.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_hr.append(seats_elem.text)
        
print("Successfully Completed")

data_hr = {
    "busname": Bus_names_hr,
    "bustype": Bus_types_hr,
    "departing_time": Start_Time_hr,
    "duration": Duration_hr,
    "reaching_time": End_Time_hr,
    "price": Price_hr,
    "seat_availability": Seats_hr,
    "star_rating": Ratings_hr,
    "R_name": Route_names_hr,
    "link": Route_links_hr}
df_next_hr= pd.DataFrame(data_hr)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\hr_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_hr.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_hr)

#north bengal
#north bengal
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
driver.get("https://www.redbus.in/online-booking/north-bengal-state-transport-corporation")

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
dfnb= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\nb_route details_new.csv"

try:
    dfnb.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfnb= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfnb)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_nb = []
Bus_types_nb= []
Start_Time_nb = []
End_Time_nb = []
Ratings_nb = []
Duration_nb = []
Price_nb = []
Seats_nb = []
Route_names_nb = []
Route_links_nb = []



for i,r in dfnb.iterrows():
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
        Bus_names_nb.append(bus.text)
        Route_links_nb.append(link)
        Route_names_nb.append(routes)
    for bus_type_elem in bustype:
        Bus_types_nb.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_nb.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_nb.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_nb.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_nb.append(ratings.text)
    for price_elem in price:
        Price_nb.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_nb.append(seats_elem.text)
        
print("Successfully Completed")

data_nb = {
    "busname": Bus_names_nb,
    "bustype": Bus_types_nb,
    "departing_time": Start_Time_nb,
    "duration": Duration_nb,
    "reaching_time": End_Time_nb,
    "price": Price_nb,
    "seat_availability": Seats_nb,
    "star_rating": Ratings_nb,
    "R_name": Route_names_nb,
    "link": Route_links_nb}
df_next_nb= pd.DataFrame(data_nb)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\nb_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_nb.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_nb)

#punjab
#punjab
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
driver.get("https://www.redbus.in/online-booking/pepsu/?utm_source=rtchometile")

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

    for page_number in range(1, 4):  # Loop from page 1 to 5
        try:
            # Collect route details from the current page
            print(f"Collecting data from page {page_number}...")
            route_details = collect_route_details()
            all_route_details.extend(route_details)

            if page_number < 3:  # Don't attempt to click next on the last page
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
dfpj= pd.DataFrame(all_route_details, columns=['Route_name', 'Route_link'])

# Specify a different file path or name if necessary
path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\pj_route details_new.csv"

try:
    dfpj.to_csv(path, index=False)
    print(f"Data successfully saved to {path}")
except PermissionError:
    print(f"PermissionError: Unable to save file. Please check if the file is open or if you have write permissions to the path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

# Read the CSV file
try:
    dfpj= pd.read_csv(path)
    print("Collected Bus Data:")
    print(dfpj)
except FileNotFoundError:
    print(f"FileNotFoundError: The file was not found at the path {path}.")
except Exception as e:
    print(f"An error occurred while reading the file: {e}")

# Close the WebDriver
driver.quit() 

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

Bus_names_pj = []
Bus_types_pj= []
Start_Time_pj = []
End_Time_pj = []
Ratings_pj = []
Duration_pj = []
Price_pj = []
Seats_pj = []
Route_names_pj = []
Route_links_pj = []



for i,r in dfpj.iterrows():
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
        Bus_names_pj.append(bus.text)
        Route_links_pj.append(link)
        Route_names_pj.append(routes)
    for bus_type_elem in bustype:
        Bus_types_pj.append(bus_type_elem.text)
    for start_time_elem in departing_time:
        Start_Time_pj.append(start_time_elem.text)
    for end_time_elem in reaching_time:
        End_Time_pj.append(end_time_elem.text)
    for total_duration_elem in duration:
        Duration_pj.append(total_duration_elem.text)
    for ratings in star_rating:
        Ratings_pj.append(ratings.text)
    for price_elem in price:
        Price_pj.append(price_elem.text)
    for seats_elem in seat_availability:
        Seats_pj.append(seats_elem.text)
        
print("Successfully Completed")

data_pj= {
    "busname": Bus_names_pj,
    "bustype": Bus_types_pj,
    "departing_time": Start_Time_pj,
    "duration": Duration_pj,
    "reaching_time": End_Time_pj,
    "price": Price_pj,
    "seat_availability": Seats_pj,
    "star_rating": Ratings_pj,
    "R_name": Route_names_pj,
    "link": Route_links_pj}
df_next_pj= pd.DataFrame(data_pj)

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\pj_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_next_pj.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")

# Print DataFrame
print(df_next_pj)

df_busdetails_up=pd.read_csv("up_bus_details.csv")

df_busdetails_nb=pd.read_csv("nb_bus_details.csv")
df_busdetails_kl=pd.read_csv("kl_bus_details.csv")


df_busdetails_hr=pd.read_csv("hr_bus_details.csv")

df_busdetails_ch=pd.read_csv("ch_bus_details.csv")
df_busdetails_rj=pd.read_csv("rj_bus_details.csv")

df_busdetails_tl=pd.read_csv("tl_route_details.csv")
df_busdetails_sb=pd.read_csv("sb_route_details.csv")
df_busdetails_kl=pd.read_csv("kl_bus_details.csv")
df_busdetails_pj=pd.read_csv("pj_bus_details.csv")
df_busdetails_kd=pd.read_csv("kd_bus_details.csv")
df_busdetails_ap=pd.read_csv("ap_bus_details.csv")

df_allbus=pd.concat([df_busdetails_up,df_busdetails_nb,df_busdetails_hr,df_busdetails_ch,df_busdetails_rj,df_busdetails_tl,df_busdetails_sb,df_busdetails_kl,df_busdetails_pj,df_busdetails_kd,df_busdetails_ap],ignore_index=True)


df_allbus

import os

# Define the path to save the CSV file
file_path = r"C:\Users\rakes\OneDrive\Desktop\Kavitha\personal\practice\allbus_bus_details.csv"


# Ensure the directory exists
directory = os.path.dirname(file_path)
if not os.path.exists(directory):
    print(f"Directory does not exist: {directory}")
    os.makedirs(directory)  # Create the directory if it doesn't exist

# Convert DataFrame to CSV
try:
    df_allbus.to_csv(file_path, index=False)
    print(f"Data successfully written to {file_path}")
except PermissionError:
    print(f"PermissionError: Unable to write to the file {file_path}. Check file permissions.")
except Exception as e:
    print(f"An error occurred while writing the file: {e}")




































