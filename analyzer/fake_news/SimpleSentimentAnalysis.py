import nltk
from . import Subjects
from . import OffensiveWords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
translator = Translator()
sid = SentimentIntensityAnalyzer()

def detect_language(post):
    language = translator.detect(post)
    if language.lang == 'iw' or language.lang == 'he':
        language = 'Hebrew'
    elif language == 'en': language = 'English'
    else:
        language = language.lang
    return language

# check if word exist in each subject
# improve - currently returns only one subject per word
def find_word_in_subjects(word):
    subjects = Subjects.subjects
    for subject in subjects:
        if word in subjects[subject]:  
            return subject
    return

# calculate post's subject
# improve - currently returns only one subject per post
def detect_post_subject(post: str) -> str:
    subjects_word_count = {}    # holds word count per subject
    postWords = post.split()
    postWordsNum = len(postWords)
    # threshold = 0.5*postWordsNum  # super strict threshold!
    threshold = 0.05*postWordsNum   # onother threshold!
    print (threshold)

    for word in postWords:
        wordSubjcet = find_word_in_subjects(word)
        if wordSubjcet in subjects_word_count.keys():
            subjects_word_count[wordSubjcet] += 1
        else:
            subjects_word_count.update({wordSubjcet : 1})
    
    for subject in subjects_word_count:
        if subjects_word_count[subject] >= threshold:
            return subject
    return ""

# check if post is offenive by counting offensive words in it
def is_post_offensive(post):
    postWords = post.split()
    postWordsNum = len(postWords)
    threshold = 0.05*postWordsNum   # threshold!
    offensiveWordsNum = 0

    for word in postWords:
        if word in OffensiveWords.offensiveWords:
            offensiveWordsNum += 1

    if offensiveWordsNum >= threshold:
        return True
    else:
        return False

# check if post might be fake by analyzeing its polarity
def is_post_might_be_fake(post):  
    englishText = translator.translate(post).text   # translate text
    sentimentDict = sid.polarity_scores(englishText)  # get emotions of text

    return False

def analyze_post(post):
    # translate text
    englishText = translator.translate(post).text

    # calculate post's subject
    subject = detect_post_subject(post)

    # get emotions of text
    sentimentDict=sid.polarity_scores(englishText)

    return sentimentDict

def analyze_posts_of_profile(posts):
    offensivePostsNum = 0
    fakePostsNum = 0

    for post in posts:
        if is_post_offensive(post):
            offensivePostsNum+=1
        if is_post_might_be_fake(post):
            fakePostsNum+=1

    # calculate rates
    postsNum = len(posts)
    offensiveRate = offensivePostsNum / postsNum
    fakeRate = fakePostsNum / postsNum

    #convert rates to text result
    offensiveResultText = convert_offensive_rate_to_text(offensiveRate)
    fakeResultText = convert_polarity_rate_to_text(fakeRate)
    return (offensiveResultText, fakeResultText)

def analyze_profile_offensiveness(posts):
    return

def analyze_profile_emotional_polarity(posts):
    return

def convert_offensive_rate_to_text(offensiveRate):
    return ""

def convert_polarity_rate_to_text(fakeRate):
    return ""


# analyze_post("בדיקה")