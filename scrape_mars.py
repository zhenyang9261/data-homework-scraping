# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from selenium import webdriver

# Function to scrape different websites for Mars facts.
def scrape():

    # Splinter definitions
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    
    #---------- NASA Mars News -------------------#

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page. Create BeautifulSoup object; parse with 'html.parser'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find and compose result
    first_news = soup.find('div', class_="list_text")

    news_title = first_news.a.text.strip()
    news_paragraph = first_news.find('div', class_="article_teaser_body").text.strip()
    latest_news =[news_title, news_paragraph]

    #---------- JPL Mars Space Images -------------------#

    # URL of page to be scraped
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Retrieve page. Create BeautifulSoup object; parse with 'html.parser'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find and compose the url
    featured_image_url = soup.find('footer').a['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image_url

    #---------- Mars Weather -------------------#

    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    
    # Retrieve page. Create BeautifulSoup object; parse with 'html.parser'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find the tweets
    tweets = soup.find_all('div', class_="tweet")

    # Loop through tweets search for result
    for tweet in tweets:

        # Find the title and content of the tweet
        title = tweet.find('span', class_='FullNameGroup')
        mars_weather = tweet.find('div', class_='js-tweet-text-container').p.text.strip()
    
        if ("InSight" in mars_weather):
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
    
    #---------- Mars Hemispheres -------------------#
    
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Links to be clicked
    hemi_text = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced',\
            'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
    
    # Result list
    hemisphere_img = []

    for x in range(4):

        # Retrieve page. Create BeautifulSoup object; parse with 'html.parser'
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # Click on the link and go to the next page to get the image link
        browser.click_link_by_partial_text(hemi_text[x])

        # # Retrieve page. Create BeautifulSoup object; parse with 'html.parser'
        html=browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        # Find the image link
        download = soup.find('div', class_='downloads')
        link = download.find('a')['href']

        # Compose result list
        hemisphere_img.append(link)

    #-------------- Compose the result dictionary -----------------------------#
    mars = {'news': latest_news,
            'img_url': featured_image_url,
            'weather': mars_weather,
            'facts': html_table,
            'caption': hemi_text,
	    'hemisphere': hemisphere_img}

    return mars