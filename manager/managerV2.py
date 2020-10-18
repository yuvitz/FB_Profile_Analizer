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
        profile_result = Analyzer.analyze_user(fb_user)
        scan_result.append(profile_result)

    return scan_result