from selenium import webdriver # Opens Amazon in a real browser (needed because Amazon is JS-heavy)
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By # Helps locate elements (CLASS_NAME, XPATH, etc.)
import time
import pandas as pd # To create a DataFrame & export CSV
from bs4 import BeautifulSoup # Parse saved HTML files
import os # Work with folders & file paths
import html # Fix HTML entities like &amp;



# driver = webdriver.Chrome()
# driver.get("https://www.bbc.com/news/world")
# assert "Latest" in driver.title
# elems = driver.find_elements(By.CSS_SELECTOR, "h2.sc-fa814188-3")
# print(f"Found.: {len(elems)} headlines.")
# for elem in elems:
#     print(elem.text)
# # elem.clear()
# # elem.send_keys("pycon")
# # elem.send_keys(Keys.RETURN)
# # assert "No results found." not in driver.page_source
# time.sleep(4)
# driver.close()


# Extract data from Amazon.ae website using Selenium WebDriver

driver = webdriver.Chrome()
category = "laptop"
i = 1

# store the html content in file.
for i in range(1, 20):
    driver.get(f"https://www.amazon.ae/s?k={category}&page={i}&qid=1765240318&xpid=jODZqVriKHKvH&ref=sr_pg_{i}")

    elems = driver.find_elements(By.CLASS_NAME, "puis-card-container")
    print(f"Found {len(elems)} products on page {i}.")
    for elem in elems:
        d = elem.get_attribute('outerHTML')
        with open(f"major_project/amazon_pages/page_{i}.html", "a", encoding='utf-8') as f:
            f.write(d)

driver.close()

# Use beautifulsoup to parse the saved HTML files and extract product details
with open("major_project/amazon_pages/page_1.html", "r", encoding='utf-8') as f:
    html_content = f.read()
soup = BeautifulSoup(html_content, 'html.parser')
pretty_html =soup.prettify() 

# Save prettified HTML
with open("major_project/amazon_pages/page_1_pretty.html", "w", encoding="utf-8") as f:
    f.write(pretty_html)


length = len(os.listdir("/Users/mohammedarafat/major_project/amazon_pages"))
print(length)

d = {'Title': [], 'Price': [], 'Offer': [], 'Link': [], 'Page_No': []}

base_link = "https://www.amazon.ae"
folder = "/Users/mohammedarafat/major_project/amazon_pages"
for file in os.listdir(folder):
    if file.endswith(".html"):
        full_path = os.path.join(folder, file)
        print(f"{full_path} \n")
        with open(full_path) as f:
            html_file = f.read()
        soup = BeautifulSoup(html_file, 'html.parser')
        
        products = soup.select("div.a-section.a-spacing-small.puis-padding-left-small.puis-padding-right-small")
        for product in products:

            # Extract Page Number
            

            # Extract Title
            title_tag = product.select_one("h2 span")
            raw_title = title_tag.get_text()
            clean_title = " ".join(raw_title.split()) if title_tag else None

            
            # Extract Price
            price_tag = product.select_one("span.a-price > span.a-offscreen")
            price = price_tag.get_text() if price_tag else None

            # Extract Offer
            offer_tag = product.select_one("div.a-row.a-size-base.a-color-secondary span")
            offer = offer_tag.get_text(strip=True) if offer_tag else None

            # Extract Link
            link_tag = product.select_one("a.a-link-normal.s-line-clamp-4.s-link-style.a-text-normal")
            # Fix 1: Convert HTML entities (&amp; → &)
            clean_link = html.unescape(link_tag['href'])
            full_url = base_link + clean_link if link_tag else None

            # Append Now
            d['Page_No'].append(file)
            d['Title'].append(clean_title)
            d['Price'].append(price)
            d['Offer'].append(offer)
            d['Link'].append(full_url)
            
        
for key, value in d.items():
    print(f"{key, len(value)}")
df = pd.DataFrame(data = d)
df.to_csv("/Users/mohammedarafat/major_project/amazon_pages/data.csv", index=False)
print("File has been Saved Sucessfully!!!")



## EXTRACT HEADLINES AND LINKS <a> TAG FROM A DYNAMICALLY LOADED PAGE. ##

# driver = webdriver.Chrome()

# url = "https://www.bbc.com/news/uk"
# driver.get(url)
# links = driver.find_elements(By.CSS_SELECTOR, '[data-testid="internal-link"]')


# print(f"Found {len(links)} <a> tags. \n")

# # save all link tags with headlines
# count = 0
# list_items = []
# for link in links:
#     href = link.get_attribute('href')

#     try:
#         headline = link.find_element(By.TAG_NAME, 'h2').text.strip()
#     except:
#         headline = "No headline found"
#     list_item = {
#         f"link_{count}": href,
#         f"headline_{count}": headline
#     }
#     list_items.append(str(list_item))
#     count += 1
# df = pd.DataFrame(list_items)
# print(df.head())
# with open("major_project/bbc_links_and_headlines/bbc_headlines_links.html", "w", encoding='utf-8') as f:
#     df.to_html(f, index=False)
# driver.close()



