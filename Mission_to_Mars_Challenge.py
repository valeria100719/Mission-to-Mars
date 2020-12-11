#!/usr/bin/env python
# coding: utf-8

# In[31]:


# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


# In[32]:


# Path to chromedriver
get_ipython().system('which chromedriver')


# In[33]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[10]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[11]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[12]:


slide_elem.find("div", class_='content_title')


# In[13]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[14]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
news_p


# ### JPL Space Images Featured Image

# In[15]:


# Visit URL
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[16]:


# Find and click the full image button
full_image_elem = browser.find_by_id('full_image')
full_image_elem.click()


# In[17]:


# Find the more info button and click that
browser.is_element_present_by_text('more info', wait_time=1)
more_info_elem = browser.links.find_by_partial_text('more info')
more_info_elem.click()


# In[18]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[19]:


# find the relative image url
img_url_rel = img_soup.select_one('figure.lede a img').get("src")
img_url_rel


# In[20]:


# Use the base url to create an absolute url
img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
img_url


# ### Mars Facts

# In[21]:


df = pd.read_html('http://space-facts.com/mars/')[0]

df.head()


# In[22]:


df.columns=['Description', 'Mars']
df.set_index('Description', inplace=True)
df


# In[23]:


df.to_html()


# ### Mars Weather

# In[24]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[25]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[26]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[27]:


import time
# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[28]:


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


# In[29]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[30]:


# 5. Quit the browser
browser.quit()


# In[ ]:




