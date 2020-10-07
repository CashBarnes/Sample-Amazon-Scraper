# Simple Sample Amazon Scraper by Cash Barnes
# requirements:
# Selenium (make sure you are using the correct version for your browser)
# Chrome
# BeautifulSoup
# sample_input.csv with list of search terms. Each search term should be the only thing on the row.

from selenium import webdriver  # make sure you are using the correct webdriver for the version of Chrome you are using
import time # import time so that we can use time.sleep() as needed when loading new pages
import csv  # import csv so that we can read and write from and to csv files
from selenium.webdriver.common.keys import Keys # import keys so that we can send key strokes to the pages our scraper is visiting
from bs4 import BeautifulSoup   

sample_input = 'sample_input.csv'   #change this to the name of the input csv you want to have your scraper use
sample_output = 'sample_output.csv'
search_url = 'http://amazon.com'    #change this to the url that you want to have your scraper visit

# Here we will open our sample output file and clear it with 'w'.
with open(sample_output, 'w', newline='') as csvfile:
        namewriter = csv.writer(csvfile)
        namewriter.writerow(['Search Term','Top Item','Rating','URL'])   # this will print the first line of our output file, which will be a header. 
        
# Open our input file and begin scraping Amazon
with open(sample_input, newline='') as csvfile:
    search_term_reader = csv.reader(csvfile, delimiter=",")
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('http://amazon.com')
        
    for row in search_term_reader:
        search_term = row[0]    # this will assign the first column in the input file to the search term variable (there should only be on column)
        # for this example, we will be using driver.find_element to find the search box. You could also just use the search url paired with the search terms.
        search_box = driver.find_element_by_id('twotabsearchtextbox').clear()   # find and clear the search box on the site you want to scrape. 
        search_box = driver.find_element_by_id('twotabsearchtextbox')           # after clearing the search box, this is re-assigning it to the search_box variable
        
        search_box.send_keys(search_term)  # this will use send_keys to type the search_term into the search box
        search_box.send_keys(Keys.RETURN)  # this will hit the enter key after sending the search_term to the search box
        time.sleep(.5)                     # this is to allow a brief pause for the page to load after hitting enter
        
        soup = BeautifulSoup(driver.page_source, 'html.parser') # we will use BeautifulSoup to parse page as html
        results = soup.find_all('div', {'data-component-type': 's-search-result'})  # we can use the inspect tool in chrome to find unique identifiers for the elements we want to return                
        item = results[0]   
        atag = item.h2.a
        description = atag.text.strip()
        url = 'https://www.amazon.com' + atag.get('href')

        #price_parent = item.find('span', 'a-price')                this will return the parent span to the class that has price
        #price = price_parent.find('span', 'a-offscreen').text      this will return the price span within the parent span. These lines are commented out since all items don't have a price
        rating = item.i.text
        #review_count = item.find('span',{'class': 'a-size-base', 'dir': 'auto'}).text  # Not consistently pointing to review count so commented out.   

        with open(sample_output, 'a', newline='') as csvfile:
            namewriter = csv.writer(csvfile)
            namewriter.writerow([search_term, description, rating, url])             

driver.quit()


