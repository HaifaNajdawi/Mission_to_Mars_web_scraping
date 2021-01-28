#!/usr/bin/env python
# coding: utf-8

# In[618]:


# Dependencies 
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[619]:


# Retrive page with the requests module
executable_path = {'executable_path': "C:\Windows\chromedriver"}
browser = Browser('chrome', **executable_path, headless=False)


# In[620]:


# URL for the page to be scraped
url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"


# In[621]:


# Create BeautifulSoup object parse with lxml
browser.visit(url)


# In[622]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())


# In[623]:


data_holder={}
#Find main class of text and parg
item_list=soup.find_all("ul",class_="item_list")
for item in item_list:
    slide=item.find_all("li",class_="slide")[0]
    data_holder["news_p"] = slide.find('div', class_='rollover_description_inner').text.strip()  
    data_holder["news_title"]=slide.h3.text
    print(data_holder["news_p"])
    print(data_holder["news_title"])


# In[624]:


executable_path={"executable_path":"C:\Windows\chromedriver"}
browser=Browser("chrome",**executable_path,headless=False)


# In[625]:


url="https://www.jpl.nasa.gov/images/new-all-in-one-antenna-for-the-deep-space-network/"
browser.visit(url)


# In[626]:


# html object
html=browser.html


# In[627]:


#Parse HTML with Beautiful Soup
soup=BeautifulSoup(html,"html.parser")
print(soup.prettify())


# In[628]:


# Find class contain the picture
img_page = soup.find_all('div', class_='relative bg-black border border-black')
print(len(img_page))

#loop in the div and take src and hold it in the dic.
for pic in img_page:
    data_holder["feature_image_url"] = pic.img["src"]
    print(data_holder["feature_image_url"])


# In[629]:


# web page st scrape table from it
url="https://space-facts.com/mars/"


# In[630]:


tables = pd.read_html(url)
tables


# In[631]:


# get first table from the list
print(len(tables))
mars_fact_df=tables[0]
mars_fact_df.head()


# In[632]:


#rename the columns
mars_fact_df.columns=["Mars","Description"]
mars_fact_df


# In[633]:


#Remove colon from the table
mars_fact_df["Mars"] = mars_fact_df["Mars"].replace({':':''}, regex=True)
mars_fact_df


# In[634]:


mars_fact_df = mars_fact_df.set_index("Description")
mars_fact_df.head()


# In[635]:


#convert table to HTML code
html_table = mars_fact_df.to_html()
html_table


# In[636]:


#replace new line with white space
html_table.replace('\n', '')


# In[637]:


#put html in seprate file 
mars_fact_df.to_html('mars_html.html')


# In[638]:


get_ipython().system('open mars_html.html')


# In[648]:


# Retrive page with the requests module
executable_path = {'executable_path': "C:\Windows\chromedriver"}
browser = Browser('chrome', **executable_path, headless=False)


# In[649]:


url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url)


# In[650]:


html=browser.html
soup=BeautifulSoup(html,"html.parser")
print(soup.prettify())


# ## To Run this code make sure you are in the first page
# 

# In[728]:


hemisphere_image_urls=[]
links = browser.find_by_css("a.itemLink.product-item h3")
print(len(links))
for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.itemLink.product-item h3")[item].click()
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    
    # Get Hemisphere Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Append Hemisphere Object to List
    hemisphere_image_urls.append(hemisphere)
    
    # Return back after first click because it will be in the second page
    browser.back()
hemisphere_image_urls


# In[ ]:




