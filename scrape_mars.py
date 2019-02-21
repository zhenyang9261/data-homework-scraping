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

    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    first_news = soup.find('div', class_="list_text")

    news_title = first_news.a.text.strip()
    news_paragraph = first_news.find('div', class_="article_teaser_body").text.strip()
    
    latest_news =[news_title, news_paragraph]

    #---------- JPL Mars Space Images -------------------#

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

    #---------- Mars Hemispheres -------------------#
    # URL of page to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	
	# Picture - Cerberus Hemisphere Enhanced -------------

    # Retrieve page
    browser.visit(url)
    html = browser.html

    # Wait a couple seconds in case result is not coming back fast enough

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # Click on the link and go to the next page to get the image link
    browser.click_link_by_partial_text('Cerberus Hemisphere Enhanced')


    html_cerberus=browser.html
    soup = BeautifulSoup(html_cerberus, 'html.parser')
    download_cerbrus = soup.find('div', class_='downloads')

    link_cerberus = download_cerbrus.find('a')['href']

	# Picture - Schiaparelli Hemisphere Enhanced -------------

	# Retrieve page
    browser.visit(url)
    html = browser.html

	# Wait a couple seconds in case result is not coming back fast enough

	# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

	# Click on the link and go to the next page to get the image link
    browser.click_link_by_partial_text('Schiaparelli Hemisphere Enhanced')


    html_schiaparelli=browser.html
    soup = BeautifulSoup(html_schiaparelli, 'html.parser')
    download_schiaparelli = soup.find('div', class_='downloads')

    link_schiaparelli = download_schiaparelli.find('a')['href']

	# Picture - Syrtis Major Hemisphere Enhanced -------------

	# Retrieve page
    browser.visit(url)
    html = browser.html

	# Wait a couple seconds in case result is not coming back fast enough

	# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

	# Click on the link and go to the next page to get the image link
    browser.click_link_by_partial_text('Syrtis Major Hemisphere Enhanced')

    html_syrtis=browser.html
    soup = BeautifulSoup(html_syrtis, 'html.parser')
    download_syrtis = soup.find('div', class_='downloads')

    link_syrtis = download_syrtis.find('a')['href']
	
	# Picture - Valles Marineris Hemisphere Enhanced -------------

	# Retrieve page
    browser.visit(url)
    html = browser.html

	# Wait a couple seconds in case result is not coming back fast enough

	# Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
  
	# Click on the link and go to the next page to get the image link
    browser.click_link_by_partial_text('Valles Marineris Hemisphere Enhanced')


    html_valles=browser.html
    soup = BeautifulSoup(html_valles, 'html.parser')
    download_valles = soup.find('div', class_='downloads')

    link_valles = download_valles.find('a')['href']

    hemisphere_img = [link_cerberus, link_schiaparelli, link_syrtis, link_valles]

    #-------------- Compose the result dictionary -----------------------------#
    mars = {'news': latest_news,
            'img_url': featured_image_url,
            'weather': mars_weather,
            'facts': html_table,
			'hemisphere': hemisphere_img}
    
    return mars