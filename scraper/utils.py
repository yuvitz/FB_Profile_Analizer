import argparse
import os
import sys
import time
from calendar import calendar
from . import modes, settings
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def to_bool(x):
    if x in ["False", "0", 0, False]:
        return False
    elif x in ["True", "1", 1, True]:
        return True
    else:
        raise argparse.ArgumentTypeError("Boolean value expected")


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


# -------------------------------------------------------------
# Helper functions for Page scrolling
# -------------------------------------------------------------
# check if height changed
def check_height(driver, selectors, old_height):
    new_height = driver.execute_script(selectors.get("height_script"))
    return new_height != old_height


# dictionary containing (id, posts)
def my_scroll(number_of_posts, driver, selectors, scroll_time, elements_path, scan_type):
    my_posts = []
    global old_height
    posts_scraped = 0
    # cur_posts_scraped = 0
    last_post_id = 0
    start = time.time()
    while posts_scraped < number_of_posts:
        try:
            data = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, elements_path)))
            driver.execute_script(selectors.get("scroll_script"))

            data = remove_comments(data)
            lim = number_of_posts-posts_scraped

            cur_posts_scraped, last_post_id, to_stop = my_extract_and_write_posts(data[posts_scraped:], lim, last_post_id, my_posts, start, scan_type)

            if to_stop:
                print("posts took:", time.time() - start, "seconds")
                return my_posts

        except TimeoutException:
            print("posts took:", time.time() - start, "seconds")
            return my_posts

        except Exception:
            print("my_scroll() exception",
            "Status =",
            sys.exc_info()[0],)
            return my_posts

    print("posts took:", time.time()-start, "seconds")
    return my_posts

    
def friends_scroll(driver, selectors, scroll_time):
    # global old_height
    old_height = driver.execute_script(selectors.get("height_script"))
    # loop_count = 0     # just for debug, to prevent long runs
    while True:
        # loop_count += 1
        try:
            driver.execute_script(selectors.get("scroll_script"))
            WebDriverWait(driver, scroll_time, 0.05).until(
                lambda driver: check_height(driver, selectors, old_height)
            )
            new_height = driver.execute_script(selectors.get("height_script"))
            if old_height == new_height:
                break
            old_height = new_height

        except TimeoutException:
            break
    return


def remove_comments(data):
    posts = []
    for x in data:
        post_id = -1
        try:
            post_id = x.get_attribute("aria-posinset")
            if post_id != None:
                posts.append(x)
        except Exception:
            pass
    return posts


def my_extract_and_write_posts(elements, lim, last_post_id, my_posts, start, scan_type):
    if scan_type == modes.Scan_type.full_scan:
        time_lim = 60
    else:
        time_lim = 30
    to_stop = False
    try:
        posts_written = 0
        for x in elements:
            if time.time() - start >= time_lim:
                to_stop = True
                break
            try:
                post_id = my_get_post_id(x)
                int_post_id = int(post_id)
                if post_id != None:
                    if int_post_id > last_post_id:
                        status = my_get_status(x)
                        # print(status)
                        try:
                            if status != "":
                                my_posts.append(status)
                                posts_written += 1
                                last_post_id = int_post_id
                                if posts_written == lim:
                                    break
                        except Exception:
                            print("Posts: Could not map encoded characters")
            except Exception:
                print("passing")
                pass
    except ValueError:
        print("Exception Value (my_extract_and_write_posts)", "Status =", sys.exc_info()[0])
    except Exception:
        print("Exception General (my_extract_and_write_posts)", "Status =", sys.exc_info()[0])
    return posts_written, last_post_id, to_stop


# -----------------------------------------------------------------------------
# MyHelper Functions for Posts
# -----------------------------------------------------------------------------

def my_get_status(x):
    status = ""
    statuses = []
    try:
        post = x.find_element_by_xpath(settings.selectors.get("post"))
        try:
            see_more_button = post.find_element_by_css_selector(settings.selectors.get("see_more"))
            see_more_button.click()
        except NoSuchElementException:
            pass
        statuses = post.find_elements_by_xpath('./*[contains(@class, cxmmr5t8)]/div')
        for item in statuses:
            status += item.text
        # exps_in_row = 0

    except Exception:
        pass

    return status


def my_get_post_id(x):
    post_id = -1
    try:
        post_id = x.get_attribute("aria-posinset")
    except Exception:
        pass
    return post_id


# -----------------------------------------------------------------------------
# Helper Functions for Posts
# -----------------------------------------------------------------------------


def identify_url(url):
    """
    A possible way to identify the link.
    Not Exhaustive!
    :param url:
    :return:
    0 - Profile
    1 - Profile post
    2 - Group
    3 - Group post
    """
    if "groups" in url:
        if "permalink" in url:
            return 3
        else:
            return 2
    elif "posts" in url:
        return 1
    else:
        return 0


def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None
