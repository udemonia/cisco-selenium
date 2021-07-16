#!/usr/bin/env python3

# * Cisco Call Manager
# ? python Version 3.7
# ? Google Chrome is up to date - Version 80.0.3987.122 (Official Build) (64-bit)
# ? selenium Version 2.37.2

#! for the chrome driver version error - look up chrome version and ensure it's aligned w/ web drive

import pandas as pd
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from getpass import getpass
from time import sleep
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import sys

# ? Enable if you're getting the SSL error - also use the second browser = driver(location, options)
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

# ? read in the CSV
pdc = pd.read_csv('/Users/blambert/Downloads/pdclines.csv', na_filter=False)


# -------------------------------
#        Data Validation
# -------------------------------

# ? check to see if the DID == 7 digits
for index, row in pdc.iterrows():
    if len(str(row['DID'])) != 7:
        print(
            "*DID* MUST BE 7 DIGITS, DO NOT INCLUDE HYPENS '-', CORRECT THE DID AND RUN AGAIN")
        exit()
# ? check to see if Broadcast length in 0,10
for index, row in pdc.iterrows():
    if len(str(row['Broadcast'])) not in (0, 10):
        print(
            f"*Broadcast* MUST BE EMPTY OR 10 DIGITS LONG, DO NOT INCLUDE HYPENS '-', CORRECT THE BROADCAST AND RUN AGAIN\n{index} doesn't = 0,10")
        exit()


# -------------------------------
#     Get Login Credentials
# -------------------------------

# ? handle passwords
user = getpass("Enter your username\n")
password = getpass("Enter your password\n")

# -------------------------------
#        Set Constants
# -------------------------------

# ? search variables to copy previous set ups
search_did = 8298187
search_ext = 1387
search_trigger = 2387
uccxapp = pdc.at[0, 'App Name']
uccxprefix = str(pdc.at[0, 'Extension'])

# --------------------------------------------------
#      Print Dataframe for Last Validation
# --------------------------------------------------
print(pdc)

# -------------------------------
#      Ask to Continue
# -------------------------------


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


answer = query_yes_no("would you like to continue?")

# -------------------------------
#      Validate Extensions
# -------------------------------

# ? exit the program on no
if answer == False:
    exit()

# create an empty array and append index 0 & index 1 for each extension in df
extension_first_two_index_list = []
for index, row in pdc.iterrows():
    # ? to test results
    # print(str(row["Extension"])[0:2])
    extension_first_two_index_list.append(str(row["Extension"])[0:2])


def all_same(items):
    '''
        #*function to return true if the first two index poistions in the df['extensions'] are the same
    '''
    return all(x == items[0] for x in items)


# pass the array into function
run_func = all_same(extension_first_two_index_list)

# ask if the user wants to quite as the extensions are not the same
if run_func == False:
    second_answer = query_yes_no(
        "Extensions indexes are not the same\nwould you like to continue?")
    if second_answer == False:
        exit()

# -------------------------------
#      Chrome Driver
# -------------------------------

# * WEB DRIVER
# # define Browser as webdriver
browser = webdriver.Chrome(
    '/Users/blambert/Documents/Scripts/chromedriver', chrome_options=options)
# browser = webdriver.Chrome(
#     'chromedriver', chrome_options=options)


# ------------------------------------------
#     Initial get() and Authentication
# -----------------------------------------

# ? open url
browser.get('https://s-md-pd-cucm-pub.healthgrades.com/ccmadmin/index.jsp')
# browser.maximize_window()

# ? authenticate into Call Manager
browser.find_element_by_xpath(
    "/html/body/form[@name='logonForm']/div[@class='content']/table[1]/tbody/tr[1]/td[2]/table//input[@name='j_username']").send_keys(user)
browser.find_element_by_xpath(
    "/html/body/form[@name='logonForm']/div[@class='content']/table[1]/tbody/tr[1]/td[2]/table//input[@name='j_password']").send_keys(password)
browser.find_element_by_xpath(
    "/html/body/form[@name='logonForm']/div[@class='content']/table[1]/tbody/tr[1]/td[2]/table//button[@type='submit']").click()


# --------------------------------------------------------
#      Functions to Handle Cisco CM and UCCX Setups
# --------------------------------------------------------

# ?  uncomment out the Break when:
# ?  the code failes after completing the functions (for instance, if code fails on directory number, uncomment out the translation pattern break)

def translationpattern(pdc):
    for index, row in pdc.iterrows():
        # continue
        # break
        browser.find_element_by_xpath(
            "/html//a[@id='Call RoutingButton']").click()
        browser.implicitly_wait(5)
        browser.find_element_by_css_selector(
            "#callrouting li:nth-of-type(11) [tabindex]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='searchString0']").clear()
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='searchString0']").send_keys(search_did)
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='findButton']").click()
        browser.find_element_by_xpath(
            "//div[@id='contentautoscroll']/form[@action='https://s-md-pd-cucm-pub.healthgrades.com/ccmadmin/translationFindList.do?recCnt=1&colCnt=5']/table[@class='cuesTableBg']//tr[@class='cuesTableRowEven']/td[3]/a[@href='translationEdit.do?key=6e700eea-ff04-4ded-9834-5eec66c23e18']").click()
        browser.find_element_by_css_selector(
            "[keephref='javascript\:onCopy\(\)']").click()
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(row["DID"])
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").send_keys(row['Line Name'])
        browser.find_element_by_xpath(
            "/html//input[@id='CALLEDPARTYTRANSFORMATIONMASK']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='CALLEDPARTYTRANSFORMATIONMASK']").send_keys(row['Trigger'])
        # * save the copy
        browser.find_element_by_xpath(
            "//div[@id='contentautoscroll']/form[@action='/ccmadmin/translationEdit.do']//input[@alt='Save']").click()
        time.sleep(1)
        # ? print the result of the add to terminal
        print(browser.find_element_by_xpath(
            "/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/form[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[2]").text + " Translation Pattern " + str(row["DID"]))


def directorynumber(pdc):
    for index, row in pdc.iterrows():
        # continue
        # break
        browser.find_element_by_xpath(
            "/html//a[@id='Call RoutingButton']").click()
        time.sleep(2)
        browser.find_element_by_css_selector(
            "#callrouting li:nth-of-type(15) [tabindex]").click()
        time.sleep(1)
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='searchString0']").clear()
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='searchString0']").send_keys(search_ext)
        browser.find_element_by_xpath(
            "//table[@id='cuesTableFilter']/tbody/tr[1]//input[@name='findButton']").click()
        browser.find_element_by_css_selector(
            "[headers='Pattern\/Directory Number'] .cuesTextLink").click()
        browser.find_element_by_css_selector(
            "[keephref='javascript\:onCopy\(\)']").click()
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").send_keys(row["Line Name"])
        browser.find_element_by_xpath(
            "/html//input[@id='ALERTINGNAME']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='ALERTINGNAME']").send_keys(row["Line Name"])
        browser.find_element_by_xpath(
            "/html//input[@id='ALERTINGNAMEASCII']").clear()
        browser.find_element_by_xpath("/html//input[@id='ALERTINGNAMEASCII']").send_keys(
            row["Line Name"] + " " + str(row["Extension"]))
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").click()
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(row["Extension"])
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_xpath(
            "/html//input[@id='DNORPATTERN']").send_keys(Keys.BACK_SPACE)
        # *  save the copy
        browser.find_element_by_xpath(
            "//form[@id='directoryNumberForm']//input[@alt='Save']").click()
        time.sleep(2)
        # ? print save results out to terminal
        print(browser.find_element_by_xpath(
            "/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/form[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[2]").text + " Directory Number " + str(row["Extension"]))


def routehunt(pdc):
    for index, row in pdc.iterrows():
        # continue
        browser.find_element_by_xpath(
            "/html//a[@id='Call RoutingButton']").click()
        time.sleep(1)
        browser.find_element_by_css_selector(
            "body.layout:nth-child(2) table.menubar:nth-child(3) td.menubar-title ul.udm:nth-child(3) li:nth-child(2) ul:nth-child(2) li:nth-child(4) > a.nohref:nth-child(1)").click()
        time.sleep(1)
        browser.find_element_by_css_selector(
            "body.layout:nth-child(2) table.menubar:nth-child(3) td.menubar-title ul.udm:nth-child(3) ul:nth-child(2) li:nth-child(4) ul:nth-child(2) li:nth-child(4) > a:nth-child(1)").click()
        time.sleep(1)
        browser.find_element_by_xpath("//input[@id='searchString0']").clear()
        browser.find_element_by_xpath(
            "//input[@id='searchString0']").send_keys("*" + str(search_ext) + str(8))
        browser.find_element_by_css_selector("[name='findButton']").click()
        browser.find_element_by_css_selector(
            "[headers='Pattern'] .cuesTextLink").click()
        browser.find_element_by_css_selector(
            "[keephref='javascript\:onCopy\(\)']").click()
        browser.find_element_by_css_selector("[name='dnorpattern']").click()
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(Keys.BACK_SPACE)
        browser.find_element_by_css_selector(
            "[name='dnorpattern']").send_keys(row["Extension"])
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").clear()
        browser.find_element_by_xpath(
            "/html//input[@id='DESCRIPTION']").send_keys(row["Line Name"])
        browser.find_element_by_css_selector(
            "[name='callingpartytransformationmask']").click()
        browser.find_element_by_css_selector(
            "[name='callingpartytransformationmask']").clear()
        time.sleep(2)

        #! COMMENT OUT IF YOU DONT HAVE BROADCAST NUMBER

        browser.find_element_by_xpath(
            "/html//input[@id='CALLINGPARTYTRANSFORMATIONMASK']").send_keys(row["Broadcast"])

        #! OMMENT OUT IF Y9OU DONT HAVE A BROADCAST NUMBER

        # * save the copy
        browser.find_element_by_xpath(
            "//form[@id='routePattern2Form']//input[@alt='Save']").click()
        browser.implicitly_wait(5)
        time.sleep(1)
        browser.switch_to_alert().accept()
        time.sleep(1)
        browser.switch_to_alert().accept()
        print(browser.find_element_by_xpath(
            "/html[1]/body[1]/table[1]/tbody[1]/tr[1]/td[1]/div[1]/form[1]/fieldset[1]/table[1]/tbody[1]/tr[1]/td[2]").text + " Route Hunt " + "*" + str(row["Extension"]))
        time.sleep(4)


def uccxapplication(pdc):
    browser.get("https://s-md-pd-uccx-pub.healthgrades.com/appadmin/main")
    browser.implicitly_wait(5)

    browser.find_element_by_xpath(
        "//body/form[@name='frmLogin']/table[1]/tbody/tr[1]/td[2]/table//input[@name='j_username']").send_keys(user)
    browser.find_element_by_css_selector(
        "[summary] tr:nth-of-type(4) [size]").send_keys(password)
    time.sleep(2)
    browser.find_element_by_xpath(
        "//body/form[@name='frmLogin']/table[1]/tbody/tr[1]/td[2]/table//button[@type='submit']").click()
    browser.find_element_by_xpath(
        "/html//ul[@id='udm']//a[@title='Applications']").click()
    browser.find_element_by_xpath(
        "/html//ul[@id='udm']/li[2]/ul[@class='udmsubmenu']/li[1]/nobr/a").click()
    # * new application set up
    browser.find_element_by_xpath(
        "/html//div[@id='cuesToolbar']/table[@class='cuesToolbarContainer']/tbody/tr/td[1]/table//td[@class='cuesToolbarCell']//a[@title='Add New']").click()
    time.sleep(2)
    browser.find_element_by_xpath(
        "/html//div[@id='cuesToolbar']/table[@class='cuesToolbarContainer']/tbody/tr/td[1]/table//td[@class='cuesToolbarCell']//a[@title='Next']").click()
    browser.find_element_by_xpath(
        "/html//form[@id='ScriptApp']/table[@class='content']/tbody/tr/td[2]//table[@class='content-form']//input[@name='appname']").send_keys(uccxapp)
    browser.find_element_by_xpath(
        "/html//form[@id='ScriptApp']/table[@class='content']/tbody/tr/td[2]//table[@class='content-form']//input[@name='session']").send_keys("150")
    browser.find_element_by_xpath(
        "/html//form[@id='ScriptApp']/table[@class='content']/tbody/tr/td[2]//table[@class='content-form']//input[@name='desc']").click()
    time.sleep(2)
    # ? find the application from the drop down menu
    element = browser.find_element_by_xpath(
        "/html//form[@id='ScriptApp']/table[@class='content']/tbody/tr/td[2]//table[@class='content-form']//select[@name='script']")
    drp = Select(element)
    drp.select_by_value("SCRIPT[HealthGradesBaseScript.aef]")

    # ? now we need to fill in the application
    browser.find_element_by_css_selector(
        ".Label > input[name='cfgVarssVMPrefix_cb']").click()
    browser.find_element_by_css_selector(
        "input[name='cfgVarssVMPrefix']").send_keys(Keys.ARROW_LEFT)
    browser.find_element_by_css_selector(
        "input[name='cfgVarssVMPrefix']").send_keys(uccxprefix)
    browser.find_element_by_css_selector(
        "input[name='cfgVarssVMPrefix']").send_keys(Keys.BACK_SPACE)
    browser.find_element_by_css_selector(
        "input[name='cfgVarssVMPrefix']").send_keys(Keys.BACK_SPACE)
    # *save the application
    browser.find_element_by_xpath(
        "/html//form[@id='ScriptApp']/table[2]//input[@name='btnUpdate']").click()
    time.sleep(8)


def uccx_trigger_test():
    '''
    this lives inside of uccx trigger - if we want to test an existing app or add triggers to an existing app
    we would not call the uccx application creator and instead call this.
    Have to pass the script name in the last browser.find
    #todo add the xpath as a paramater/argument in the function
    '''
    #! TEST CODE for uccx trigger adds
    browser.get("https://s-md-pd-uccx-pub.healthgrades.com/appadmin/main")
    browser.implicitly_wait(5)
    browser.find_element_by_xpath(
        "//body/form[@name='frmLogin']/table[1]/tbody/tr[1]/td[2]/table//input[@name='j_username']").send_keys(user)
    browser.find_element_by_css_selector(
        "[summary] tr:nth-of-type(4) [size]").send_keys(password)
    browser.find_element_by_xpath(
        "//body/form[@name='frmLogin']/table[1]/tbody/tr[1]/td[2]/table//button[@type='submit']").click()
    browser.find_element_by_xpath(
        "/html//ul[@id='udm']//a[@title='Applications']").click()
    browser.find_element_by_xpath(
        "/html//ul[@id='udm']/li[2]/ul[@class='udmsubmenu']/li[1]/nobr/a").click()
    #! - - - - - - - - - -  pass the xpath of the application here - - - - - - - -

    browser.find_element_by_xpath(
        "//table[@id='t1.td']/tbody/tr[516]//a[@href='/appadmin/App?request_type=configure&appname=PDCP5&apptype=Cisco+Script+Application']").click()
    #! TEST CODE for uccx trigger adds


def uccxtriggers(pdc):
    # uccx_trigger_test()
    for index, row in pdc.iterrows():
        time.sleep(4)
        select = browser.find_element_by_link_text("Add new trigger")
        select.click()

        # ? need to switch to window
        window_before = browser.window_handles[0]
        handles = browser.window_handles
        for handle in handles:
            browser.switch_to.window(handle)
            # !print(browser.title)
        browser.find_element_by_css_selector(
            "[border] td [type='button']:nth-of-type(1)").click()
        # * select items from drop down menu's on UCCX Application
        time.sleep(3)
        select1 = browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/fieldset[2]/table[@class='content-form']//select[@name='locselect']")
        drp1 = Select(select1)
        drp1.select_by_value("en_US")
        browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/fieldset[2]/table[@class='content-form']//input[@name='deviceName']").send_keys(row["Line Name"])
        browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/fieldset[2]/table[@class='content-form']//input[@name='description']").send_keys(row["Line Name"])
        # ? language drop down
        select2 = browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/fieldset[2]/table[@class='content-form']//select[@name='ccgselect']")
        drp2 = Select(select2)
        drp2.select_by_value("2")
        browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/fieldset[@class='status-fieldset']/table[@class='content-form']//input[@name='trigname']").send_keys(row["Trigger"])
        browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/table[1]//input[@name='sm']").click()
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").click()
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(Keys.ARROW_LEFT)
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(row["Line Name"])
        browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//input[@name='alertingnameascii']").send_keys(Keys.SPACE)
        time.sleep(3)
        # ? device pool drop down
        select3 = browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//select[@name='devicePool']")
        drp3 = Select(select3)
        drp3.select_by_value("{C9E7F582-5CEF-DB52-55E3-A8FF75C28A68}")

        # ? location drop down
        select4 = browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[1]/table[@class='content-form']//select[@name='location']")
        drp4 = Select(select4)
        drp4.select_by_value("{D6983F75-00FA-5A4B-F7BF-8BB4FDD15E5F}")

        # ? Partition drop down
        select5 = browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[2]/table[@class='content-form']//select[@name='partition']")
        drp5 = Select(select5)
        drp5.select_by_value("{410C04AE-76F7-91CC-9053-532DE2F974D0}")

        # ? voice mail drop down
        select6 = browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[2]/table[@class='content-form']//select[@name='vmProfile']")
        drp6 = Select(select6)
        drp6.select_by_value("{C9357B15-94AA-CE65-AE37-D69A4FAF2E6C}")

        # ? calling party drop down
        select7 = browser.find_element_by_xpath(
            "/html//div[@id='showBlock']/div/fieldset[2]/table[@class='content-form']//select[@name='css']")
        drp7 = Select(select7)
        drp7.select_by_value("{a65255ac-ecc8-2356-e2ce-5637a8251296}")
        time.sleep(5)

        # # * save the trigger
        browser.find_element_by_xpath(
            "/html//form[@id='jtapiTriggerInfo']/table[1]//input[@name='btnUpdate']").click()

        # ? switch back to main window
        time.sleep(5)
        browser.switch_to_window(window_before)
        time.sleep(8)


# ------------------------------------------
#      JIRA Notes and AutoIT Scripting
# ------------------------------------------

# ? creates the jira notes based upon the csv in the formating to create a table within jira notes

def jira_notes():
    print("|Line Name|Broadcast|DID|Extension|Trigger|AppName|")
    for index, row in pdc.iterrows():
        if len(str(row["Broadcast"])) < 1:
            row["Broadcast"] = 'N/A'
        print("|" + row["Line Name"] + "|" + str(row["Broadcast"]) + "|" + '608' +
              str(row["DID"]) + "|" + str(row["Extension"]) + "|" + str(row["Trigger"]) + "|" + str(row["App Name"]) + "|")

# ? creates the auto it scripting that controls the agents computers/popups by number


def print_autoIT(pdc):
    for index, row in pdc.iterrows():
        trig = row["Trigger"]
        line = row["Line Name"]
        db = row["Data Base"]
        greet = row["Greetings"]
        mind = row["Reminder"]
        fac = row["Facility"]
        source = row["Source"]
        client_name = row["Client Name"]
        closing = "*" + str(row["Extension"])
        color = row['Color']
        flag = row['Flag']
        red_alert = ["PDC2", "PDCM2", "PDCX2"]
        if row['Source'] in red_alert:
            color = '0xFF0000'
        if row['Source'] in red_alert:
            flag = "48"
        else:
            flag = "0"
        print(f';{db}\n\tCase $sSplit="{trig}"\n\t\t$sClient="{db}"\n\t\t$sLine="{source}"\n\t\t$sFlag="{flag}"\n\t\t$sCName="{client_name}"\n\t\t$sGreeting="{greet}"\n\t\t$sLink=""\n\t\t$sReminder="{mind}"\n\t\t$sClose="Thank you for calling." & @CRLF & @CRLF & "{closing}"\n\t\t$sBoxColor="{color}"\n\t\t$sFacility="{fac}"')


# -------------------------------
#      Call the Functions
# -------------------------------

# ? Call the functions - Call Manager
translationpattern(pdc)
directorynumber(pdc)
routehunt(pdc)

# ? call the functions - UCCX
#!run the uccx app + trigger functions only if first two digits of 'extension' are the same
if run_func == True:
    uccxapplication(pdc)
else:
    print("The 'extension' prefixes are not the same for each line\nCan't create UCCX application and triggers\nPlease create them manually")

#! if you run this, aks for help first----
# ? uccx test triggers will add triggers to a existing application - not normally needed for new set ups
# if run_func == True:
#     uccx_trigger_test(pdc)

# ? Trigger adds, has to be run with the uccxapplication function
if run_func == True:
    uccxtriggers(pdc)

#! call the notes and autoIT functions
# * print out the JIRA notes and the AutoIT scripting
jira_notes()
print_autoIT(pdc)

# default Greetings for PDC - - -
# #? Hi, my name is _________.  All calls may be recorded for quality purposes.  How can I help you today?

browser.quit()

# todo add logging
# f = f = open('Results.txt', 'w')

# csv_record = account_name + "," + profile_name + \
#                 "," + user_name + "," + email + "\n"
# f.write(csv_record)
