import pandas as pd
import requests
import json
import logging
from bs4 import BeautifulSoup
import time

logging.basicConfig(filename='webscraping.log',
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

logger = logging.getLogger('webscraper')
# GET COUNTRIES
#country_names = [c_name for c_name in pd.read_csv('/Users/meggan/dsi-10/portfolio/capstone/data/country_names.csv')['name']]
country_names = [c_name for c_name in pd.read_csv('./country_names.csv')['name']]
# SOURCES: http://worldpopulationreview.com/countries/most-visited-countries/
    # & https://www.travel-advisory.info/api

# GET ALL URLS
try:
    with open('temp_file_articles.json') as f:
        file_articles=json.load(f)
except:
    file_articles = []
    
    
try:
    with open('temp_file_search.json') as f:
        search_articles=json.load(f)
except:
    search_articles = []

try:
    with open('countries.json') as f:
        countries=json.load(f)
except:
    countries = []
    
file_pages = {}
search_pages = {}

print("STARTING")
for country in country_names[len(countries):]:
    countries.append(country)
    logger.info(f'Searching {country}...')

    # FIND THE MAXIMUM PAGES OF BLOG POSTS BY COUNTRY
    url_file = f'https://fathomaway.com/{country}'
    url_search = f'https://fathomaway.com/search/?q={country}'
    res_file = requests.get(url_file)
    res_search = requests.get(url_search)
    soup_file = BeautifulSoup(res_file.content, 'lxml')
    soup_search = BeautifulSoup(res_search.content, 'lxml')
    time.sleep(10)
    try:
        file_pages[country] =  soup_file.find_all(attrs={'class': 'pagination__link'})[-2].text
    except:
        file_pages[country] =  1
    try:
        search_pages[country] =  soup_search.find_all(attrs={'class': 'pagination__link'})[-2].text
    except:
        search_pages[country] =  1
    
    # GET URLS FOR EACH COUNTRY FILE
    logger.info(f'... {file_pages[country]} pages of filed articles ...')
    
    for num in range(int(file_pages[country])): 
        url_base = f'https://fathomaway.com/{country}/?page={num}'
        res_ = requests.get(url_base)
        soup_ = BeautifulSoup(res_.content, 'lxml')
        time.sleep(10)

        for link in soup_.find_all(attrs={'class': 'content__url'}):
            article = {}
            article['href'] = link.attrs['href']
            article['title'] = link.text.strip()
            article['country'] = country
            file_articles.append(article)
            

    # GET URLS FOR COUNTRY BY SEARCH
    logger.info(f'... and {search_pages[country]} pages of searched articles ...')
    
    for num in range(int(search_pages[country])): 
        url_base = f'https://fathomaway.com/search/?q={country}&page={num}'
        res_ = requests.get(url_base)
        soup_ = BeautifulSoup(res_.content, 'lxml')
        time.sleep(10)

        for link in soup_.find_all(attrs={'class': 'content__url'}):
            article = {}
            article['href'] = link.attrs['href']
            article['title'] = link.text.strip()
            article['country'] = country
            search_articles.append(article)
    logger.info("SAVING FILES FOR " + country)
    with open('countries.json', 'w') as outfile:
        json.dump(countries, outfile)
    with open('temp_file_articles.json', 'w') as outfile:
        json.dump(file_articles, outfile)
    with open('temp_file_search.json', 'w') as outfile:
        json.dump(search_articles, outfile)        


df_file = pd.DataFrame(file_articles)
df_file = df_file.sort_values(by='title', ascending=False).drop_duplicates('href').copy()

df_search = pd.DataFrame(search_articles)
df_search = df_search.sort_values(by='title', ascending=False).drop_duplicates('href').copy()

# PARSE CONTENT OF EVERY BLOG POST - FILED
logger.info(f'Pulling text from filed articles ...')
try:
    with open('content_filed.json') as f:
        content_filed=json.load(f)
except:
    content_filed = []
    
try:
    with open('href_cached.json') as f:
        hrefs=json.load(f)
except:
    hrefs = []

print("PULLING TEXT")
for url in df_file['href'][len(hrefs):]:
    hrefs.append(url)
    url_post = f'https://fathomaway.com{url}'
    res_post = requests.get(url_post)
    soup_post = BeautifulSoup(res_post.content, 'lxml')

    paragraphs = soup_post.find_all(attrs={'class': 'article-detail__main'})

    text = ''.join([paragraph.text.replace('\n', '') for paragraph in paragraphs])
    content_filed.append(text)
    with open('href_cached.json', 'w') as outfile:
        json.dump(hrefs, outfile) 
    with open('content_filed.json', 'w') as outfile:
        json.dump(content_filed, outfile) 
    time.sleep(10)

# PARSE CONTENT OF EVERY BLOG POST - SEARCHED
print("PARSING CONTENT")
logger.info(f'Pulling text from searched articles ...')
try:
    with open('content_searched.json') as f:
        content_searched=json.load(f)
except:
    content_searched = []
    
try:
    with open('href_cached_content_search.json') as f:
        hrefs=json.load(f)
except:
    hrefs = []

for url in df_search['href'][len(hrefs):]:
    hrefs.append(url)
    url_post = f'https://fathomaway.com{url}'
    res_post = requests.get(url_post)
    soup_post = BeautifulSoup(res_post.content, 'lxml')

    paragraphs = soup_post.find_all(attrs={'class': 'article-detail__main'})

    text = ''.join([paragraph.text.replace('\n', '') for paragraph in paragraphs])
    content_searched.append(text)
    with open('href_cached_content_search.json', 'w') as outfile:
        json.dump(hrefs, outfile) 
    with open('content_searched.json', 'w') as outfile:
        json.dump(content_searched, outfile) 
    time.sleep(10)

df_file['text'] = content_filed
df_search['text'] = content_searched

df_search.to_csv('search_all_articles.csv')
df_file.to_csv('files_all_articles.csv')
