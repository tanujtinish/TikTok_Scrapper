from urllib.parse import urlencode, quote, urlparse

import requests

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from src.services.CaptchaSolver.Solver import TikTokCaptchaSolver

class TiktTokRecommendationBrowserSession:
    def __init__(self, ms_token, headless=True, proxy=None):
        # Initialize a headless Selenium browser session
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-dev-shm-usage");
        options.add_argument("--no-sandbox");
        options.add_argument("--disable-setuid-sandbox");
        options.add_argument("--headless")
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        
        # self.browser = webdriver.Chrome(options=options)
        # self.browser = webdriver.Remote(
        # 'http://localhost:4444/wd/hub',
        #     options=options,
        # )
        self.browser = webdriver.Remote(
        command_executor='http://headless_chrome:3000/webdriver',
            options=options,
        )
        
        self.browser.get("https://www.tiktok.com")
        
        self.ms_token = ms_token# Set cookies (replace with your cookies)
        self.browser.add_cookie({"name": "msToken", "value": self.ms_token})
        
        # self.solve_captcha()
        # self.close_signup_box()

    def solve_captcha(self):
        try:
            res = TikTokCaptchaSolver(
                device_id=7297801250002699819, install_id=0
            ).solve_captcha()
        
            while(res["code"]==500):
                
                res = TikTokCaptchaSolver(
                        device_id=7297801250002699819, install_id=0
                    ).solve_captcha()
        except Exception as e:
            pass
    
    def close_signup_box(self):
        try:
            WebDriverWait(self.browser, 4).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#login-modal > div.tiktok-1ecw34m-DivCloseWrapper.e1gjoq3k6'))
            )
            self.browser.find_element(By.CSS_SELECTOR, '#login-modal > div.tiktok-1ecw34m-DivCloseWrapper.e1gjoq3k6').click()
        except Exception as e:
            pass

    def close_session(self):
        self.browser.quit()

    def get_headers(self):
        return self.headers

    def get_cookies(self):
        return self.browser.get_cookies()

    def generate_x_bogus(self, url):
        x_bogus = self.browser.execute_script(f'return window.byted_acrawler.frontierSign("{url}")')
        return x_bogus

    def sign_url(self, url):
        x_bogus = "DFSzswVYJD2ANHqMtFMwpU9WcBny"
        # x_bogus = self.generate_x_bogus(url) 
        if "?" in url:
            return f"{url}&X-Bogus={x_bogus}"
        else:
            return f"{url}?X-Bogus={x_bogus}"

    def make_request(self, url, params=None):
        # Set the session headers including missing parameters
        headers = {
            "User-Agent": self.browser.execute_script("return navigator.userAgent"),
            "Accept-Language": self.browser.execute_script("return navigator.language || navigator.userLanguage"),
            "Platform": self.browser.execute_script("return navigator.platform"),
            "msToken": self.ms_token,
            "Cookie": f"msToken={self.ms_token};",
            "aid": "1988",
            "app_language": "en",
            "app_name": "tiktok_web",
            "browser_language": "en-GB",
            "browser_name": "Mozilla",
            "browser_online": "true",
            "browser_platform": "MacIntel",
            "channel": "tiktok_web",
            "clientABVersions": "70508271,71141826,71148491,71217864,71303179,71325544,71497445,71554598,71583918,71602041,71605987,71610717,71619656,71620049,71625632,71640357,71662599,71668139,71671791,71686262,50070521,50077909,50089479,70405643,70772958,71057832,71200802,71381811,71516509,71662362,71680683,71691165",
            "cookie_enabled": "true",
            "coverFormat": "2",
            "device_platform": "web_pc",
            "device_type": "web_h264",
            "focus_state": "false",
            "from_page": "fyp",
            "history_len": "3",
            "isNonPersonalized": "false",
            "is_fullscreen": "false",
            "is_page_visible": "true",
            "language": "en",
            "os": "mac",
            "priority_region": "",
            "pullType": "2",
            "referer": "",
            "region": "US",
            "root_referer": "https://www.tiktok.com/foryou?lang=en",
            "screen_height": "900",
            "screen_width": "1440",
            "tz_name": "America/Chicago",
            "verifyFp": "verify_lokwbxw0_XFehFvEk_MNw5_4kbH_BwTG_xfZ7kc5dNUi1",
            "watchLiveLastTime": "",
            "webcast_language": "en",
            "device_id":"7297801250002699819"          
        }
                
        if params:
            url = f"{url}?{urlencode({**headers, **params}, quote_via=quote)}"
            signed_url = self.sign_url(f"{url}")
        else:
            url = f"{url}?{urlencode({**headers}, quote_via=quote)}"
            signed_url = self.sign_url(url)
        
        try:
            # Execute JavaScript to make the API request (e.g., using fetch or XMLHttpRequest)
            # self.browser.set_script_timeout(60)
            # api_response = self.browser.execute_script(f'''
            #     var xhr = new XMLHttpRequest();
            #     xhr.open("GET", "{signed_url}", true);
            #     xhr.send();
            #     var res= xhr.responseText;
            #     return res
            # ''')
            response = requests.get(signed_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the JSON response
                data = response.json()
                return data
            else:
                print(f"Failed to retrieve data. Status code: {response.status_code}")
                return {"itemList":[]}
        except Exception as e:
            print(f"Failed to retrieve data. Error: {e}")
            return {"itemList":[]}
            
    
    def solve_captcha_for_other_sessions(self, url):
        print(f"solving captcha for other sessions using link {url}")
        self.browser.switch_to.new_window('tab')
        self.browser.get(url)
        
        # Maximum time to wait for CAPTCHA (in seconds)
        timeout = 2
        try:
            # Wait for the CAPTCHA element to become visible
            captcha_elem = WebDriverWait(self.browser, timeout).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.captcha_verify_img--wrapper'))
            )
            
            print("Found captcha")
            # Solve the CAPTCHA
            print("Closing captcha...")
            self.solve_captcha()
            print("Closed captcha")

        except Exception as e:
             pass
        
        try:
            signup_box_div = self.browser.find_element(By.ID, 'loginContainer')
            
            if(signup_box_div):
                print("Found signup_box Pop up Box")
                # Close the signup box (if it appears)
                self.close_signup_box()
                print("Closing sign up box...")
                self.close_signup_box()
                print("Closed sign up box")
                

        except Exception as e:
            pass
            
        
        
