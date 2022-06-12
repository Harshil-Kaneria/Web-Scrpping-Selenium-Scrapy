import sys, os
import time
import scrapy
from scrapy import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from openpyxl import Workbook


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(os.path.sep, ROOT_DIR,'chromedriver.exe')

save_file_name="Data.xlsx"
main_url = "https://amazon.in"
search_string = "sumsung phones"
page_wait = 5
total_page = 5

driver=webdriver.Chrome(executable_path=driver_path)
driver.maximize_window()
driver.get(main_url)
driver.implicitly_wait(page_wait)

driver.find_element(By.XPATH,"//input[contains(@id,'search')]").send_keys(search_string)
driver.find_element(By.XPATH,"//input[contains(@value,'Go')]").click()

name=[]
price=[]
link=[]

name.append("NAME")
name.append("")
price.append("PRICE")
price.append("")
link.append("LINK")
link.append("")

main_div = None
div_selector = None
def get_data():
    main_div = driver.find_elements(By.XPATH,"//div[contains(@class,'s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col s-widget-spacing-small sg-col-12-of-16')]")
    
    for single_div in main_div:
        div_selector = Selector(text=single_div.get_attribute('innerHTML'))

        try:
            name.append(div_selector.css("span.a-size-medium.a-color-base.a-text-normal::text").get())
        except:
            name.append('')

        try:
            price.append(div_selector.css("span.a-price-whole::text").get())
        except:
            price.append('')
        
        try:
            link.append(div_selector.css("a.a-size-base.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").attrib['href'])
        except:
            link.append('')



for i in range(total_page):
    get_data()
    print(i+1," Page Scaned !")
    try:
        driver.find_element(By.XPATH,"//a[contains(@class,'s-pagination-item s-pagination-next s-pagination-button s-pagination-separator')]").click()
    except:
        break;
    time.sleep(page_wait)



final_data = zip(name,price,link)



wb = Workbook()
ws = wb.active

for data in final_data:
    ws.append(data)

wb.save(save_file_name)
print("Done Developer")

driver.close()