# Mission-to-Mars
This repository contains the app that scrapes the internet for Mars data, stores obtained data in the Mongo DB and shows the data on the app home web-page using Flask and Bootstrap.

<table>
  <tr>
    <td><img src = "/apps/templates/web-app-1.png">
    <td><img src = "/apps/templates/web-app-2.png">
  </tr>
</table>

The data for the app is gathered using Splinter and BeautifulSoup Python libraries (<i>scraping.py</i> project file). 
The following data is obtained:
- News title and article from https://mars.nasa.gov/news/ ;
- Featured image from https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars ;
- Table of facts about Mars from http://space-facts.com/mars/ ;
- Full-resolution pictures of four Mars hemispheres fromhttps://astrogeology.usgs.gov/ .

After obtaining data is stored at the MongoDB database and retrieved on the web-app home page using Flask tools (<i>app.py</i> file).
Homepage for the app is designed using Bootstrap.

# Challenge
2020-03-23 The scraping part of the challenge obtaining hemispheres data from https://astrogeology.usgs.gov/ is added to the <i>scraping.py</i> project file.

2020-03-22 The https://astrogeology.usgs.gov/ site was down on Sunday, March 22, so the images of the Mars hemispheres are temporarily replaced by fake images. Web-scraping part of the Challenge will be added as soon as the source web-site is up. 
