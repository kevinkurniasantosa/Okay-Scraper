import re
import requests
from bs4 import BeautifulSoup
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import string

print('import successful')

###################### CAN BE CUSTOMIZED
url = [
    'https://www.okay.com/en/property/rent/great-george-building/297720'
    # 'https://www.okay.com/en/property/rent/riviera-mansion/287286'
]
output_filename = 'output.json'

######################

# SETUP
output_arr = []
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable_infobars')
chrome_options.add_argument("--window-size=400,700")
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(options=chrome_options)

def run_scraping():
    for input_url in url:
        print('Start scraping ' + input_url)

        res = requests.get(input_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # driver.get(input_url)
        # soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        try:
            sku_id = soup.find('div', class_='c-prophead__id').text.strip()
            x = re.match('ID: (.+)', str(sku_id))
            sku_id = x.group(1)
        except:
            sku_id = '-'
        print('ID: ' + str(sku_id))

        try:
            title = soup.find('div', class_='c-prophead__titlegroup').find('h1', class_='c-prophead__title').text.strip()
        except:
            title = '-'
        print('Title: ' + title)

        try:
            description = soup.find('div', class_='c-proptext__text').text.strip()
        except:
            description = '-'
        print('Description: ' + description)

        try:
            price = soup.find('span', class_='c-prophead__current--short').text
            try:
                x = re.match('(.+).+(Incl.)', str(price))
                price = x.group(1)
            except:
                pass
        except:
            price = '-'
        print('Price: ' + price)

        try:
            driver.get(input_url)
            wait = WebDriverWait(driver,5)
            contact_button = wait.until(lambda driver: driver.find_element_by_xpath("//a[@class='c-calloremail__item c-calloremail__item--main']"))
            contact_button.click()

            whatsapp_button = wait.until(lambda driver: driver.find_element_by_xpath("//div[@class='c-replybar__actions']"))
            whatsapp_tag = whatsapp_button.find_element_by_tag_name('a')
            whatsapp_link = whatsapp_tag.get_attribute('href')
            z = re.match('.+\/(\d+)\?', str(whatsapp_link))
            phone = z.group(1)  
        except:
            phone = '-'
        print('Phone : ' + str(phone))
            
        image_url_arr = []
        list_images = soup.find_all('div', class_='c-propslider__slide')

        for image in list_images:
            image_url = image.find('img')['src']
            image_url_arr.append(image_url)
        print('Image URL: ' + str(image_url_arr))

        ############################################

        json_output = {
            "id": sku_id,
            "title": title,
            "description": description,
            "price": price,
            "phone": phone,
            "images": [
            ]
        }

        image_url_len = len(image_url_arr)
        for y in range(image_url_len):
            each_image_url = {
                "url": image_url_arr[y]
            }
            json_output['images'].append(each_image_url)

        output_arr.append(json_output)
        
    with open(output_filename, 'w') as output_file:
        # output_arr = {"MetaData": {}, "SRData": dResult}
        json_arr = json.dump(output_arr, output_file, sort_keys=False, indent=4)

################################################
################################################
## START HERE

run_scraping()
print('---------------------')
print('Scraping successful')




