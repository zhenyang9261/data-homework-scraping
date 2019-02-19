# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver

# Function to scrape different websites for Mars facts.
def scrape():
    #---------- NASA Mars News -------------------#

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # get news title and paragraph
    news_title = soup.find('div', class_="content_title").a.text.strip()
    news_paragraph = soup.find('div', class_="rollover_description_inner").text.strip()
    latest_news =[news_title, news_paragraph]

    #---------- JPL Mars Space Images -------------------#

    # Splinter definitions
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Retrieve page
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Find and compose the url
    featured_image_url = soup.find('footer').a['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    #---------- Mars Weather -------------------#

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    # Retrieve page
    browser.visit(url)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    tweets = soup.find_all('div', class_="tweet")

    # Loop through tweets search for result
    for tweet in tweets:

        # Find the title of the tweet
        title = tweet.find('span', class_='FullNameGroup')
    
        if ("Mars Weather" in title.text.strip()):
            
            mars_weather = tweet.find('div', class_='js-tweet-text-container').p.text.strip()
            break

    #---------- Mars Facts -------------------#

    # URL of page to be scraped
    url = 'https://space-facts.com/mars/'

    # Read tables into pandas
    facts_tables = pd.read_html(url)

    # Compose the dataframe
    facts_df = facts_tables[0]
    facts_df.columns = ['Description', 'Value']

    # Set index
    facts_df.set_index('Description', inplace=True)

    # General HTML table 
    html_table = facts_df.to_html()

    #-------------- Compose the result dictionary -----------------------------#
    mars = {'news': latest_news,
            'img_url': featured_image_url,
            'weather': mars_weather,
            'facts': html_table}
    
    return mars