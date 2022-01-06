# -------- Currently under development --------
# Purpose to control objects on a webpage, so we can login and sort the news
# ---------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import traceback
from bs4 import BeautifulSoup

URL_SAMPLE = "https://www.python.org"
URL_SMH = "https://www.smh.com.au/login"

options = webdriver.ChromeOptions()
# options.add_argument("--profile-directory=Default")
# options.add_argument("--whitelisted-ips")
# options.add_argument("--start-maximized")
# options.add_argument("--disable-extensions")
# options.add_argument("--disable-plugins-discovery")
# options.add_argument("--headless")
driver = webdriver.Chrome(options=options)


def get_smsh():
    #<button class="_3oI1J" form="googleSignIn" type="submit" value="Continue with Google">
    # <span>Continue with Google</span></button>

    #<input type="email" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="username" spellcheck="false" tabindex="0" aria-label="Email or phone" name="identifier" autocapitalize="none" id="identifierId" dir="ltr" data-initial-dir="ltr" data-initial-value="wellia.lioeng@gmail.com" badinput="false">
    #<span jsname="V67aGc" class="VfPpkd-vQzf8d">Next</span>
    #<input type="password" class="whsOnd zHQkBf" jsname="YPqjbf" autocomplete="current-password" spellcheck="false" tabindex="0" aria-label="Enter your password" name="password" autocapitalize="off" dir="ltr" data-initial-dir="ltr" data-initial-value="Bulbul0127" badinput="false">
    #<button class="VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b" jscontroller="soHxf" jsaction="click:cOuCgd; mousedown:UX7yZ; mouseup:lbsD7e; mouseenter:tfO1Yc; mouseleave:JywGue; touchstart:p6p2H; touchmove:FwuNnf; touchend:yfqBxc; touchcancel:JMtRjd; focus:AHmuwe; blur:O22p3e; contextmenu:mg9Pef;" data-idom-class="nCP5yc AjY5Oe DuMIQc qIypjc TrZEUc lw1w4b" jsname="LgbsSe" type="button"><div class="VfPpkd-Jh9lGc"></div><div class="VfPpkd-RLmnJb"></div><span jsname="V67aGc" class="VfPpkd-vQzf8d">Next</span></button>
    #<span jsname="V67aGc" class="VfPpkd-vQzf8d">Next</span>


    #open url
    driver.get(URL_SMH)
    print(driver.title)
    # val = 60 # in seconds
    # driver.implicitly_wait(val)

    #click google login
    value = "Continue with Google"
    try:
        elements = driver.find_elements_by_class_name("_3oI1J")
        btn = elements[0]
        btn.click()
    except Exception:
        traceback.print_exc()
        driver.quit()

    #enter google email
    email_box = driver.find_element_by_xpath("//input[@type='email']")
    #upload_field = driver.find_element_by_css_selector("input[name='filePath'][type='file']")

    email_box.send_keys("user@gmail.com")
    email_box.send_keys(Keys.RETURN)

    #enter google password
    #https://myaccount.google.com/lesssecureapps
    # password_box = driver.find_element_by_xpath("//input[@type='password']")
    # password_box.send_keys("JanganMakanMartabak2020")
    # password_box.send_keys(Keys.RETURN)

    #driver.quit()

def main():
    get_smsh()

if __name__ == "__main__":
    main()


