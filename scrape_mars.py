from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "C:/Users/User/Downloads/driver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    scraped_data = {}
    title_para = marsNews()
    scraped_data['mars_title'] = title_para[1].text
    scraped_data['mars_paragraph'] = title_para[0].text
    scraped_data['mars_featured_image'] = marsImage()
    scraped_data['mars_facts'] = marsFacts()
    scraped_data['mars_hemisphere'] = marsHemisphere()

    return scraped_data
    
def marsNews():  
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_title = soup.find_all('div',class_='content_title')
    paragraph_text = soup.find_all('div',class_='article_teaser_body')
    title_para = [news_title,paragraph_text]
    return title_para
    
def marsImage():   
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')
    image_link = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + image_link
    return featured_image_url
    

def marsFacts():    
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    mars_facts = pd.read_html(url)
    mars_facts = mars_facts[0]
    return mars_facts

def marsHemisphere():
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url)
    html = browser.html
    soup = bs(html,"html.parser")
    title_img_url = []
    items = soup.find_all('div',class_='item')

    for item in items:
        link = item.find('a')['href']
        title = item.find('h3').text
        title_img_url.append({"Title":title,"Img_url":base_url+link})

    return title_img_url