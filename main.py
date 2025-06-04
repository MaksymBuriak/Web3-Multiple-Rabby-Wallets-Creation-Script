import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import tempfile
from config import password, amount


# Create fake_useragent
fake_useragent = UserAgent()

EXTENSION_DIR = os.path.join(os.getcwd(), "rabby_unpacked")

print('Start of creating wallets:')
print('------------------------------')

# Using "try" - "except" block to catch any errors and print them out
try:
    # Will be creating {n} wallets
    for i in range(0, amount):
        options = Options()
        user_data_dir = tempfile.mkdtemp()
        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--load-extension={EXTENSION_DIR}")
        options.add_argument("--disable-extensions-except=" + EXTENSION_DIR)
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Adding a random UserAgent to the options
        options.add_argument(f'user-agent={UserAgent().random}')
        # Disabling detection of a webdriver
        options.add_argument('--disable-blink-features=AutomationControlled')
        # Web-browser UI will not be loaded
        options.add_argument('--headless=new')
        # Using Driver Manager automatically installing a chromium webdriver and sending the options to it
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)
        time.sleep(3)
        # Open Rabby Wallet extension web-page
        driver.get('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html#/new-user/guide')
        time.sleep(3)

        # Switch browser displayed and active window to the very first one
        handles = driver.window_handles
        driver.switch_to.window(handles[0])
        time.sleep(3)

        driver.find_element(by=By.XPATH, value = '/html/body/div/div/div/div[2]/button[1]').click() # Find and click "Create New Wallet"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/button')))
        driver.find_element(by=By.XPATH, value = '/html/body/div/div/div/button').click() # Find and click "Show Seed Phrase"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[4]/div[1]/span')))
        seedka = ''
        # Manually going through each separate item in the seed and adding it to the seedka variable with the correct layout
        for j in range (1, 13):
            seedka = seedka + f"{driver.find_element(by=By.XPATH, value=f'//*[@id="root"]/div/div/div[4]/div[{j}]/span').get_attribute('innerText')}" + ' '
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/button')))
        driver.find_element(by=By.XPATH, value = '//*[@id="root"]/div/div/button').click() # Find and click "I've saved Seed Phrase"
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="password"]')))
        driver.find_element(by=By.XPATH, value = '//*[@id="password"]').send_keys(password) # Input the password
        driver.find_element(by=By.XPATH, value = '//*[@id="confirmPassword"]').send_keys(password) # Confirm password
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div/form/footer/button')))
        driver.find_element(by=By.XPATH, value = '//*[@id="root"]/div/div/div/form/footer/button').click() # Click "Confirm password"
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/button')))
            driver.find_element(by=By.XPATH, value = '//*[@id="root"]/div/div/button').click() # Click "Let's gooo" or smth like this (wallet is created)
        except TimeoutException as err:
            print(f'\n{err} - Timeout, moving to the next wallet creation')
            driver.quit()
            continue

        # Open a Rabby wallet dashboard, due to the same active session no need to input password
        driver.get('chrome-extension://acmacodkjbdgmoleebolmdjonilkdbch/index.html')
        # Change the active window to the last-opened
        #handles = driver.window_handles
        #driver.switch_to.window(handles[-1])
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[1]/span/div[3]/div/div')))
            # Obtaining the 0x wallet address from the Rabby Wallet dashboard and saving it into code
            code = driver.find_element(by=By.XPATH, value='//*[@id="root"]/div/div[1]/div[1]/div[1]/span/div[3]/div/div').get_attribute('title')
        except TimeoutException:
            WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[2]/div[1]')))
            driver.find_element(by=By.XPATH, value = '//*[@id="root"]/div/div[3]/div[2]/div[1]').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/main/div/form/h1/span')))
            # Split the 12-word seed phrase into a list
            words = seedka.strip().split()
            # Loop through each word and input it into the corresponding box
            for index, word in enumerate(words):
                input_xpath = f'/html/body/div/main/div/form/div[1]/div[1]/div/div/div/div/div/div[2]/div[{index + 1}]/input'
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, input_xpath)))
                driver.find_element(By.XPATH, input_xpath).send_keys(word)
            time.sleep(1)
            driver.find_element(by=By.XPATH, value = '//*[@id="root"]/main/div/form/div[2]/button').click()
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="rc-tabs-0-panel-hd"]/div/div/div/div/div/div[2]/table/tbody/tr[2]/td[3]/div/span')))
            code = driver.find_element(By.XPATH, '//*[@id="rc-tabs-0-panel-hd"]/div/div/div/div/div/div[2]/table/tbody/tr[2]/td[3]/div/span').get_attribute('innerText')
        finally:
            # Write the wallet address, seed phrase into the file (if file is missing in the directory soft will generate it automatically)
            with open('result.txt', 'a') as f:
                f.write(f"{code}, {seedka}\n")
                f.close()

            print(f'Wallet {i+1} was created successfully!')

            # Close the driver after each iteration, so every next iteration will have a different user_agent, cookies, etc.
            driver.quit()
            i +=1
# Capturing any Exceptions (errors) during and printing them into the console. Then wait for user to see and investigate
except Exception as err:
    import traceback
    traceback.print_exc()
    print(err)
    driver.quit()  # Ensure browser exits cleanly
    time.sleep(999999)
finally:
    print('-----------------------------')
    print('Wallet creation complete!')





