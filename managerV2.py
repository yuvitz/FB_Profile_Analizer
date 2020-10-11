import tkinter as tk
from tkinter import messagebox
# from subprocess import call
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from scan_result import ScanResult
from modes import Scrape_mode, Mode
from scraper import scraper
from scraper import settings
from functools import partial
from text_analyzer import OffensivenessAnalysis
from text_analyzer import PotentialFakeNewsAnalysis
from text_analyzer import SubjectsAnalysis
from text_analyzer import UTVAnalysis

def scrape_and_analyze(email, password, user_url, mod, scrape_mod):
    scan_result = []
    profiles_to_analyze = scraper.main(email, password, user_url, mod, scrape_mod)
    for profile in profiles_to_analyze:
        profile_result = analyze_profile(profile)
        scan_result.append(profile_result)

    print("scan result:", scan_result)
    return scan_result

# gets posts of profile. performs all analysis, and render results
def analyze_profile(profile):
    posts = profile.posts
    name = profile.name
    if isinstance(posts, str):
        print(posts)
        return
    else:
        # perform all analyses
        offensiveness_result = OffensivenessAnalysis.analyze_profile_offensiveness(posts)
        potentialFakeNews_result = PotentialFakeNewsAnalysis.analyze_profile_potential_fake_news(posts)
        subjects_result = SubjectsAnalysis.analyze_profile_subjects(posts)
        utv_result = UTVAnalysis.analyze_UTV(profile.age, profile.friendship_duration,
                                        profile.total_friends, profile.mutual_friends)

    return ScanResult(name, offensiveness_result, potentialFakeNews_result, subjects_result, utv_result)