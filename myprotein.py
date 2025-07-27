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
        try:
            with open(user_data, "r") as file:
                data = json.load(file)
            if not data:
                raise FileNotFoundError(f"Could not load {user_data}.")
        except Exception as e:
            print(f"Error while loading user data: {e}")
            sys.exit(1)
        
        self.data = data
        
        self.product_url = data["productUrl"]
        
        account_data = data["myProteinAccountData"]
        self.email = account_data["myproteinUsername"]
        self.password = account_data["myproteinPassword"]
        
        smtp_data = data["smtp"]
        self.smtp_name = smtp_data["username"]
        self.smtp_password = smtp_data["password"]
        self.port = smtp_data["port"]
        self.server = smtp_data["server"]
        
        self.required_discount = data["notifyWhenDiscount"]
        
        self.promo_code = data["promoCode"]
                
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
    '''
    def sign_in(self):
        try:
            subprocess.run(r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe Set-WinUserLanguageList en-US -Force", shell=True)
            
            #print(self.driver.current_url})
            print("Opening the sign-in page")
            self.driver.get(self.product_url)

            #waiting for email field to show up
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="email"]'))
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
                EC.presence_of_element_located((By.XPATH, '//input[@name="password"]'))
            )
            password_input.send_keys(self.password)
            print("Password entered")


            #clicking on "Prijava" button
            prijava_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="login_submit_button"]'))
            )
            prijava_button.click()
            print("'Prijava' button has been clicked")

            #print(self.driver.current_url)
            time.sleep(10)
            if("/account" in self.driver.current_url):
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
    '''
    
    def add_product_to_basket(self):
        self.driver.get(self.product_url)
    
        cookies_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@id="onetrust-accept-btn-handler"]'))
        )
        cookies_button.click()
        
        add_to_basket_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@data-e2e="product_add-to-basket"]'))
        )
        add_to_basket_button.click()
        print("'Add to basket' button has been clicked")
        

    def go_to_basket(self):
        #time.sleep(10)
        try:
            print("Getting to the basket page")


            wait = WebDriverWait(self.driver, 10)
            basket_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-e2e="product_go-to-basket"]')))

            basket_link.click()

            wait.until(EC.url_contains("/basket/"))
        
            print("Clicked the basket button")
            
            time.sleep(10)
            #print(self.driver.current_url)
            if("/basket" in self.driver.current_url):
                print("Basket page loaded successfully")

        except Exception as e:
            self.driver.save_screenshot("go_to_basket_error.png")
            print(f"Error while going to the basket page: {e}")
            self.send_mail("Myprotein scraper error", f"Error while going to the basket page: {e}")
            sys.exit(1)

            
            
    def input_code(self):
        try:
            wait = WebDriverWait(self.driver, 20)

            #dismiss cookie pop-up
            try:
                consent_button = wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR,
                    "#onetrust-accept-btn-handler"
                )))
                consent_button.click()
                print("Closed cookie pop-up")
            except:
                print("No cookie pop-up to close")

            promo_code_input = wait.until(EC.element_to_be_clickable((By.ID, "promo-code-input")))
            promo_code_input.send_keys(self.promo_code)

           #scroll into view
            self.driver.execute_script("""
                const button = document.getElementById('promo-code-add');
                button.scrollIntoView({behavior: 'smooth', block: 'center'});
                setTimeout(() => button.click(), 100); 
            """)
            time.sleep(2)

            wait.until(EC.element_to_be_clickable((By.ID, "promo-code-add"))).click()

        except Exception as e:
            print(f"Error while inputing discount code: {e}")
            self.send_mail("Myprotein scraper error", f"Error while inputing discount code: {e}")
            sys.exit(1)

        
    def extract_discount_percentage(self):
        try:
            time.sleep(5)

            percentages = self.driver.find_elements(By.XPATH, '//*[contains(text(), "%")]')
            valid_percentages = []

            for percent in percentages:
                tag_name = percent.tag_name.lower()
                if tag_name in ["style", "script"]:
                    continue

                text = self.driver.execute_script("return arguments[0].textContent;", percent).strip()

                if re.search(r'(width|padding|margin|opacity|font|border|background)[\s:-]*\d+%', text, re.IGNORECASE):
                    continue
                        
                #print(text)

                if "!" in text:
                    match = re.search(r"(\d+)%", text)
                    percentage = int(match.group(1))
                    valid_percentages.append(percentage)

            if valid_percentages:
                return valid_percentages[0]
               

            raise Exception("No percentage with !")

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
        #self.sign_in()
        self.add_product_to_basket()
        self.go_to_basket()
        self.input_code()
        
        discount_percentage = self.extract_discount_percentage()
        
        if (discount_percentage >= self.required_discount):            
            self.send_mail(f"Myprotein discount is over {self.required_discount}%", f"The discount is currently at {discount_percentage}%")

if __name__ == "__main__":

    scraper = MyProteinScraper("userdata.json")

    scraper.run()
