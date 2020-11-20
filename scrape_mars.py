from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser


def marsNews():
    browser = init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    news_title = soup.find_all('div', class_='content_title')
    paragraph_text = soup.find_all('div', class_='article_teaser_body')
    latest_news_title = news_title[1].text
    latest_paragraph_text = paragraph_text[0].text
    return latest_news_title, latest_paragraph_text


def marsImage():
    browser = init_browser()
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    image_link = soup.find('article')['style'].replace(
        'background-image: url(', '').replace(');', '')[1:-1]
    featured_image_url = 'https://www.jpl.nasa.gov' + image_link
    return featured_image_url


def marsFacts():
    browser = init_browser()
    url = 'https://space-facts.com/mars/'
    browser.visit(url)
    time.sleep(10)
    mars_facts = pd.read_html(url)
    mars_facts = mars_facts[0].to_html()
    return mars_facts


def marsHemisphere():
    browser = init_browser()
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    browser.visit(url)
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')
    title_img_url = []
    
    items = soup.find_all('div',class_='item')

    for item in items:
        title = item.find('h3').text
        link = item.find('a', class_='itemLink product-item')['href']
        browser.visit(base_url+link)
        html = browser.html
        soup = BeautifulSoup(html,"html.parser")
        img_link = base_url + soup.find('img',class_='wide-image')['src']
        title_img_url.append({"Title":title,"Img_url":img_link})

    return title_img_url

def scrape_info():
    scraped_data = {}
    scraped_data['mars_title'], scraped_data['mars_paragraph'] = marsNews()
    scraped_data['mars_featured_image'] = marsImage()
    scraped_data['mars_facts'] = marsFacts()
    scraped_data['mars_hemisphere'] = marsHemisphere()

    return scraped_data
