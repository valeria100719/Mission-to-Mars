# Import Splinter and BeautifulSoup
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
import time

# Path to chromedriver
#!which chromedriver

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path)

def scrape_all():
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemispheres = mars_hemispheres(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": hemispheres
    }
    #print(data["hemisphere_info"])
    # Stop webdriver and return data
    
    browser.quit()
    return data

def mars_news(browser):
    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


# # ## JPL Space Images Featured Image

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        print(img_url_rel)

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Mars Planet Profile', 'Description']

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(index=False)

def mars_hemispheres(browser):
    # ### Hemispheres
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    # Define a list of Hemispheres
    Mars_Hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    i = 0
    for hemispheres in Mars_Hemispheres:
        #print(f"Hemisphere is: {hemispheres}")
        browser.links.find_by_partial_text(hemispheres).first.click()
        time.sleep(1)
        html = browser.html
        
        # Parse the resulting html with soup
        html_soup = soup(html, 'html.parser')

        # Find relevant image element
        img_elem = html_soup.find("div", class_='downloads')

        #Find image URL
        img_url = img_elem.find('a', href=True)
        
        #Append the list with URL
        hemisphere_image_urls.append({"img_url":img_url['href']})
        #hemisphere_image_urls
        title_elem = html_soup.find("div", class_='content')
        
        title_txt = title_elem.find('h2', class_='title').get_text()
        
        #Update the list with title
        hemisphere_image_urls[i].update({"title":title_txt})
        
        i+=1
        browser.back()

    return hemisphere_image_urls

if __name__ == "__main__":
    scrape_all()