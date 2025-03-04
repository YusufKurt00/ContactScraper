import os
import pandas as pd
import time
import re
import random
import gc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from openpyxl import load_workbook


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.205 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.6871.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4_0) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.1 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.2045.31 Safari/537.36 Edg/117.0.2045.31",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 AtContent/94.5.4701.42",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.137 Safari/537.36", # burdan sonra yeniler
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.4565.142 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Version/16.4 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.4643.69 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.4044.129 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.5022.74 Safari/537.36"
]


def init_driver():
    chrome_options = Options()
    #chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")  
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def chrome_ilk_site_bul(site, driver):
    
    try:
        query = f"https://www.google.com/search?q={site} website"
        driver.get(query)
          
        first_result = WebDriverWait(driver, 15).until(  
            EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
        )
        time.sleep(3)  
        first_result.click()

        WebDriverWait(driver, 15).until(  
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        current_url = driver.current_url
        return current_url 
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        print("Site bulunamadı. Website yazmadan arama yapılıyor...")
        
        try:

            query = f"https://www.google.com/search?q={site}"
            driver.get(query)
        
            first_result = WebDriverWait(driver, 15).until(  
                EC.element_to_be_clickable((By.CSS_SELECTOR, "h3"))
            )
            time.sleep(3)  
            first_result.click()

            WebDriverWait(driver, 15).until(  
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            current_url = driver.current_url
            return current_url 
        
        except Exception as e2:
            
            print(f"Hata oluştu: {e2}")
            return None

def html_kaynagi_al(url, driver):
    try:
        driver.get(url)
        WebDriverWait(driver, 20).until(  
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        html_content = driver.page_source
        time.sleep(1)  
        return html_content
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None

def email_getir(soup):
   
    email_pattern = [
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    ]
    emails=[]
    for email in email_pattern:
        emails.extend(re.findall(email, soup.get_text()))
    return emails

def telefon_getir(soup):
    
    phone_patterns = [
        r'((?:\+\d{1,3}[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}))',
        r'\(\d{3}\)\s\d{3}\s\d{5}',
        r'\b\+?\d{10,12}\b',
        r'(?:\+\d{1,3}[- ]?)?\(?\d{3}\)?[- ]?\d{3}\)?[- ]?\d{4}\b',
        r'\d{3}-\d{3}-\d{4}',  # 123-456-7890 format
        r'\+\d{1,3}\s\d{1,4}\s\d{4,10}'  # +90 532 1234567 format
    ]
    phone_numbers=[]
    for pattern in phone_patterns:
        phone_numbers.extend(re.findall(pattern, soup.get_text()))
        
    return phone_numbers

def contact_bolumu(soup):
    
    contact_links = []
    for link in soup.find_all('a', href=True):
        if 'contact' in link['href'].lower() or 'iletisim' in link['href'].lower() or 'kontakt' in link['href'].lower():
            contact_links.append(link['href'])
            
    return contact_links

def bilgi_topla(site, driver):
    
    print(f"İşleniyor: {site}")
    site_url = chrome_ilk_site_bul(site, driver)
    time.sleep(1)  
    
    if site_url is None:
        return [site, "Site Bulunamadı", "Email Bulunamadı", "Telefon Bulunamadı"]

    html_content = html_kaynagi_al(site_url, driver)
    if not html_content:
        return [site, site_url, "Email Bulunamadı", "Telefon Bulunamadı"]

    soup = BeautifulSoup(html_content, 'html.parser')

    emails = email_getir(soup)
    phone_numbers = telefon_getir(soup)

    if not emails or not phone_numbers:
        
        print("E-posta veya telefon bulunamadı. Contact bölümüne gidiliyor...")
        contact_links = contact_bolumu(soup)
        
        if contact_links:
            
            print(f"Contact linkleri: {contact_links}")
            contact_url = contact_links[0]
            contact_url = urljoin(site_url, contact_url)  
            time.sleep(1)
            html_content = html_kaynagi_al(contact_url, driver)
            soup = BeautifulSoup(html_content, 'html.parser')

            emails += email_getir(soup)
            phone_numbers += telefon_getir(soup)

    email = emails[0] if emails else "Email Bulunamadı"
    phone = phone_numbers[0] if phone_numbers else "Telefon Bulunamadı"
    return [site, site_url, email, phone]


def excelden_veri_cek(input_excel_path, output_excel_path, start_index=0):
      
    df = pd.read_excel(input_excel_path, header=None)

    driver = init_driver()
    driver.get("https://www.google.com")  
    time.sleep(2) 

    header = ["Site Adı", "Website Linki", "Email", "Telefon"]

    if not os.path.exists(output_excel_path):
        pd.DataFrame(columns=header).to_excel(output_excel_path, index=False)

    sayac=0
    
    for index, site in enumerate(df.iloc[:, 0]):  
        
        if index < start_index:
            continue
        
        if sayac % 10 == 0 and sayac != 0:
            driver.quit()  
            gc.collect()  # Memory cleaning
            sayac=0
            time.sleep(6)  
            driver = init_driver()  
            driver.get("https://www.google.com")
        
        result = bilgi_topla(site, driver)

        print(f"Site Adı: {result[0]}, Website Linki: {result[1]}, Email: {result[2]}, Telefon: {result[3]}")

        existing_data = pd.read_excel(output_excel_path)
        new_data = pd.DataFrame([result], columns=header)
        combined_data = pd.concat([existing_data, new_data], ignore_index=True)

        combined_data.to_excel(output_excel_path, index=False)

        sayac+=1
        time.sleep(random.randint(15, 20))  

    driver.quit()
        
input_excel_path = "example.xlsx"  
output_excel_path = "result.xlsx"  
startindex=334
excelden_veri_cek(input_excel_path, output_excel_path,startindex)


