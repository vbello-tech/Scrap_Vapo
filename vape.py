# import these two modules bs4 for selecting HTML tags easily
from bs4 import BeautifulSoup
# requests module is easy to operate some people use urllib but I prefer this one because it is easy to use.
import requests
from selenium import webdriver
import pandas as pd
import time
import urllib.parse

no_of_pd = 0  # number of products
vape_list = []  # list of products
n_w = 1


# 1 = https://vapology.com.ng/?product-page=1
# 2 = https://vapology.com.ng/?product-page=2
# 3 = https://vapology.com.ng/?product-page=3
# 4 = https://vapology.com.ng/?product-page=4
# 5 = https://vapology.com.ng/?product-page=5


def get_chrome_web_driver(options):
    return webdriver.Chrome("./chromedriver", chrome_options=options)


def get_web_driver_options():
    return webdriver.ChromeOptions()


def set_ignore_certificate_error(options):
    options.add_argument('--ignore-certificate-errors')


def set_browser_as_incognito(options):
    options.add_argument('--incognito')


while n_w < 6:
    url = f"https://vapology.com.ng/?product-page={n_w}"
    source = requests.get(url)

    # Parsing the HTML
    soup = BeautifulSoup(source.content, 'html.parser', )

    #  fetch all list item with class "product
    list_contents = soup.find_all("li", class_='product')
    for i in list_contents:
        x = i.text
        # print(x.rstrip().replace("\n", ""))
        item_link = i.find('a', class_="woocommerce-LoopProduct-link", href=True)['href']
        item_name = i.find('h2', class_="woocommerce-loop-product__title").text
        item_category = i.find('span', class_="loop-product-categories").get_text()
        vape_list.append([item_name, item_link, item_category])
        no_of_pd += 1
        time.sleep(1)
    n_w += 1

print(no_of_pd)
for vape in vape_list:
    print(vape, "\n")

df = pd.DataFrame(vape_list, columns=['item_link', 'item_name', 'item_category'])
print(df)

#  convert to csv
df.to_csv('vape_items.csv', index=False)

#  convert ro excel format
df.to_excel('vape product.xlsx', index=False,)


"""
# Extract the relevant information from the HTML code

for row in soup.select('tbody.lister-list tr'):
title = row.find('td', class_='titleColumn').find('a').get_text()
year = row.find('td', class_='titleColumn').find('span', class_='secondaryInfo').get_text()[1:-1]
rating = row.find('td', class_='ratingColumn imdbRating').find('strong').get_text()
movies.append([title, year, rating])

# Store the information in a pandas dataframe
df = pd.DataFrame(movies, columns=['Title', 'Year', 'Rating'])

# Add a delay between requests to avoid overwhelming the website with requests
time.sleep(1)

Now, let’s export the data as a CSV file. We will use the pandas library.

# Export the data to a CSV file
df.to_csv('top-rated-movies.csv', index=False)

<span class="loop-product-categories"><a href="https://vapology.com.ng/product-category/vape-accessories/" rel="tag">Vape Accessories</a></span>
<h2 class="woocommerce-loop-product__title">Nicotine Salt ICED STRAWBERRY MANGO 30ML</h2>
<a href="https://vapology.com.ng/product/nicotine-salt-iced-strawberry-mango-30ml/" class="woocommerce-LoopProduct-link woocommerce-loop-product__link"><h2 class="woocommerce-loop-product__title">Nicotine Salt ICED STRAWBERRY MANGO 30ML</h2><div class="product-thumbnail product-item__thumbnail"><img width="300" height="300" src="https://vapology.com.ng/wp-content/uploads/2024/04/images-88-300x300.jpeg" class="attachment-woocommerce_thumbnail size-woocommerce_thumbnail" alt="" loading="lazy"></div></a>
"""
