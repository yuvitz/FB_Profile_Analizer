import csv
import os
from data_contracts import fb_user


def encode_posts(posts):
    posts_string = ""
    for post in posts:
        posts_string += post+"|||"
    return posts_string


def write_fb_friends_to_file(friend, count):
    path = os.path.dirname(__file__) + '/../fb_friends.csv'
    posts = encode_posts(friend.posts)
    with open(path, mode='a', encoding='utf-8') as fb_friends:
        fieldnames = ['name', 'url', 'age', 'friendship_duration', 'total_friends', 'mutual_friends', 'posts']
        friends_writer = csv.DictWriter(fb_friends, fieldnames=fieldnames)
        # headline
        if count == 1:
            friends_writer.writeheader()
        row = {'name': friend.name,
               'url': friend.url,
               'age': friend.age,
               'friendship_duration':  friend.friendship_duration,
               'total_friends': friend.total_friends,
               'mutual_friends': friend.mutual_friends,
               'posts': posts}

        friends_writer.writerow(row)

