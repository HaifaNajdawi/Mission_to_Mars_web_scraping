# Dependencies 
from bs4 import BeautifulSoup
import requests
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd





# Retrive page with the requests module
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():

    browser=init_browser()
    data_holder={}

    url1="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    # Create BeautifulSoup object parse with html
    browser.visit(url1)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Find main class of text and parg
    item_list=soup.find_all("ul",class_="item_list")
    for item in item_list:
        slide=item.find_all("li",class_="slide")[0]
        data_holder["news_p"] = slide.find('div', class_='rollover_description_inner').text.strip()  
        data_holder["news_title"]=slide.h3.text
    # Close the browser after scraping
    url2="https://www.jpl.nasa.gov/images/new-all-in-one-antenna-for-the-deep-space-network/"
    browser.visit(url2)
    # html object
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    img_page = soup.find_all('div', class_='relative bg-black border border-black')
    for pic in img_page:
        data_holder["feature_image_url"] = pic.img["src"]

    url3="https://space-facts.com/mars/"

    tables = pd.read_html(url3)
    # get first table from the list
    print(len(tables))
    mars_fact_df=tables[0]
    #rename the columns
    mars_fact_df.columns=["Mars","Description"]
    #Remove colon from the table
    mars_fact_df["Mars"] = mars_fact_df["Mars"].replace({':':''}, regex=True)
    
    mars_fact_df = mars_fact_df.set_index("Description")
    
    #convert table to HTML code
    data_holder["mars_table"]= mars_fact_df.to_html()  
    #replace new line with white space
    html_table=data_holder["mars_table"].replace('\n', '')
    print(html_table)
    url4="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url4)
    html=browser.html
    soup=BeautifulSoup(html,"html.parser")
    
    data_holder["hemisphere_image_urls"]=[]
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
        data_holder["hemisphere_image_urls"].append(hemisphere)
        
        # Return back after first click because it will be in the second page
        browser.back()
    return data_holder
scrape()







