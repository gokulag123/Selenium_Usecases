import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

op = Options()
op.add_argument('--start-maximized')
# op.add_argument("--incognito")
op.add_argument('--disable-notifications')
driver = webdriver.Chrome(options=op)
driver.implicitly_wait(6)
actions = ActionChains(driver)


class Test_usecase:

    def __init__(self, username, password):
        self.user = username
        self.password = password
        self.login()

    def login(self):
        driver.get("https://login.salesforce.com/")
        driver.find_element(By.CSS_SELECTOR, "#username").send_keys(self.user)
        driver.find_element(By.CSS_SELECTOR, "#password").send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, "#Login").click()

    def new_lead(self, firstname, lastname, company):
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id='Lead']/one-app-nav-bar-item-dropdown"))
        )

        lead = driver.find_element(By.XPATH,
                                   "//one-app-nav-bar-item-root[@data-id='Lead']/one-app-nav-bar-item-dropdown")
        actions.move_to_element(lead).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='New Lead']")))

        new_lead = driver.find_element(By.XPATH, "//span[text()='New Lead']")
        actions.move_to_element(new_lead).click().perform()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[class='isModal inlinePanel oneRecordActionWrapper']"))
        )
        driver.find_element(By.XPATH, "//span[text()='--None--']").click()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item/span/span[text()='Mr.']"))
        )

        driver.find_element(By.XPATH, "//lightning-base-combobox-item/span/span[text()='Mr.']").click()
        driver.find_element(By.XPATH, "//div/input[@placeholder='First Name']").send_keys(firstname)
        driver.find_element(By.XPATH, "//div/input[@placeholder='Last Name']").send_keys(lastname)
        driver.find_element(By.XPATH, "//input[@name='Company']").send_keys(company)
        driver.find_element(By.XPATH, "//button[text()='Save']").click()
        fullname = firstname + ' ' + lastname

        driver.execute_script("document.querySelector('.forceVisualMessageQueue').style.display='none';")
        time.sleep(1)          #removed fails#
        # verify new lead which was created
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id='Lead']/one-app-nav-bar-item-dropdown"))
        )

        lead = driver.find_element(By.XPATH,
                                   "//one-app-nav-bar-item-root[@data-id='Lead']/one-app-nav-bar-item-dropdown")
        actions.move_to_element(lead).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{fullname}']")))

        new_one = driver.find_element(By.XPATH, f"//span[text()='{fullname}']")
        actions.move_to_element(new_one).click().perform()
        print('New Lead name: ',
              driver.find_element(By.XPATH, "//lightning-formatted-name[@data-output-element-id='output-field']").text)
        print('Status: ', driver.find_element(By.XPATH,
                                              "//records-record-layout-item[@field-label='Lead Status']//lightning-formatted-text[@slot='outputField']").text)
        # Converting Lead to account
        driver.find_element(By.XPATH,
                            "//div[@class='windowViewMode-normal oneContent active lafPageHost']//button[text()='Convert']").click()
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//span[normalize-space(text())='Choose Existing Account']"))
        )
        driver.find_element(By.XPATH, "//span[normalize-space(text())='Choose Existing Account']").click()
        driver.find_element(By.XPATH, "//span[normalize-space(text())='Create New Account']").click()
        driver.find_element(By.XPATH, '//div[@class="modal-footer slds-modal__footer"]/span/button').click()
        time.sleep(3)
        driver.save_screenshot("lead_convert.png")
        driver.find_element(By.XPATH, "//button[@title='Close this window']").click()
        # Checking the converted account
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown"))
        )
        action = ActionChains(driver)
        account_dropdown = driver.find_element(By.XPATH,
                                               "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown")
        action.move_to_element(account_dropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{company}']"))
        )
        new_acc = driver.find_element(By.XPATH, f"//span[text()='{company}']")
        action.move_to_element(new_acc).click().perform()
        print('Account name: ', driver.find_element(By.XPATH, "//lightning-formatted-text[@slot='primaryField']").text)

        driver.close()


c1 = Test_usecase("gokul.gangadhara-6rcu@force.com", "Tiger@1234")
c1.new_lead("Raman", "Kartha", "Indigo")
