import asyncio
from os.path import join, dirname, expanduser
from itertools import product
import sys, getopt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
from time import localtime, sleep, strftime, time, monotonic
import chromedriver_autoinstaller
import requests

__version__ = "0.0.1"


def read_config():
    """Read config from file."""

    # iterate folders and files
    for directory, filename in product(
        [
            ".",
            expanduser("~"),
        ],
        ["volvo.conf", ".volvo.conf"],
    ):
        try:
            # open folder / file
            config = join(directory, filename)
            with open(config) as config:
                # return the dictionary with parameters from config file
                return dict(
                    x.split(": ")
                    for x in config.read().strip().splitlines()
                    if not x.startswith("#")
                )
        except (IOError, OSError):
            # try next folder / file
            continue
    return {}


def WebDriverWait_and_find_element_by_xpath(driver, xpath, message):
    print("Waiting for element: {}".format(message))
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)
        
    print("Finding XPATH: {}".format(message))
    try:
        element = driver.find_element_by_xpath(xpath)
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)
    else:
        return element


def WebDriverWait_and_find_elements_by_xpath(driver, xpath, message):
    print("Waiting for element: {}".format(message))
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)
        
    print("Finding XPATH: {}".format(message))
    try:
        element = driver.find_elements_by_xpath(xpath)
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)
    else:
        return element


def WebDriverWait_and_find_element_by_id(driver, xpath, id, message):
    print("Waiting for element: {}".format(message))
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath)))
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)

    print("Finding ID: {}".format(message))
    try:
        element = driver.find_element_by_id(id)
    except Exception as e:
        print("Exception: {}".format(e))
        sys.exit(1)
    else:
        return element


def wait(seconds):
    start = time()
    while time() - start < seconds:
        print("Waiting for {} secs".format(round(seconds - (time() - start))))
        sleep(1)
        
        
async def main(argv):
    """Command line interface."""

    # Read config from config file
    config = read_config()
    api = ""

    # Get command line options
    try:
        opts, args = getopt.getopt(argv,"ha:",["api="])
    except getopt.GetoptError:
        print('volvo-selenium.py [-h] -a <api: connected/extended/energy>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('volvo-selenium.py [-h] -a <api: connected/extended/energy')
            sys.exit()
        elif opt in ("-a", "--api"):
            api = arg
            
    # Print results
    print("Login type: {}".format(config["login_type"]))
    print("Username: {}".format(config["dev_username"]))
    print("Password: ****") # .format(config["dev_password"])
    print("API: {}".format(api))
    print("Website: {}".format(config["website"]))

    chromedriver_autoinstaller.install()  

    options = webdriver.ChromeOptions()
    options.add_argument('ignore-certificate-errors')
#    options.add_argument('--headless') # No interface.
#    options.add_argument('--disable-gpu') # Combine with disable-gpu above.
    options.add_experimental_option("excludeSwitches", ["enable-logging"])

    driver = webdriver.Chrome(options=options)
    driver.get(config["website"])
    driver.set_window_position(0, 0)
    driver.set_window_size(1200, 800)
    print("Loading: {}".format(driver.current_url))
    print("Loaded: {}".format(driver.title))

    # Accept cookies
    # --------------
    # //*[@id="onetrust-accept-btn-handler"]
    # document.querySelector("#onetrust-accept-btn-handler")
    acceptcookies = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="onetrust-accept-btn-handler"]', "Accepting cookies")
    acceptcookies.click()
    
    # Login
    # --------------
    # //*[@id="main"]/div/nav[2]/div[1]/div[1]/div/div/div/button
    # //*[@id="main"]/div/nav[2]/div[1]/div[1]/div/div/div/button
    # document.querySelector("#main > div > nav.c.d.df.di.ei.ej.el.f.qq.qr.qs.qt.qu.qv.qw.qx.qy.qz.s > div.b.c.d.ei.ej.el.f.fj.ra.s > div.b.bl.ct.d.dg.ej.f.g.h.nk.nl.nm.nn.no.np.nq.nr.ns.q > div > div > div > button")
    # document.querySelector("#main > div > nav.c.d.df.di.ei.ej.el.f.qq.qr.qs.qt.qu.qv.qw.qx.qy.qz.s > div.b.c.d.ei.ej.el.f.fj.ra.s > div.b.bl.ct.d.dg.ej.f.g.h.nk.nl.nm.nn.no.np.nq.nr.ns.q > div > div > div > button")
    login = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="main"]/div/nav[2]/div[1]/div[1]/div/div/div/button', "Clicking login")
    login.click()

    if config["login_type"] == "github":
        print("Logging into github...")
        
        # GITHUB
        # //*[@id="kc-content-wrapper"]/div/div/a[2]
        # document.querySelector("#kc-content-wrapper > div > div > a.provider-link.button.outline.github")
        choose_github = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="kc-content-wrapper"]/div/div/a[2]', "Clicking Github")
        choose_github.click()

        # -- USERNAME
        # //*[@id="login_field"]
        # document.querySelector("#login_field")
        github_login_email = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="login_field"]', "Entering Github username")
        github_login_email.clear()
        github_login_email.send_keys(config["dev_username"])

        # -- PASSWORD
        # //*[@id="password"]
        # document.querySelector("#password")
        github_login_pwd = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="password"]', "Entering Github password")
        github_login_pwd.clear()
        github_login_pwd.send_keys(config["dev_password"])

        # -- SIGN IN
        # //*[@id="login"]/div[3]/form/div/input[11]
        # document.querySelector("#login > div.auth-form-body.mt-3 > form > div > input.btn.btn-primary.btn-block.js-sign-in-button")
        github_login = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="login"]/div[3]/form/div/input[11]', "Clicking Github login")
        github_login.click()
    elif config["login_type"] == "google":
        print("Logging into google...")
        
        # -- GOOGLE
        # //*[@id="kc-content-wrapper"]/div/div/a[3]
        # document.querySelector("#kc-content-wrapper > div > div > a.provider-link.button.outline.google")
        choose_google = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="kc-content-wrapper"]/div/div/a[3]', "Clicking Google")
        choose_google.click()

        # -- USERNAME
        # //*[@id="identifierId"]
        # document.querySelector("#identifierId")
        google_login_email = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="identifierId"]', "Entering Google username")
        google_login_email.clear()
        google_login_email.send_keys(config["dev_username"])

        # -- PASSWORD
        #
        #
        google_login_pwd = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="password"]', "Entering Google password")
        google_login_pwd.clear()
        google_login_pwd.send_keys(config["dev_password"])

        # -- NEXT
        # //*[@id="identifierNext"]/div/button
        # document.querySelector("#identifierNext > div > button")
        google_login = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="login"]/div[3]/form/div/input[11]', "Clicking Github login")
        google_login.click()
    else:
        print("Incorrect logintype...")
        sys.exit(1)

    # https://developer.volvocars.com/account/#api-test-access-tokens
    driver.get(config["website"]+'/account/#api-test-access-tokens')

    # //*[@id="accept-btn"]
    # document.querySelector("#accept-btn")
    signin = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="accept-btn"]', "Clicking Signin")
    signin.click()
    
    # -- API SELECTOR
    # document.querySelector("#vcc-ui-select-input-3")
    if api == "connected":
        print("Connected API...")
        # <option value="connected-vehicle-c3">Connected Vehicle API</option>
        # //*[@id="vcc-ui-select-input-3"]/option[text()="Connected Vehicle API"]
        choose_api = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="vcc-ui-select-input-3"]/option[text()="Connected Vehicle API"]', "Clicking Connected Vehicle API")
        choose_api.click()
    elif api == "energy":
        print("Energy API...")
        # <option value="energy-api">Energy API</option>
        # //*[@id="vcc-ui-select-input-3"]/option[text()="Energy API"]
        choose_api = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="vcc-ui-select-input-3"]/option[text()="Energy API"]', "Clicking Energy API")
        choose_api.click()
    elif api == "extended":
        print("Extended API...")
        # <option value="extended-vehicle-c3">Extended Vehicle API</option>
        # //*[@id="vcc-ui-select-input-3"]/option[text()="Extended Vehicle API"]
        choose_api = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="vcc-ui-select-input-3"]/option[text()="Extended Vehicle API"]', "Clicking Extended Vehicle API")
        choose_api.click()
    else:
        print("Incorrect API...")
        sys.exit(1)
        
    # -- AUTHORISE MY CAR
    # document.querySelector("#main > div > div > div > section:nth-child(3) > div:nth-child(13) > div > div.b.c.d.e.f.g.rg > div.b.c.d.e.f.g.si.sj.z > div > button")
    # //*[@id="main"]/div/div/div/section[2]/div[6]/div/div[2]/div[3]/div/button
    volvoid_authorise = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="main"]/div/div/div/section[2]/div[6]/div/div[2]/div[3]/div/button', "Clicking Authorise My Car")
    volvoid_authorise.click()

    # document.querySelector("#loginField")
    # //*[@id="loginField"]
    volvoid_login_email = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="loginField"]', "Entering Volvo ID username")
    volvoid_login_email.clear()
    volvoid_login_email.send_keys(config["volvoid_username"])

    # document.querySelector("#pwdField")
    # //*[@id="pwdField"]
    volvoid_login_pwd = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="pwdField"]', "Entering Volvo ID password")
    volvoid_login_pwd.clear()
    volvoid_login_pwd.send_keys(config["volvoid_password"])

    # document.querySelector("#loginButton")
    # //*[@id="loginButton"]
    volvoid_login = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="loginButton"]', "Clicking Volvo ID Signin")
    volvoid_login.click()

    # -- SHOW
    # document.querySelector("#main > div > div.a.gj.gk > div > section:nth-child(3) > div:nth-child(13) > div > div:nth-child(1) > div > div.dd.dw.rk.rl.rm.rn.ro.rp.rq.rr.v > div.a.p.rt > div > div.b.c.d.e.f.g.is.jw.n.se.sf.sg.sh.si.sj.sk > button")
    # //*[@id="main"]/div/div[1]/div/section[2]/div[6]/div/div[1]/div/div[1]/div[2]/div/div[2]/button/em
    show_token = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="main"]/div/div[1]/div/section[2]/div[6]/div/div[1]/div/div[1]/div[2]/div/div[2]/button/em', "Clicking Show")
    show_token.click()

    # -- TOKEN ELEMENT
    # <p class="a aj ak al an ap ar at av ax az fc fd ff fg fj fk fn fo is ld le sb sc sd">****</p>
    # document.querySelector("#main > div > div.a.gj.gk > div > section:nth-child(3) > div:nth-child(13) > div > div:nth-child(1) > div > div.dd.dw.rk.rl.rm.rn.ro.rp.rq.rr.v > div.a.p.rt > div > div.b.c.cv.d.e.f.g.is.nq.p.ry.v > div > p")
    # //*[@id="main"]/div/div[1]/div/section[2]/div[6]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/p
    token_field = WebDriverWait_and_find_element_by_xpath(driver, '//*[@id="main"]/div/div[1]/div/section[2]/div[6]/div/div[1]/div/div[1]/div[2]/div/div[1]/div/p', "Selecting token")
    generated_token = token_field.get_attribute('innerHTML')

    # -- COPY
    # document.querySelector("#main > div > div.a.gj.gk > div > section:nth-child(3) > div:nth-child(13) > div > div:nth-child(1) > div > div.dd.dw.rk.rl.rm.rn.ro.rp.rq.rr.v > div.a.sq > div > div > button")
    #
    # -- not used

    url = "https://api.volvocars.com/connected-vehicle/v1/vehicles"

    payload={}
    headers = {
      'Accept': 'application/vnd.volvocars.api.connected-vehicle.vehiclelist.v1+json',
      'Authorization': 'Bearer ' + generated_token,
      'vcc-api-key': config["vcc_apikey"]
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)

    wait(60)

    print("Closing driver...")
    driver.close()

    print("Done!")

    wait(60)

if __name__ == "__main__":
    try:
        from asyncio import run
    except ImportError:
        # pre 3.7

        def run(fut, debug=False):
            loop = asyncio.get_event_loop()
            loop.set_debug(debug)
            loop.run_until_complete(fut)
            loop.close()

        asyncio.create_task = lambda coro: asyncio.get_event_loop().create_task(
            coro
        )

    try:
        run(main(sys.argv[1:]))
    except KeyboardInterrupt:
        print("Closing driver...")
        driver.close()
        exit()
