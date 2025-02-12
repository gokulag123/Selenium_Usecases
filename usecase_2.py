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
driver.implicitly_wait(10)
action = ActionChains(driver)


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

    def new_acc(self,account,opportunity_name,closedate,stage,contact_name):
        time.sleep(1)
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown"))
        )
        account_dropdown = driver.find_element(By.XPATH,
                                               "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown")
        action.move_to_element(account_dropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='New Account']"))
        )
        new_acc = driver.find_element(By.XPATH, "//span[text()='New Account']")
        action.move_to_element(new_acc).click().perform()

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//div[@class='isModal inlinePanel oneRecordActionWrapper']//div/input[@class='slds-input' and @name='Name']"))
        )

        driver.find_element(By.XPATH, "//div/input[@class='slds-input' and @name='Name']").send_keys(account)
        driver.find_element(By.XPATH, "//button[text()='Save']").click()

        driver.execute_script("document.querySelector('.forceVisualMessageQueue').style.display='none';")

        # Checking account Creation
        time.sleep(1)  ##Then only it will show in recent accounts    #removed fails#
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown"))
        )
        account_dropdown = driver.find_element(By.XPATH,
                                               "//one-app-nav-bar-item-root[@data-id ='Account']/one-app-nav-bar-item-dropdown")
        action.move_to_element(account_dropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{account}']"))
        )
        new_acc = driver.find_element(By.XPATH, f"//span[text()='{account}']")
        action.move_to_element(new_acc).click().perform()
        assert driver.find_element(By.XPATH, "//lightning-formatted-text[@slot='primaryField']").text == account,"Name different"
        print('New Account : ',driver.find_element(By.XPATH, "//lightning-formatted-text[@slot='primaryField']").text )

        # Creating an oPPortunity and attaching to account
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id='Opportunity']/one-app-nav-bar-item-dropdown"))
        )

        oppdropdown = driver.find_element(By.XPATH,
                                          "//one-app-nav-bar-item-root[@data-id='Opportunity']/one-app-nav-bar-item-dropdown")
        action.move_to_element(oppdropdown).click().perform()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//span[text()='New Opportunity']"))
        )
        new_opp = driver.find_element(By.XPATH, "//span[text()='New Opportunity']")
        action.move_to_element(new_opp).click().perform()
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div/input[@name='Name']"))
        )
        driver.find_element(By.XPATH, "//div/input[@name='Name']").send_keys(opportunity_name)
        driver.find_element(By.XPATH, "//input[@aria-haspopup='listbox']").send_keys(account)
        accounts_list = driver.find_elements(By.XPATH, "//ul/li//lightning-base-combobox-formatted-text")
        for acc in accounts_list:
            if acc.text == account:
                acc.click()
                break

        driver.find_element(By.XPATH, "//div/input[@name='CloseDate']").send_keys(closedate) #"31/12/2025"
        # Locate the element
        element = driver.find_element("xpath", "//div/button[@aria-label='Stage']")
        # Scroll to the element
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        driver.find_element(By.XPATH, "//div/button[@aria-label='Stage']").click()

        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, f"//lightning-base-combobox-item//span[text()='{stage}']"))
        ).click()
        driver.find_element(By.XPATH, "//div[@class='footer-full-width']//button[text()='Save']").click()
        time.sleep(1)  # load the created opportunity    #removed fails#

        # Checking the opportunity details
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id='Opportunity']/one-app-nav-bar-item-dropdown"))
        )
        oppdropdown = driver.find_element(By.XPATH,
                                          "//one-app-nav-bar-item-root[@data-id='Opportunity']/one-app-nav-bar-item-dropdown")
        action.move_to_element(oppdropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, f"//span[text()='{opportunity_name}']"))
        )
        new_opp = driver.find_element(By.XPATH, f"//span[text()='{opportunity_name}']")
        action.move_to_element(new_opp).click().perform()
        print('Opportunity name: ', driver.find_element(By.XPATH,
                                                        "//records-record-layout-item[@field-label='Opportunity Name']//lightning-formatted-text").text)
        acc_name = driver.find_element(By.XPATH,
                                       "//records-record-layout-item[@field-label='Account Name']//records-hoverable-link//slot//slot")
        print('Oppor Attached Account: ', acc_name.text)

        # Contact attachment#
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id ='Contact']/one-app-nav-bar-item-dropdown"))
        )

        contact_dropdown = driver.find_element(By.XPATH,
                                               "//one-app-nav-bar-item-root[@data-id ='Contact']/one-app-nav-bar-item-dropdown")
        action.move_to_element(contact_dropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='New Contact']"))
        )
        new_contact = driver.find_element(By.XPATH, "//span[text()='New Contact']")

        action.move_to_element(new_contact).click().perform()

        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//button[@name='salutation']")
        ))
        driver.find_element(By.XPATH, "//button[@name='salutation']").click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.XPATH, "//div/lightning-base-combobox-item/span/span[text()='Mr.']")
        ))
        driver.find_element(By.XPATH, "//div/lightning-base-combobox-item/span/span[text()='Mr.']").click()
        driver.find_element(By.XPATH, "//input[@name='lastName']").send_keys(contact_name)
        driver.find_element(By.XPATH, "//input[@placeholder='Search Accounts...']").send_keys(account)
        account_lis = driver.find_elements(By.XPATH, "//ul[@role='group']/li")
        for acc in account_lis:
            if acc.text == account:
                acc.click()
                break

        driver.find_element(By.XPATH,
                            "//runtime_platform_actions-action-renderer//button[text()='Save']").click()

        time.sleep(1)  # load Contact

        # Contact Check#
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//one-app-nav-bar-item-root[@data-id ='Contact']/one-app-nav-bar-item-dropdown"))
        )

        contact_dropdown = driver.find_element(By.XPATH,
                                               "//one-app-nav-bar-item-root[@data-id ='Contact']/one-app-nav-bar-item-dropdown")
        action.move_to_element(contact_dropdown).click().perform()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[text()='{contact_name}']"))
        )
        new_contact = driver.find_element(By.XPATH, f"//span[text()='{contact_name}']")

        action.move_to_element(new_contact).click().perform()

        acc_name = driver.find_element(By.XPATH,
                                       "//records-record-layout-item[@field-label='Account Name']//records-hoverable-link//slot//slot")
        print('Created Contact: ',
              driver.find_element(By.XPATH, "//slot[@name='outputField']/lightning-formatted-name").text)
        print('Contact Attached Account: ', acc_name.text)

        time.sleep(3)
        driver.close()


c1 = Test_usecase("gokul.gangadhara-6rcu@force.com", "Tiger@1234")
c1.new_acc("yty","Virtual","31/12/2025","Qualify","Ravidran")
# account,opportunity_name,closedate,stage,contact_name
# stage =Qualify
# creating an account BW
#creating an oppo and passing BW
#Creating an contact and passwing BW