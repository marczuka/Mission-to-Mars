# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup
import datetime as dt
import pandas as pd
import traceback

def scrape_all():
    
    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)

    news_title, news_paragraph, news_link = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "news_link": news_link,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": mars_hemispheres(browser),
      "last_modified": dt.datetime.now()
    }

    # Close the browser driver
    browser.quit()

    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Choose the first article from the list
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first <a> tag and save it as a "news_title"
        news_title = slide_elem.find("div", class_='content_title').get_text()
        
        # Get the link for the featured article
        news_link = slide_elem.find("div", class_='content_title').find("a").get("href")
        news_link = f"https://mars.nasa.gov{news_link}"

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    
    except AttributeError:
        return None, None, None

    return news_title, news_p, news_link

# LOOKING FOR THE IMAGE

def featured_image(browser):
    
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.find_link_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = BeautifulSoup(html, 'html.parser')

    try:
        # Find the relative image url
        # img_url_rel = img_soup.select_one('figure.lede a img').get("src")

        # Finding an image different way - by the unique class name
        img_url_rel = img_soup.find('img', class_='main_image').get("src")
    
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url

# LOOKING FOR THE TABLE

def mars_facts():

    try:
        
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('http://space-facts.com/mars/')[0]
        
    except BaseException as e:
        print("MARS FACTS EXCEPTION !!!")
        print(str(e))
        traceback.print_exc()
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Value']
    #df.set_index('Description', inplace=True)
    
    # Convert dataframe into a list of dictionaries
    list_of_dict = [{'desc' : value[0], 'value': value[1]} for value in df.values]
    
    return list_of_dict

def mars_hemispheres(browser):

    # Empty list for the hemispheres data
    mars_hemispheres = [] 

    # Visit the astrogeology.usgs.gov web-site
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("div div a img", wait_time=1)

    # Scrape the web-site for the full resolution hemisphere images
    try:

        for i in range(4):
        
            # Clicking the link for each hemisphere
            hemi_url = browser.find_link_by_partial_text("Enhanced")[i]
            hemi_url.click()
    
            # Parse the page with BeautifulSoup
            html = browser.html
            hemi_soup = BeautifulSoup(html, 'html.parser')
    
            # Get hemisphere name
            hemi_name = hemi_soup.find('h2', class_="title").get_text()
        
            # Get hemisphere full resolution image link
            hemi_link = hemi_soup.find('div', class_="downloads").find("a").get("href")
    
            # Add the hemisphere data to the list
            mars_hemispheres.append({"title": hemi_name, "img_url": hemi_link})
    
            # Go back to the original page
            browser.back()

    except BaseException:
        return None

    return mars_hemispheres


if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())
