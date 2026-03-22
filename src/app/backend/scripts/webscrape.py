from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re

def webscrape_week_threats():
    """Scrape the last week top 10 threats on each detection type  
    ...
    :return threat_list: A list of dictionaries which contains all threats scraped.
    """


    current_date = datetime.now().strftime("%Y-%m-%d")
    threat_list = []
    
    detection_types_dict = {"On-Access Scan": "OAS", "On-Demand Scan": "ODS", "Mail Anti Virus": "MAV", "Web Anti-Virus": "WAV", "Intrusion Detection Scan": "IDS", "Vulnerability Scan": "VUL", "Ransomware": "RMW", "Kaspersky Anti-Spam": "KAS"}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    for detection_type in detection_types_dict.keys():
        threat_index = 60
        threat_link_index = 10

        url_type = detection_types_dict[detection_type]
        url = f"https://cybermap.kaspersky.com/stats#country=215&type={url_type}&period=w"

        driver.get(url=url)
        driver.maximize_window()

        while threat_index <= 69 and threat_link_index <= 19:
            try:
                threat_name = driver.find_elements(By.CLASS_NAME, 'element_name')[threat_index].text
                threat_type = re.split(r'[.]', threat_name)[0]

                threat_value = driver.find_elements(By.CLASS_NAME, 'element_value')[threat_index].text
                threat_link = driver.find_elements(By.CLASS_NAME, 'threats_link')[threat_link_index].get_attribute('href')

                threat_list.append({
                    "Date of Collection": current_date,
                    "Country Stats Detection Type": detection_type,
                    "Threat Type": threat_type,
                    "Threat Name": threat_name,
                    "Threat Value (%)": threat_value,
                    "Threat Link": threat_link
                    })

            except IndexError:
                pass

            threat_index += 1
            threat_link_index += 1


    driver.quit()

    return threat_list

def threat_type_general_info_webscraper(element):

    blacklist = ["description", "read more", "find out the statistics of the vulnerabilities spreading in your region on statistics.securelist.com"]

    url=f"https://threats.kaspersky.com/en/class/{element}/"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get(url=url)
    driver.maximize_window()

    time.sleep(2)

    description_pos = 2
    description_list = []

    try:
        while True:
            element_description = driver.find_elements(By.TAG_NAME, "p")[description_pos].text

            if element_description.lower() in blacklist:
                pass
            else:
                description_list.append(element_description)

            description_pos += 1
    
    except IndexError:
        driver.quit()

    driver.quit()

    description = "\n".join(description_list)
    return description

def threat_info_webscraper(url):

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)

    time.sleep(2)
    
    driver.get(url=url)
    driver.maximize_window()

    content = driver.find_element(By.CLASS_NAME, "content").text

    parent_class_match = re.search(r"Parent class:(.*?)\n(.*?)(?=\nClass:)", content, re.DOTALL)
    class_match = re.search(r"Class:(.*?)\n(.*?)(?=\nRead more)", content, re.DOTALL)
    platform_match = re.search(r"Platform:(.*?)\n(.*?)(?=\n['Description', 'Family'])", content, re.DOTALL)

    try:
        if parent_class_match is not None:
            parent_class_name = parent_class_match.group(1).strip()
            parent_class_description = parent_class_match.group(2).strip()
        else:
            parent_class_name = "Not found"
            parent_class_description = "Not found"


        if class_match is not None:
            class_name = class_match.group(1).strip()
        else:
            class_name = "Not found"


        if platform_match is not None:
            platform_type = platform_match.group(1).strip()
            platform_description = platform_match.group(2).strip()
        else:
            platform_type = "Not found"
            platform_description = "Not found"

        driver.quit()

        return parent_class_name, parent_class_description, class_name, platform_type, platform_description
    
    except AttributeError:
        driver.quit()
