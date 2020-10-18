# data contract between the scraper and the analyzer
# used to retreive users info from the scraper
class FBUser:
    def __init__(self, name, url, age, friendship_duration, total_friends, mutual_friends, posts):
        self.name = name
        self.url = url
        self.age = age
        self.friendship_duration = friendship_duration
        self.total_friends = total_friends
        self.mutual_friends = mutual_friends
        self.posts = posts
