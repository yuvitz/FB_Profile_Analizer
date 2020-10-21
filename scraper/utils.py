import argparse
import os
import sys
import time
from calendar import calendar
from modes import Scan_type
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


# def create_post_link(post_id, selectors):
#     return (
#             selectors["facebook_https_prefix"] + selectors["facebook_link_body"] + post_id
#     )


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


# helper function: used to scroll the page
# def scroll(total_scrolls, driver, selectors, scroll_time):
#     global old_height
#     current_scrolls = 0

#     while True:
#         try:
#             if current_scrolls == total_scrolls:
#                 return

#             old_height = driver.execute_script(selectors.get("height_script"))
#             driver.execute_script(selectors.get("scroll_script"))
#             WebDriverWait(driver, scroll_time, 0.05).until(
#                 lambda driver: check_height(driver, selectors, old_height)
#             )
#             current_scrolls += 1


#         except TimeoutException:
#             break
#     return


# dictionary containing (id, posts)
def my_scroll(number_of_posts, driver, selectors, scroll_time, elements_path, scan_type):
    my_posts = []
    global old_height
    posts_scraped = 0
    cur_posts_scraped = 0
    last_post_id = 0
    start = time.time()
    # old_height = driver.execute_script(selectors.get("height_script"))
    # driver.execute_script("window.scrollBy(0, document.body.scrollHeight/3);")
    while posts_scraped < number_of_posts:
        try:
            # WebDriverWait(driver, scroll_time, 0.05).until(
            #     lambda driver: check_height(driver, selectors, old_height)
            # )
            data = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, elements_path))
            )
            # driver.execute_script(selectors.get("scroll_script"))
            # data = driver.find_elements_by_xpath(elements_path)
            driver.execute_script(selectors.get("scroll_script"))

            data = remove_comments(data)
            lim = number_of_posts-posts_scraped
            cur_posts_scraped, last_post_id, to_stop = my_extract_and_write_posts(data[posts_scraped:], lim, last_post_id, my_posts, start, scan_type)
            # end = time.time()
            # if exps_in_row >= 10 or (scan_type==Scan_type.quick_scan and (end-start > 20)):
            if to_stop:
                print("posts took:", time.time() - start, "seconds")
                return my_posts
            # old_height = driver.execute_script(selectors.get("height_script"))
            # posts_scraped += cur_posts_scraped

        except TimeoutException:
            print("posts took:", time.time() - start, "seconds")
            return my_posts
    print("posts took:", time.time()-start, "seconds")
    return my_posts

    
def friends_scroll(driver, selectors, scroll_time):
    my_posts = {}
    global old_height

    posts_scraped = 0
    cur_posts_scraped = 0
    last_post_id = 0

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
            # if loop_count >=3:
            #     break
            # data = driver.find_elements_by_xpath(elements_path)
            # data = remove_comments(data)
            # lim = number_of_posts-posts_scraped
            # cur_posts_scraped, last_post_id = my_extract_and_write_posts(data[posts_scraped:], lim, last_post_id, my_posts)
            # posts_scraped += cur_posts_scraped

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
    if scan_type == Scan_type.full_scan:
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
        post = x.find_element_by_xpath('./div/div/div/div/div/div[2]/div/div[3]/div/div/div/div/span')
        try:
            see_more_button = post.find_element_by_css_selector('.oajrlxb2.g5ia77u1.qu0x051f.esr5mh6w.e9989ue4.r7d6kgcz.rq0escxv.nhd2j8a9.nc684nl6.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.jb3vyjys.rz4wbd8a.qt6c0cv9.a8nywdso.i1ao9s8h.esuyzwwr.f1sip0of.lzcic4wl.oo9gr5id.gpro0wi8.lrazzd5p')
            see_more_button.click()
        except NoSuchElementException:
            pass
        statuses = post.find_elements_by_xpath('./*[contains(@class, cxmmr5t8)]/div')
        for item in statuses:
            status += item.text
        exps_in_row = 0

    except Exception:

        #     try:
        #         status = x.find_element_by_xpath(selectors.get("status_exc")).text
        #     except Exception:
        #         pass
        print("my_get_status exception")
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

# def get_status(x, selectors):
#     status = ""
#     try:
#         status = x.find_element_by_xpath(
#             selectors.get("status")
#         ).text  # use _1xnd for Pages
#     except Exception:
#         try:
#             status = x.find_element_by_xpath(selectors.get("status_exc")).text
#         except Exception:
#             pass
#     return status


# def get_post_id(x):
#     post_id = -1
#     try:
#         post_id = x.get_attribute("id")
#         post_id = post_id.split(":")[-1]
#     except Exception:
#         pass
#     return post_id


# def get_group_post_id(x):
#     post_id = -1
#     try:
#         post_id = x.get_attribute("id")

#         post_id = post_id.split("_")[-1]
#         if ";" in post_id:
#             post_id = post_id.split(";")
#             post_id = post_id[2]
#         else:
#             post_id = post_id.split(":")[0]
#     except Exception:
#         pass
#     return post_id


# def get_photo_link(x, selectors, small_photo):
#     link = ""
#     try:
#         if small_photo:
#             link = x.find_element_by_xpath(
#                 selectors.get("post_photo_small")
#             ).get_attribute("src")
#         else:
#             link = x.get_attribute("data-ploi")
#     except NoSuchElementException:
#         try:
#             link = x.find_element_by_xpath(
#                 selectors.get("post_photo_small_opt1")
#             ).get_attribute("src")
#         except AttributeError:
#             pass
#         except Exception:
#             print("Exception (get_post_photo_link):", sys.exc_info()[0])
#     except Exception:
#         print("Exception (get_post_photo_link):", sys.exc_info()[0])
#     return link


# def get_post_photos_links(x, selectors, small_photo):
#     links = []
#     photos = safe_find_elements_by_xpath(x, selectors.get("post_photos"))
#     if photos is not None:
#         for el in photos:
#             links.append(get_photo_link(el, selectors, small_photo))
#     return links


# def get_div_links(x, tag, selectors):
#     try:
#         temp = x.find_element_by_xpath(selectors.get("temp"))
#         return temp.find_element_by_tag_name(tag)
#     except Exception:
#         return ""


# def get_title_links(title):
#     l = title.find_elements_by_tag_name("a")
#     return l[-1].text, l[-1].get_attribute("href")


# def get_title(x, selectors):
#     title = ""
#     try:
#         title = x.find_element_by_xpath(selectors.get("title"))
#     except Exception:
#         try:
#             title = x.find_element_by_xpath(selectors.get("title_exc1"))
#         except Exception:
#             try:
#                 title = x.find_element_by_xpath(selectors.get("title_exc2"))
#             except Exception:
#                 pass
#     finally:
#         return title


# def get_time(x):
#     time = ""
#     try:
#         time = x.find_element_by_tag_name("abbr").get_attribute("title")
#         time = (
#                 str("%02d" % int(time.split(", ")[1].split()[1]), )
#                 + "-"
#                 + str(
#             (
#                     "%02d"
#                     % (
#                         int(
#                             (
#                                 list(calendar.month_abbr).index(
#                                     time.split(", ")[1].split()[0][:3]
#                                 )
#                             )
#                         ),
#                     )
#             )
#         )
#                 + "-"
#                 + time.split()[3]
#                 + " "
#                 + str("%02d" % int(time.split()[5].split(":")[0]))
#                 + ":"
#                 + str(time.split()[5].split(":")[1])
#         )
#     except Exception:
#         pass

#     finally:
#         return time


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


# def safe_find_elements_by_xpath(driver, xpath):
#     try:
#         return driver.find_elements_by_xpath(xpath)
#     except NoSuchElementException:
#         return None


# def get_replies(comment_element, selectors):
#     replies = []
#     data = comment_element.find_elements_by_xpath(selectors.get("comment_reply"))
#     for d in data:
#         try:
#             author = d.find_element_by_xpath(selectors.get("comment_author")).text
#             text = d.find_element_by_xpath(selectors.get("comment_text")).text
#             replies.append([author, text])
#         except Exception:
#             pass
#     return replies


def safe_find_element_by_id(driver, elem_id):
    try:
        return driver.find_element_by_id(elem_id)
    except NoSuchElementException:
        return None
