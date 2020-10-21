import tkinter as tk
from tkinter import messagebox
# from subprocess import call
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from data_contracts.scan_result import ScanResult
from data_contracts.fb_user import FBUser
from modes import Scrape_mode, Mode
from scraper import scraper
from scraper import settings
from functools import partial
from analyzer import Analyzer


def scrape_and_analyze(email, password, user_url, mod, scrape_mod, should_run_full_scan):
    scan_result = []

    users_to_analyze = scraper.main(email, password, user_url, mod, scrape_mod, should_run_full_scan)
    for fb_user in users_to_analyze:
        print(fb_user.url)
        user_result = Analyzer.analyze_user(fb_user)
        scan_result.append(user_result)

    return scan_result


### test
posts = [ "בתחת שלי כל הבלה בלה בלה הזה", "יא הומו!", "שחקני כדורגל הם מטומטמים", "הגברת התלוננה על הטרדה מינית", "מכירת סמי פיצוציות זה פאסה", "הפיגוע שהיה אתמול היה מחריד" ]
fb_user = FBUser("Yuvi", "www.facebook.com", 1, 1, 1, 1, posts)
user_result = Analyzer.analyze_user(fb_user)

off = user_result.offensiveness_result
fake = user_result.potentialFakeNews_result
trigers = user_result.trigers_result

print("1. " + off.percent + " " + off.text)
print("2. " + fake.percent + " " + fake.text)
print("3. " + trigers.percent + " " + trigers.text)