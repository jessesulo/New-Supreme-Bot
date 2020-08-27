from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

class bot():
    def __init__(self, category, keyword, color, size):
        self.driver = self.loadNewDriver()
        self.category = category
        self.keyword = keyword.lower()
        self.color = color.lower()
        self.size = size

    #returns driver with properties
    def loadNewDriver(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0")
        profile.set_preference("javascript.enabled", False)

        options = webdriver.FirefoxOptions()
        #options.set_headless()

        d = webdriver.Firefox(firefox_profile=profile, options=options)
        return d

    #uses backlink and loads page
    def loadSupremePage(self):
        #backlink link
        self.driver.get("https://www.gq.com/story/supreme-online-sale-2020")
        self.waitForLoad()
        
        try:
            backlink = self.driver.find_element_by_xpath("//a[contains(@href,'https://www.supremenewyork.com/')]")
            backlink.click()
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
        except:
#MAKE THIS MORE DYNAMIC
            print("Backlink failed")
            self.driver.get("https://www.supremenewyork.com/")

        self.waitForLoad()
        return True

    #goes to category page
    def goToItemPage(self):
        print(self.driver.current_url)
        if(self.driver.current_url == "https://www.supremenewyork.com/"):
            self.waitForElement("//a[@href='/shop']")
            shopBtn = self.driver.find_element_by_xpath("//a[@href='/shop']")
            shopBtn.click()
            self.waitForRandom()

        self.waitForElement("//a[@href='http://www.supremenewyork.com/shop/all']")
        viewAll = self.driver.find_element_by_xpath("//a[@href='http://www.supremenewyork.com/shop/all']")
        viewAll.click()
        self.waitForRandom()
        
        if(self.category!="all"):
            section = self.driver.find_element_by_xpath("//a[@href='/shop/all/"+ self.category +"']")
            section.click()
        
        return True

    def lookForItem(self):
        elements = self.driver.find_elements_by_xpath("//li/div/div")
        for i in elements:
            if(i.get_attribute("class") == "product-name"):
                if(i.text.lower().find(self.keyword) >= 0):
                    if(elements[elements.index(i)+1].get_attribute("class") == "product-style"):
                        if(elements[elements.index(i)+1].text.lower().find(self.color) >= 0):
                            self.waitForRandom()
                            i.click()
                            self.waitForRandom()
                            self.waitForLoad()
                            self.addItemToCart()
                            return True
        return False

    def addItemToCart(self):
        sizes = self.driver.find_element_by_id("s")
        for i in sizes.find_elements_by_tag_name("option"):
            if(i.text.lower() == self.size.lower()):
                i.click()
        self.waitForRandom()
        self.driver.find_element_by_xpath("//input[@name='commit']").click()
        self.waitForRandom()
        self.driver.get("https://www.supremenewyork.com/checkout")

                
    #wait for page to be loaded
    def waitForLoad(self):
        try:
            element_present = EC.presence_of_element_located((By.XPATH,'//a/div'))
            WebDriverWait(self.driver, 2).until(element_present)
        except:
            print("Page not responding big oof")

    #wait for specific element to be loaded
    def waitForElement(self, element):
        try:
            element_present = EC.presence_of_element_located((By.XPATH,element))
            WebDriverWait(self.driver, 2).until(element_present)
        except:
            print("Page not responding big oof")

    #wait for a random time between 0-4 seconds
    def waitForRandom(self):
        r = random.uniform(1, 4)
        print(r)
        self.driver.implicitly_wait(r)


def main():
    b = bot("sweatshirts", "Portrait", "black", "medium")
    b.loadSupremePage()
    b.goToItemPage()
    b.lookForItem()
    input("Done! Press any key to continue.")
    b.driver.close()

main()
