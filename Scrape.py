"""
This .py file takes a link runs it through Youtubetranscript.com, and extracts all
the individual quote time stamps, stores them as individual .mp3 file and it's associated text
"""

#imports
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


# step 1: paste link into website

# Specify the path to the webdriver executable
driver_path = 'chromedriver'

# Create an instance of the webdriver
driver = webdriver.Chrome(driver_path)

# Navigate to youtube transcript
driver.get('https://youtubetranscript.com/')

# Find the search bar element by its ID
search_bar = driver.find_element(by='id', value='video_url')

# search url
search_bar.send_keys('https://www.youtube.com/watch?v=MkKxAi_c0LQ')
search_bar.send_keys(Keys.ENTER)

# wait 3 seconds
time.sleep(2) 

# step 2: grab the time stamps and text
demo_div = driver.find_element(By.ID, 'demo') # locate div with the element id

# Get every single element
elements = demo_div.find_elements(By.CSS_SELECTOR, '*')

# Initialize variables
current_string = ''
quotes = []

quote_data = {}

br_count = 0
beg = True

# loop through the elements
for element in elements:

    if element.tag_name == 'a':
        br_count = 0
        current_string += element.text + ' '
        if beg == True:
            quote_data['start_time'] = element.get_attribute('data-start')

        ending = element.get_attribute('data-end')

    elif element.tag_name == 'br':
        br_count+=1
        beg = False

        if br_count == 2:
            quote_data['quote'] = current_string.strip()
            quote_data['end_time'] = ending
            quotes.append(quote_data)
            quote_data = {}
            current_string = ''
            br_count = 0
            beg = True

    else:
        br_count = 0
            
# Add the last string to the list if not already added
if current_string.strip() != '':
    quote_data['quote'] = current_string.strip()
    quote_data['end_time'] = element.get_attribute('data-end')
    quotes.append(quote_data)

# Close the browser window
driver.quit()

# Print the list of strings
# count = 0
# for quote in quotes:
#     print(f"TimeStamp: [{start_time[count]}, {end_time[count]}] {quote}")
#     print("---------")
#     count += 1

# Write the dictionary to a JSON file
with open('quotes.json', 'w') as f:
    json.dump(quotes, f, indent=2)
