from enum import Enum


class Mode(Enum):
    Release = 1
    Dev = 2



class Scrape_mode(Enum):
    Scrape_specific = 1
    Scrape_all = 2
