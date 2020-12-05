import csv

from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from data_contracts.scan_result import ScanResult
from data_contracts.fb_user import FBUser
from scraper.modes import Scrape_mode, Mode, Scan_type
from scraper import scraper
from scraper import settings
from functools import partial
from analyzer import Analyzer
from results_file_writer import write_results_to_file
import os


def scrape_and_analyze(email, password, user_url, mod, scrape_mod, scan_type):
    scan_results = []
    if scrape_mod == Scrape_mode.Scrape_specific:
        users_to_analyze = scraper.main(email, password, user_url, mod, scrape_mod, scan_type)
    else:
        scraper.main(email, password, user_url, mod, scrape_mod, scan_type)
        users_to_analyze = read_friends_csv()
    for fb_user in users_to_analyze:
        user_result = Analyzer.analyze_user(fb_user)
        scan_results.append(user_result)

    # sort users result according to dangerous level
    scan_results.sort(reverse=True, key=calculate_analyzes_sum)  # sort descending, according to sum of analyzes

    # write results to file
    write_results_to_file(scan_results)

    return scan_results

def calculate_analyzes_sum(scan_result):
    offensive = scan_result.offensiveness_result.numeric
    fakeNews = scan_result.potentialFakeNews_result.numeric
    trigers = scan_result.trigers_result.numeric
    utv = scan_result.utv_result.numeric

    # calculate utv as: 1-utv (take the unreliable part)
    return offensive + fakeNews + trigers + (1-utv)


def read_friends_csv():
    path = os.path.dirname(__file__) + '/fb_friends.csv'
    friends_list = []
    with open(path, mode='r', encoding='utf-8') as fb_friends:
        friends_reader = csv.DictReader(fb_friends)
        for friend in friends_reader:
            age = friend['age']
            # print(age)
            if '.' in age:
                age = float(friend['age'])
            else:
                age = 0
            duration = friend['friendship_duration']
            # print(duration)
            if '.' in duration:
                duration = float(friend['friendship_duration'])
            else:
                duration = 0
            total_friends = int(friend['total_friends'])
            mutual_friends = int(friend['mutual_friends'])
            friends_list.append(FBUser(friend['name'], friend['url'], age,
                                       duration, total_friends, mutual_friends,
                                       friend['posts'].split('|||')))
        print

    if os.path.exists('fb_friends.csv'):
        os.remove('fb_friends.csv')
    return friends_list


posts = [
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה",
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה",
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה",
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה",
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה",
         "עיתון הארץ היטלר עושה רושם טוב טראמפ הוא אויב יותר מהיטלר וסטלין שטראמפ יבחר שוב אני אישית אדאג שכל מי שקשור לעיתון הזה יהיה בארהב פרסונה נון גרטה"
         ]       
fb_user = FBUser("", "", 1, 1, 1, 1, posts)
user_result = Analyzer.analyze_user(fb_user)
print(user_result.potentialFakeNews_result.percent)


