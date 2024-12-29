from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc
import time
import random
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
import re



class MyProteinScraper:
    def __init__(self, email, password):
        self.login_url = "https://si.myprotein.com/login.jsp?returnTo=https%3A%2F%2Fsi.myprotein.com%2FaccountHome.account"
        self.email = email
        self.password = password
        self.driver = None

    def driver_setup(self):
        options = Options()

        options.add_argument("--disable-blink-features=AutomationControlled")  #prevents selenium detection
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")  # Set a realistic User-Agent

        #for background running
        #options.add_argument("--headless") 

        self.driver = uc.Chrome(options=options)

    def sign_in(self):
        try:
            print("Opening the sign-in page")
            self.driver.get(self.login_url)

            #waits for email field to show up
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="E-poštni naslov"]'))
            )
            #actions = ActionChains(self.driver)
            for chr in email:
                if chr == "@":
                    #actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("v").key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
                    #name_input.send_keys(Keys.CONTROL, Keys.ALT, "v")
                    pyperclip.copy("@")
                    name_input.send_keys(Keys.CONTROL, "v")
                else:
                    name_input.send_keys(chr)
            print("Username entered")

            #waits for password field to show up and enters password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="Geslo"]'))
            )
            password_input.send_keys(self.password)
            print("Password entered")

            #clicks on "Prijava" button
            prijava_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="button-submit-login"]'))
            )
            prijava_button.click()
            print("Clicked on 'Prijava' button")
            
            time.sleep(10)
            if("/accountHome.account" in self.driver.current_url):
                print("Successfully signed in!")       

        except Exception as e:
            print(f"Error during sign-in: {e}")
            #print(self.driver.page_source)
        #finally:
            #self.driver.quit()


    def run(self):
        self.driver_setup()
        self.sign_in()
       
       
if __name__ == "__main__":
    
    '''Replace these two with your own email and password'''
    email = "seba.kauzar@gmail.com"
    password = "8u3UTNWrZSRsY!r"

    scraper = MyProteinScraper(email, password)

    scraper.run()
