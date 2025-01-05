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



class MyProteinScraper:
    def __init__(self, email, password, smtp_name,smtp_password):
        self.login_url = "https://si.myprotein.com/login.jsp?returnTo=https%3A%2F%2Fsi.myprotein.com%2FaccountHome.account"
        self.email = email
        self.password = password
        self.driver = None
        self.smtp_name = smtp_name
        self.smtp_password = smtp_password

    def driver_setup(self):
        options = Options()

        options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent Selenium detection
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")  # Set a realistic User-Agent

        #for background running
        #options.add_argument("--headless") 

        self.driver = uc.Chrome(options=options)

    def sign_in(self):
        try:
            #print(self.driver.current_url})
            print("Opening the sign-in page")
            self.driver.get(self.login_url)


            #waiting for email field to show up
            name_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//input[@name="E-poštni naslov"]'))
            )

            name_input.clear();
            pyperclip.copy("")  #Clear the clipboard
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

        except Exception as e:
            print(f"Error during sign-in: {e}")
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
            print(f"Error while going to the basket page: {e}")
            
            
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
            print(f"An error while inputing discount code: {e}")
            
        
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
                print("No discount percentage found")
                return None

        except Exception as e:
            print(f"Error while extracting the discount: {e}")

            return None
    
    
    def send_mail(self, discount_percentage):
        try:
            email_from = self.smtp_name
            email_to = "seba.kauzar@gmail.com"
            email_subject = "Myprotein discount!!!"
            
            message = MIMEMultipart()
            message["From"] = email_from
            message["To"] = email_to
            message["Subject"] = email_subject
            
            email_text = f"The discount is currently at {discount_percentage}%"
            
            message.attach(MIMEText(email_text, "plain"))
            
            #setting up gmail SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.smtp_name, self.smtp_password)
                server.sendmail(email_from, email_to, message.as_string())
                print("Email sent")
            
        
        except Exception as e:
            print(f"Error while sending email: {e}")
            
        finally:
            self.driver.quit()
    
    def run(self):
        self.driver_setup()
        self.sign_in()
        self.go_to_basket()
        self.input_code()
        
        discount_percentage = self.extract_discount_percentage()
        
        if (discount_percentage > 50):            
            self.send_mail(discount_percentage)

if __name__ == "__main__":
    
    '''Replace with your own email and password used for myprotein account'''
    email = "seba.kauzar@gmail.com"
    password = "8u3UTNWrZSRsY!r"
    
    '''Replace these with your gmail name and password used for smtp'''
    smtp_name = "seba.kauzar@gmail.com"
    smtp_password = "wdlg jmet uwot xnnx"

    scraper = MyProteinScraper(email, password, smtp_name, smtp_password)

    scraper.run()
