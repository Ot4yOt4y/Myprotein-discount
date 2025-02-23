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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import sys
import subprocess

class MyProteinScraper:
    def __init__(self, user_data):
        self.login_url = "https://si.myprotein.com/login.jsp?returnTo=https%3A%2F%2Fsi.myprotein.com%2FaccountHome.account"
        
        try:
            with open(user_data, "r") as file:
                data = json.load(file)
            if not data:
                raise FileNotFoundError(f"Could not load {user_data}.")
        except Exception as e:
            print(f"Error while loading user data: {e}")
            sys.exit(1)
        
        self.data = data
        
        account_data = data["myProteinAccountData"]
        self.email = account_data["myproteinUsername"]
        self.password = account_data["myproteinPassword"]
        
        smtp_data = data["smtp"]
        self.smtp_name = smtp_data["user"]
        self.smtp_password = smtp_data["password"]
        self.port = smtp_data["port"]
        self.server = smtp_data["server"]
                
        self.driver = None


    def driver_setup(self):
        options = Options()

        options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent Selenium detection
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")  # Set a realistic User-Agent

        #for background running
        options.add_argument("--headless=new") 

        try:
            self.driver = uc.Chrome(options=options)
        except Exception as e:
            print(f"Error while setting up Chrome WebDriver: {e}")
            sys.exit(1)

    def sign_in(self):
        try:
            subprocess.run(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Set-WinUserLanguageList en-US -Force", shell=True)
            
            #print(self.driver.current_url})
            print("Opening the sign-in page")
            self.driver.get(self.login_url)

            #waiting for email field to show up
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="E-poštni naslov"]'))
            )

            #name_input.clear();
            #pyperclip.copy("")
            actions = ActionChains(self.driver)
            time.sleep(5)
            
            for chr in self.email:
                if chr == "@":
                    #actions.key_down(Keys.CONTROL).key_down(Keys.ALT).send_keys("v").key_up(Keys.ALT).key_up(Keys.CONTROL).perform()
                    #name_input.send_keys(Keys.CONTROL, Keys.ALT, "v")
                    #pyperclip.copy("@")
                    #name_input.send_keys(Keys.CONTROL, "v")
                                        
                    actions.key_down(Keys.SHIFT).send_keys("2").key_up(Keys.SHIFT).perform();                
                    
                else:
                    name_input.send_keys(chr)

            print("Username entered")
            

            #waiting for password field to show up and entering password
            password_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="Geslo"]'))
            )
            password_input.send_keys(self.password)
            print("Password entered")


            #clicking on "Prijava" button
            prijava_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-testid="button-submit-login"]'))
            )
            prijava_button.click()
            print("'Prijava' button has been clicked")

            '''
            #check if account page is loaded
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//h1[contains(text(), "domača stran računa")]'))
            )
            '''    
            #print(self.driver.current_url)
            time.sleep(10)
            if("/accountHome.account" in self.driver.current_url):
                print("Successfully signed in!")       

            
            subprocess.run(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Set-WinUserLanguageList en-SI -Force", shell=True)    

        except Exception as e:
            self.driver.save_screenshot("sign_in_error.png")
            print(f"Error during sign-in: {e}")
            self.send_mail("Myprotein scraper error", f"Error during sign-in: {e}")
            sys.exit(1)
            
            #print(self.driver.page_source)
        #finally:
            #self.driver.quit()


    def go_to_basket(self):
        #time.sleep(10)
        try:
            print("Getting to the basket page")

            #locate and click basket button
            basket_button = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, '//a[@href="/my.basket"]'))
            )

            #for stale element exception
            #basket_button = self.driver.find_element(By.XPATH, '//a[@href="/my.basket"]')
            
            basket_button.click()
            print("Clicked the basket button")
            
            time.sleep(10)
            #print(self.driver.current_url)
            if("/my.basket" in self.driver.current_url):
                print("Basket page loaded successfully")

        except Exception as e:
            self.driver.save_screenshot("go_to_basket_error.png")
            print(f"Error while going to the basket page: {e}")
            self.send_mail("Myprotein scraper error", f"Error while going to the basket page: {e}")
            sys.exit(1)

            
            
    def input_code(self):
        try:
            #input promo code
            promo_code_bracket = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@class="athenaBasket_discountEntryInput"]'))
            )
            promo_code_bracket.send_keys("PIAFIT")
            
            #move cursor so overlay disappears
            ActionChains(self.driver) \
                .move_by_offset(7, 9) \
                .perform()
            
            #click on "unovči kodo" button
            unocvi_kodo_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@class="athenaBasket_discountEntryButton"]'))
            )
            unocvi_kodo_button.click()
                    
        except Exception as e:
            print(f"Error while inputing discount code: {e}")
            self.send_mail("Myprotein scraper error", f"Error while inputing discount code: {e}")
            sys.exit(1)
            
        
    def extract_discount_percentage(self):
        try:
            #wait for the discount to appear
            discount = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "athenaBasket_totalSavingsMessage"))
            )

            discount_text = discount.text
            #print(discount_text)

            #extract the discount percentage
            match = re.search(r"(\d+)%", discount_text)
            if match:
                discount_percentage = int(match.group(1))  #to integer
                print(f"Discount Percentage: {discount_percentage}%")
                return discount_percentage
            else:
                raise Exception("No discount percentage found.")

        except Exception as e:
            print(f"Error while extracting the discount: {e}")
            self.send_mail("Myprotein scraper error", f"Error while extracting the discount: {e}")
            sys.exit(1)    
    
    def send_mail(self, subject, text):
        try:
            email_from = self.smtp_name
            email_to = self.data["emailRecipient"]
            
            message = MIMEMultipart()
            message["From"] = email_from
            message["To"] = email_to
            message["Subject"] = subject
            
            email_text = text
            
            message.attach(MIMEText(email_text, "plain"))
            
            #setting up gmail SMTP server
            with smtplib.SMTP(self.server, self.port) as server:
                server.starttls()
                server.login(self.smtp_name, self.smtp_password)
                server.sendmail(email_from, email_to, message.as_string())
                print("Email sent")
            
        
        except Exception as e:
            print(f"Error while sending email: {e}")
            sys.exit(1)
            
        finally:
            self.driver.quit()
    
    def run(self):
        self.driver_setup()
        self.sign_in()
        self.go_to_basket()
        self.input_code()
        
        discount_percentage = self.extract_discount_percentage()
        
        if (discount_percentage >= 50):            
            self.send_mail("Myprotein discount is over 50%", f"The discount is currently at {discount_percentage}%")

if __name__ == "__main__":

    scraper = MyProteinScraper("userdata.json")

    scraper.run()
