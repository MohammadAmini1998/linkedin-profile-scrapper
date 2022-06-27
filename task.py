from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys# direct the webdriver to where the browser file is:
from selenium.common.exceptions import NoSuchElementException        
from bs4 import BeautifulSoup
import logging

from database import addRecord,csv_convertor
def log(msg):
    # Create and configure logger
    logging.basicConfig(filename="Dataa.log",
                        format='%(asctime)s %(message)s',
                        filemode='w')
    
    # Creating an object
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
   
    logger.info(msg)



def scroll_to_bottom():
    start = time.time()
    # will be used in the while loop
    initialScroll = 0
    finalScroll = 1000
    while True:
        try:
            driver.find_element(By.ID,"ember802").click()
        except NoSuchElementException:
            print("Please wait...")
        driver.execute_script(f"window.scrollTo({initialScroll},{finalScroll})")
        initialScroll = finalScroll
        finalScroll += 1000
        time.sleep(3)
        end = time.time()
        # We will scroll for 20 seconds.
        if round(end - start) > 60:
            break

def extract_info(link):
    driver.get(link)
    driver.implicitly_wait(2)
    src = driver.page_source
    soup = BeautifulSoup(src, 'lxml')

    # one of the ways to get link of current page (profile link)


    # personal details    
    name_div = soup.find('div', {'class': 'mt2 relative'})
    # name
    try:
        name = name_div.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).get_text().strip()
       
    except IndexError: # To ignore any kind of error
        name = 'NULL'
    except AttributeError:
        name = 'NULL'
        
    # location
    try:
        location = name_div.find('span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
    except IndexError:
        location = 'NULL'
    except AttributeError:
        location = 'NULL'

    # degree_level
    try:
        degree_level = name_div.find('span', {'class': 'dist-value'}).get_text().strip()
    except IndexError:
        degree_level = 'NULL'
    except AttributeError:
        degree_level = 'NULL'
        
    # No. of connections   
    connections= soup.find('ul', {'class': 'pv-top-card--list pv-top-card--list-bullet display-flex pb1'})         
    try:
        connections = connections.find('span', {'class': 't-bold'}).get_text().strip()
        
    except IndexError:
        connections = 'NULL'
    except AttributeError:
        connections = 'NULL'

    
    # recent positions
    try:
        # job_title=Experience_div.find('div',)
        job_title = name_div.find('div', {'class':'text-body-medium break-words'}).get_text().strip()
    except IndexError:
        job_title = 'NULL'
    except AttributeError:
        job_title = 'NULL'
        
    output = ({'Name': name, 'Location': location, 'Degree Level': degree_level,
                   'No. of Connections': connections, 'Postion': job_title,
                    'Linked Link': link}) 
    
        
    # saving outputs

    addRecord(name,location,degree_level,connections,job_title,link)
    log(output)

driver_path = "C:\Webdriver\chromedriver.exe"

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options,executable_path=driver_path)

# your secret credentials:

driver.get('https://www.linkedin.com/login')
time.sleep(3)



username = driver.find_element(By.ID, "username")
# In case of an error, try changing the element
# tag used here.
  
# Enter Your Email Address
user=input("Enter your email address ")
username.send_keys(user)  
  
# entering password
pword = driver.find_element(By.ID, "password")
# In case of an error, try changing the element 
# tag used here.
  
# Enter Your Password
password=input("Enter your password ")
pword.send_keys(password)        
  
# Clicking on the log in button
# Format (syntax) of writing XPath --> 
# //tagname[@attribute='value']
driver.find_element(By.XPATH,"//button[@type='submit']").click()
time.sleep(3)

links = []

my_links=driver.find_elements(By.TAG_NAME,'a')
for link in my_links:
    Link=link.get_attribute('href')
    if "https://www.linkedin.com/in/" in Link:
        links.append(Link)
        break



driver.get('https://www.linkedin.com/mynetwork/invite-connect/connections/')
time.sleep(3)
print("Scrolling page to bottom...")
scroll_to_bottom()


lists = driver.find_elements(By.CLASS_NAME,"mn-connection-card__link")

# Empty list for storing links



for lis in lists:
    links.append(lis.get_attribute('href'))

# # Loop through all the links and launch one by one
for link in links:
    extract_info(link)
csv_convertor()