import json
import os
import sys
import urllib.request
from datetime import date

from modes import Scrape_mode, Mode
import yaml
# import utils
import argparse
import time

import fb_user
from . import settings
from . import utils
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


# def get_facebook_images_url(img_links):
#     urls = []

#     for link in img_links:
#         if link != "None":
#             valid_url_found = False
#             driver.get(link)

#             try:
#                 while not valid_url_found:
#                     WebDriverWait(driver, 30).until(
#                         EC.presence_of_element_located(
#                             (By.CLASS_NAME, selectors.get("spotlight"))
#                         )
#                     )
#                     element = driver.find_element_by_class_name(
#                         selectors.get("spotlight")
#                     )
#                     img_url = element.get_attribute("src")

#                     if img_url.find(".gif") == -1:
#                         valid_url_found = True
#                         urls.append(img_url)
#             except Exception:
#                 urls.append("None")
#         else:
#             urls.append("None")

#     return urls


# -------------------------------------------------------------
# -------------------------------------------------------------

# takes a url and downloads image from that url
# def image_downloader(img_links, folder_name):
#     """
#     Download images from a list of image urls.
#     :param img_links:
#     :param folder_name:
#     :return: list of image names downloaded
#     """
#     img_names = []

#     try:
#         parent = os.getcwd()
#         try:
#             folder = os.path.join(os.getcwd(), folder_name)
#             utils.create_folder(folder)
#             os.chdir(folder)
#         except Exception:
#             print("Error in changing directory.")

#         for link in img_links:
#             img_name = "None"

#             if link != "None":
#                 img_name = (link.split(".jpg")[0]).split("/")[-1] + ".jpg"

#                 # this is the image id when there's no profile pic
#                 if img_name == selectors.get("default_image"):
#                     img_name = "None"
#                 else:
#                     try:
#                         urllib.request.urlretrieve(link, img_name)
#                     except Exception:
#                         img_name = "None"

#             img_names.append(img_name)

#         os.chdir(parent)
#     except Exception:
#         print("Exception (image_downloader):", sys.exc_info()[0])
#     return img_names


# -------------------------------------------------------------
# -------------------------------------------------------------

# returns a dictionary containing the user's posts
def scrape_posts(url, scan_list, section, elements_path):
    # page = []
    # page.append(url)
    # page += [url + s for s in section]
    try:
        # settings.driver.get(page[0])
        # print("scrape_posts")
        settings.driver.get(url)
        # time.sleep(3)
        # print("after waiting")

        # my_posts = {key: post_id, value: actual post}
        my_posts = utils.my_scroll(settings.number_of_posts, settings.driver, settings.selectors, settings.scroll_time, elements_path[0])

    except Exception:
        print(
            "Exception (scrape_data)",
            "Status =",
            # str(save_status),
            sys.exc_info()[0],
        )
        return
    return my_posts

# returns total number of friends, and number of mutual friends
def parse_friends_data(friends_data):
    friends_data = friends_data.replace(',', '')
    print(friends_data)
    friends_data = friends_data.replace('(', ' ')
    # print(friends_data)
    # friends_data = friends_data.replace(')', ' ')
    friends_data = [int(s) for s in friends_data.split() if s.isdigit()]
    print(friends_data)
    return friends_data


# returns user's friends total friends count and mutual friends count
# def scrape_friends_count(url, scan_list, section, elements_path):
def scrape_friends_count():
    try:
        settings.driver.execute_script(settings.selectors.get("scroll_script"))

        settings.driver.implicitly_wait(5)
        time.sleep(0.5)
        friends_element = settings.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[2]/div/div[1]/div[2]/div/div[3]/div/div/div/div[1]/div/div/div/div[2]/span/span')
        element_text = friends_element.text

    except Exception:
        print("scrape_friends_count: find_element FAILED")
        return [0]
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
    possible_day, possible_month, profile_year = profile_date.split(' ')
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
    print("after ints")
    print('day: ', profile_day, '\nmonth: ', profile_month, '\nyear: ', profile_year)
    age = today_year-profile_year + (today_month-profile_month)/12 + (today_day-profile_day)/365
    return age


def scrape_account_age(url):
    try:
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        photos_link = settings.driver.find_element_by_partial_link_text('Photos')
        photos_link.click()
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        albums = settings.driver.find_element_by_partial_link_text('Albums')
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        albums.click()
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        profile_pictures_link = settings.driver.find_element_by_partial_link_text('Profile')
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        profile_pictures_link.click()
        utils.friends_scroll(settings.driver, settings.selectors, settings.scroll_time)
        settings.driver.implicitly_wait(1)
        time.sleep(1)
        profile_pictures = settings.driver.find_elements_by_css_selector('.g6srhlxm.gq8dxoea.bi6gxh9e.oi9244e8.l9j0dhe7')
        last_pic = profile_pictures[len(profile_pictures)-1]
        time.sleep(1)
        last_pic.click()
        date_element = settings.driver.find_element_by_css_selector('.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.gmql0nx0.gpro0wi8.b1v8xokw')
        time.sleep(1)
        profile_date = date_element.get_attribute("aria-label")
        print('profile date: ', profile_date)
        today = date.today().strftime("%d/%m/%Y")
        print('today date: ', today)
        age = calculate_age(profile_date, today)
        settings.driver.get(url)
        time.sleep(1)
        return age
    except Exception:
        print("scrape_account_age: find_element FAILED")


def calculate_duration(friendship_year, friendship_month, today):
    today_day, today_month, today_year = today.split('/')
    today_day = int(today_day)
    today_month = int(today_month)
    today_year = int(today_year)

    friendship_month = month_switch(friendship_month)
    friendship_month = int(friendship_month)
    friendship_year = int(friendship_year)

    duration = today_year-friendship_year + (today_month-friendship_month)/12 + today_day/365
    return duration


def find_duration(url):
    # try:
        time.sleep(0.5)
        more_button = settings.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div[3]/div/div/div/div[2]/div/div/div[4]/div')
        time.sleep(0.5)
        more_button.click()
        time.sleep(0.5)

        friendship = settings.driver.find_element_by_xpath('/html/body/div[1]/div/div[1]/div[1]/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div/div[1]/div/a')
        friendship.click()
        time.sleep(3)
        common_things = settings.driver.find_elements_by_css_selector('.d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.rrkovp55.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.fe6kdd0r.mau55g9w.c8b282yb.iv3no6db.jq4qci2q.a3bd9o3v.knj5qynh.oo9gr5id.hzawbc8m')
        for thing in common_things:
            if "Your friend since" in thing.text:
                duration = thing.text
        print(duration)
        time.sleep(1)
        duration = duration.split(" ")
        duration = duration[3:]

        month = duration[0]
        year = 0
        if len(duration) > 1:
            year = int(duration[len(duration)-1])

        today = date.today().strftime("%d/%m/%Y")
        duration = calculate_duration(year, month, today)

        settings.driver.get(url)
        time.sleep(1)
        return duration
    # except Exception:
        print("find_duration: find_element FAILED")
        settings.driver.get(url)
        time.sleep(0.5)


def scrape_data(url, scan_list, section, elements_path, save_status):
    """Given some parameters, this function can scrap friends/photos/videos/about/posts(statuses) of a profile"""
    name = settings.driver.find_element_by_css_selector(".gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl.bp9cbjyn.j83agx80").text
    time.sleep(0.5)
    friendship_duration = find_duration(url)
    time.sleep(0.5)
    age = scrape_account_age(url)
    time.sleep(0.5)
    friends_data = scrape_friends_count()
    total_friends = friends_data[0]
    if len(friends_data) > 1:
        mutual_friends = friends_data[1]
    else:
        mutual_friends = 0
    print('total friends: ', total_friends, '\n', 'mutual friends: ', mutual_friends)
    posts = scrape_posts(url, scan_list, section, elements_path)
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


def scrap_all_friends():
    result = []
    # profile = settings.driver.find_element_by_xpath('./div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[1]/ul/li/div/a/div[1]/div[2]/div/div/div/div/span')
    settings.driver.find_element_by_css_selector('.gs1a9yip.ow4ym5g4.auili1gw.rq0escxv.j83agx80.cbu4d94t.buofh1pr.g5gj957u.i1fnvgqd.oygrvhab.cxmmr5t8.hcukyx3x.kvgmc6g5.tgvbjcpo.hpfvmrgz.rz4wbd8a.a8nywdso.l9j0dhe7.du4w35lb.rj1gh0hx.pybr56ya.f10w8fjw').click()
    time.sleep(0.5)
    url = settings.driver.current_url
    settings.driver.get(url+"/friends")
    time.sleep(0.5)

    friends_count = scrape_friends_count()
    print(friends_count)
    utils.friends_scroll(settings.driver, settings.selectors, settings.scroll_time)
    friends_block = settings.driver.find_element_by_css_selector('.dati1w0a.ihqw7lf3.hv4rvrfc.discj3wi')
    friends = friends_block.find_elements_by_css_selector('.oajrlxb2.gs1a9yip.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.q9uorilb.mg4g778l.btwxx1t3.pfnyh3mw.p7hjln8o.kvgmc6g5.wkznzc2l.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.p8dawk7l.pioscnbf.etr7akla')

    links = [friend.get_attribute('href') for friend in friends]

    print(links, "\n", len(links))
    list = []
    count = 0           # DEBUG: control num of iterations
    for link in links:
        count += 1
        settings.driver.get(link)
        list.append(scrap_profile())

        # DEBUG: control num of iterations
        if count >= 5:
            break
    return list


def scrap_profile():
    data_folder = os.path.join(os.getcwd(), "data")
    utils.create_folder(data_folder)
    os.chdir(data_folder)

    # execute for all profiles given in input.txt file
    url = settings.driver.current_url
    user_id = create_original_link(url)

    print("\nScraping:", user_id)

    try:
        target_dir = os.path.join(data_folder, user_id.split("/")[-1])
        utils.create_folder(target_dir)
        os.chdir(target_dir)
    except Exception:
        print("Some error occurred in creating the profile directory.")
        os.chdir("../..")
        return

    # to_scrap = ["Friends", "Photos", "Videos", "About", "Posts"]
    to_scrap = ["Posts"]
    for item in to_scrap:
        print("----------------------------------------")
        print("Scraping {}..".format(item))

        if item == "Posts":
            scan_list = [None]
        elif item == "About":
            scan_list = [None] * 7
        else:
            scan_list = settings.params[item]["scan_list"]

        section = settings.params[item]["section"]
        elements_path = settings.params[item]["elements_path"]
        save_status = settings.params[item]["save_status"]
        profile = scrape_data(user_id, scan_list, section, elements_path, save_status)

        print("{} Done!".format(item))

    print("Finished Scraping Profile " + str(user_id) + ".")
    os.chdir("../..")

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
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")

        try:
            settings.driver = webdriver.Chrome(
                executable_path=ChromeDriverManager().install(), options=options
            )
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


def scraper(email, password, user_url, mod, scrape_mod, **kwargs):
    print(scrape_mod)
    working_dir = os.path.dirname(os.path.abspath(__file__))
    if mod == Mode.Dev:

        with open(working_dir + "\credentials.yaml", "r") as ymlfile:
            cfg = yaml.safe_load(stream=ymlfile)

        if ("password" not in cfg) or ("email" not in cfg):
            print("Your email or password is missing. Kindly write them in credentials.txt")
            exit(1)
        email = cfg["email"]
        password = cfg["password"]

    # urls = [
    #     settings.facebook_https_prefix + settings.facebook_link_body + get_item_id(line)
    #     for line in open(working_dir + "\input.txt", newline="\r\n")
    #     if not line.lstrip().startswith("#") and not line.strip() == ""
    # ]
    login(email, password)
    if scrape_mod == Scrape_mode.Scrape_specific:
        # url = urls[0]
        settings.driver.get(user_url)
        result = [scrap_profile()]
    else:
        settings.selectors
        result = scrap_all_friends()
    settings.driver.close()
    return result

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------

# if __name__ == "__main__":
def main(email, password, user_url, mod, scrape_mod):
    # print(email, password)
    settings.ap = argparse.ArgumentParser()
    # PLS CHECK IF HELP CAN BE BETTER / LESS AMBIGUOUS
    # settings.ap.add_argument(
    #     "-dup",
    #     "--uploaded_photos",
    #     help="download users' uploaded photos?",
    #     default=True,
    # )
    # settings.ap.add_argument(
    #     "-dfp",
    #     "--friends_photos",
    #     help="download users' photos?",
    #     default=True
    # )
    # settings.ap.add_argument(
    #     "-fss",
    #     "--friends_small_size",
    #     help="Download friends pictures in small size?",
    #     default=True,
    # )
    # settings.ap.add_argument(
    #     "-pss",
    #     "--photos_small_size",
    #     help="Download photos in small size?",
    #     default=True,
    # )
    # settings.ap.add_argument(
    #     "-ts",
    #     "--total_scrolls",
    #     help="How many times should I scroll down?",
    #     default=2500,
    # )
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
        default=20
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

    # firefox_profile_path = settings.selectors.get("firefox_profile_path")
    settings.facebook_https_prefix = settings.selectors.get("facebook_https_prefix")
    settings.facebook_link_body = settings.selectors.get("facebook_link_body")

    # get things rolling
    scraper_result = scraper(email, password, user_url, mod, scrape_mod)
    return scraper_result
