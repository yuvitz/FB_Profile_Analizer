import json
import os
import sys
import urllib.request
from datetime import date

import yaml
import argparse
import time

import data_contracts.fb_user as fb_user
from . import settings, utils, modes, fb_users_writer
# from . import utils
# from . import modes
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# returns a dictionary containing the user's posts
def scrape_posts(elements_path, scan_type):

    try:
        my_posts = utils.my_scroll(settings.number_of_posts, settings.driver, settings.selectors, settings.scroll_time, elements_path[0], scan_type)

    except Exception:
        print(
            "Exception (scrape_data)",
            "Status =",
            # str(save_status),
            sys.exc_info()[0],
        )
        return []
    return my_posts


# returns total number of friends, and number of mutual friends
def parse_friends_data(friends_data_str):
    friends_data_str = friends_data_str.replace(',', '')
    # print(friends_data)
    friends_data_str = friends_data_str.replace('(', ' ')
    # print(friends_data)
    # friends_data = friends_data.replace(')', ' ')
    friends_data = [int(s) for s in friends_data_str.split() if s.isdigit()]
    # print(friends_data)
    return friends_data


# returns user's friends total friends count and mutual friends count
# def scrape_friends_count(url, scan_list, section, elements_path):
def scrape_friends_count():
    # try:
    settings.driver.execute_script(settings.selectors.get("scroll_script"))

    element_text = WebDriverWait(settings.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, settings.selectors.get("friends_data")))
        ).text

    # friends_element = settings.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div[2]/span/span')
    return parse_friends_data(element_text)


def month_switch(argument):
    switcher = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12
    }
    return switcher.get(argument, "Invalid month")


def calculate_age(profile_date, today):
    today_day, today_month, today_year = today.split('/')
    today_day = int(today_day)
    today_month = int(today_month)
    today_year = int(today_year)
    # print('day: ', today_day, '\nmonth: ', today_month, '\nyear: ', today_year)
    profile_date = profile_date.split(' ')
    if len(profile_date) == 3:
        possible_day, possible_month, profile_year = profile_date
    elif len(profile_date) == 2:
        possible_day, possible_month = profile_date
        profile_year = today_year
    else:
        return 0

    possible_month = possible_month.replace(',', '')
    possible_month = possible_month.replace(' ', '')

    if possible_month.isdigit():
        temp = possible_month
        possible_month = possible_day
        possible_day = temp

    profile_month = month_switch(possible_month)

    profile_day = int(possible_day)
    # profile_month = int(possible_month)
    profile_year = int(profile_year)
    # print('day: ', profile_day, '\nmonth: ', profile_month, '\nyear: ', profile_year)
    age = today_year-profile_year + (today_month-profile_month)/12 + (today_day-profile_day)/365
    return age


def scrape_account_age(url):
    settings.driver.get(url+'/photos_albums')

    WebDriverWait(settings.driver, 10).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'Profile'))).click()

    utils.friends_scroll(settings.driver, settings.selectors, settings.scroll_time)

    profile_pictures = WebDriverWait(settings.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, settings.selectors.get("profile_pics"))))

    last_pic = profile_pictures[len(profile_pictures)-1]
    last_pic.click()

    date_element = WebDriverWait(settings.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, settings.selectors.get("date_element"))))

    profile_date = date_element.get_attribute("aria-label")
    if profile_date is None:
        profile_date = date_element.text

    print('profile date: ', profile_date)
    today = date.today().strftime("%d/%m/%Y")
    # print('today date: ', today)
    age = calculate_age(profile_date, today)

    return age


def calculate_duration(friendship_year, friendship_month, today):
    today_day, today_month, today_year = today.split('/')
    today_day = int(today_day)
    today_month = int(today_month)
    today_year = int(today_year)

    friendship_month = month_switch(friendship_month)
    friendship_month = int(friendship_month)

    friendship_year = int(friendship_year)
    if friendship_year == 0:
        friendship_year = today_year

    duration = today_year-friendship_year + (today_month-friendship_month)/12 + today_day/365
    return duration


def find_duration():

    # More button click
    WebDriverWait(settings.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                            settings.selectors.get("more_button")))).click()
    # Friendship click
    WebDriverWait(settings.driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                            settings.selectors.get("see_friendship")))).click()
    settings.driver.implicitly_wait(2)
    time.sleep(2)
    common_things = WebDriverWait(settings.driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                            settings.selectors.get("common_things"))))

    for thing in common_things:
        if "Your friend since" in thing.text:
            duration = thing.text
    duration = duration.split(" ")
    duration = duration[3:]
    month = duration[0]
    year = 0
    if len(duration) > 1:
        year = int(duration[len(duration)-1])

    today = date.today().strftime("%d/%m/%Y")
    duration = calculate_duration(year, month, today)

    return duration



def scrape_data(url, elements_path, scan_type):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    time.sleep(0.5)
    try:
        name = WebDriverWait(settings.driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, settings.selectors.get("name")))).text
        print("name:", name)
    except Exception:
        print("find name failed")

    if scan_type == modes.Scan_type.full_scan:
        try:
            friendship_duration = find_duration()
            print("friendship_duration:", friendship_duration)
        except Exception:
            print("find friendship duration failed")

            friendship_duration = 0
        # time.sleep(0.5)
        try:
            age = scrape_account_age(url)
            print("age:", age)
        except Exception:
            print("find age failed")
            age = 0
        settings.driver.get(url)
        settings.driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
        time.sleep(1.5)

        try:
            friends_data = scrape_friends_count()
            print("friends data:", friends_data)
            total_friends = friends_data[0]
            if len(friends_data) > 1:
                mutual_friends = friends_data[1]
            else:
                mutual_friends = 0
        except Exception:
            print("find friends data failed")
            total_friends = 0
            mutual_friends = 0
    else:
        settings.driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
        time.sleep(1.5)
        age = 0
        friendship_duration = 0
        total_friends = 0
        mutual_friends = 0

    posts = scrape_posts(elements_path, scan_type)
    # posts = []
    profile = fb_user.FBUser(name, url, age, friendship_duration, total_friends, mutual_friends, posts)
    return profile


# return posts, friends, about

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------

def create_original_link(url):
    if url.find(".php") != -1:
        original_link = (
            settings.facebook_https_prefix + settings.facebook_link_body + ((url.split("="))[1])
        )

        if original_link.find("&") != -1:
            original_link = original_link.split("&")[0]

    elif url.find("fnr_t") != -1:
        original_link = (
            settings.facebook_https_prefix
            + settings.facebook_link_body
            + ((url.split("/"))[-1].split("?")[0])
        )
    elif url.find("_tab") != -1:
        original_link = (
            settings.facebook_https_prefix
            + settings.facebook_link_body
            + (url.split("?")[0]).split("/")[-1]
        )
    else:
        original_link = url

    return original_link


def scrap_all_friends(scan_type):
    result = []
    print("scrape all")
    WebDriverWait(settings.driver, 15).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, settings.selectors.get("profile_selector")))
    ).click()

    time.sleep(0.5)
    url = settings.driver.current_url
    settings.driver.get(url+"/friends")
    time.sleep(0.5)

    # utils.friends_scroll(settings.driver, settings.selectors, settings.scroll_time)
    friends_block = settings.driver.find_element_by_css_selector(settings.selectors.get("friends_block"))
    friends = friends_block.find_elements_by_css_selector(settings.selectors.get("friends"))

    links = [friend.get_attribute('href') for friend in friends]

    print(links, "\n", len(links))
    list = []
    # Helper: time counter
    start = time.time()
    end = time.time()
    # DEBUG: control num of iterations
    count = 0
    for link in links:
        count += 1
        try:
            this_start = time.time()
            settings.driver.get(link)
            profile = scrap_profile(scan_type)
            list.append(profile)
            fb_users_writer.write_fb_friends_to_file(profile, count)
            settings.driver.implicitly_wait(1)
            time.sleep(1)
            this_end = time.time()
            print("this profile is the", count, "profile being scraped")
            print("this profile took:", this_end-this_start)
            end = time.time()
            print("time passed so far (hours):", str(int((end - start)/3600)) +
                  ":"+str(int((end - start)/60) % 60)+":"+str(int((end - start) % 60)))

        except WebDriverException:
            break
        except Exception:
            break

        # DEBUG: control num of iterations
        if count >= 5:
            break

    print("all profiles took (hours):", str(int((end - start)/3600)) +
                  ":" + str(int((end - start)/60) % 60)+":"+str(int((end - start) % 60)))

    print("all profiles average:", (end - start)/count)

    return list


def scrap_profile(scan_type):

    url = settings.driver.current_url
    user_id = create_original_link(url)

    print("\nScraping:", user_id)


    print("----------------------------------------")
    print("Scraping {}..".format("Posts"))

    elements_path = settings.params["Posts"]["elements_path"]
    profile = scrape_data(user_id, elements_path, scan_type)

    print("{} Done!".format("item"))

    print("Finished Scraping Profile " + str(user_id) + ".")
    # os.chdir("../..")

    return profile


def get_item_id(url):
    """
    Gets item id from url
    :param url: facebook url string
    :return: item id or empty string in case of failure
    """
    ret = ""
    try:
        link = create_original_link(url)
        ret = link.split("/")[-1]
        if ret.strip() == "":
            ret = link.split("/")[-2]
    except Exception as e:
        print("Failed to get id: " + format(e))
    return ret

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def login(email, password):
    """ Logging into our own profile """
    try:
        options = Options()
        #  Code to disable notifications pop up of Chrome Browser
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        options.add_argument('--disable-browser-side-navigation')
        # options.add_argument("--headless")

        try:

            settings.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options
            )
            # settings.driver.set_headless(headless=True)
        except Exception:
            print("Error loading chrome webdriver " + sys.exc_info()[0])
            exit(1)

        fb_path = settings.facebook_https_prefix + settings.facebook_link_body
        settings.driver.get(fb_path)
        settings.driver.maximize_window()

        # filling the form
        settings.driver.find_element_by_name("email").send_keys(email)
        settings.driver.find_element_by_name("pass").send_keys(password)

        try:
            # clicking on login button
            settings.driver.find_element_by_id("loginbutton").click()
        except NoSuchElementException:
            # Facebook new design
            settings.driver.find_element_by_name("login").click()

        # if your account uses multi factor authentication
        mfa_code_input = utils.safe_find_element_by_id(settings.driver, "approvals_code")

        if mfa_code_input is None:
            return

        mfa_code_input.send_keys(input("Enter MFA code: "))
        settings.driver.find_element_by_id("checkpointSubmitButton").click()

        # there are so many screens asking you to verify things. Just skip them all
        while (
            utils.safe_find_element_by_id(settings.driver, "checkpointSubmitButton") is not None
        ):
            dont_save_browser_radio = utils.safe_find_element_by_id(settings.driver, "u_0_3")
            if dont_save_browser_radio is not None:
                dont_save_browser_radio.click()

            settings.driver.find_element_by_id("checkpointSubmitButton").click()

    except Exception:
        print("There's some error in log in.")
        print(sys.exc_info()[0])
        exit(1)


# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------


def scraper(email, password, user_url, mod, scrape_mod, scan_type, **kwargs):
    # print(scrape_mod)

    working_dir = os.path.dirname(os.path.abspath(__file__))
    if mod == modes.Mode.Dev:

        with open(working_dir + "\credentials.yaml", "r") as ymlfile:
            cfg = yaml.safe_load(stream=ymlfile)

        if ("password" not in cfg) or ("email" not in cfg):
            print("Your email or password is missing. Kindly write them in credentials.txt")
            exit(1)
        email = cfg["email"]
        password = cfg["password"]

    login(email, password)
    if scrape_mod == modes.Scrape_mode.Scrape_specific:
        settings.driver.get(user_url)
        result = [scrap_profile(scan_type)]
    else:
        result = scrap_all_friends(scan_type)
    settings.driver.close()
    return result

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------


# if __name__ == "__main__":
def main(email, password, user_url, mod, scrape_mod, scan_mode):

    settings.ap = argparse.ArgumentParser()

    settings.ap.add_argument(
        "-st",
        "--scroll_time",
        help="How much time should I take to scroll?",
        default=4
    )
    settings.ap.add_argument(
        "-nop",
        "--number_of_posts",
        help="How many posts should i take?",
        default=15
    )

    settings.args = vars(settings.ap.parse_args())
    print(settings.args)

    settings.scroll_time = int(settings.args["scroll_time"])
    settings.number_of_posts = int(settings.args["number_of_posts"])

    settings.driver = None

    working_dir = os.path.dirname(os.path.abspath(__file__))
    with open(working_dir + "\selectors.json") as selectors, open(working_dir + "\params.json") as params:
        settings.selectors = json.load(selectors)
        settings.params = json.load(params)

    settings.facebook_https_prefix = settings.selectors.get("facebook_https_prefix")
    settings.facebook_link_body = settings.selectors.get("facebook_link_body")

    # get things rolling
    scraper_result = scraper(email, password, user_url, mod, scrape_mod, scan_mode)
    return scraper_result
