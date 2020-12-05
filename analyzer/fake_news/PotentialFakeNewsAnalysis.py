import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
from data_contracts.analysis_result import AnalysisResult
translator = Translator()
sid = SentimentIntensityAnalyzer()

def analyze_user(fb_user):
    posts = fb_user.posts
    potentialFakePostsNum = 0
    postsNum = len(posts) # get total posts num  

    for post in posts:
        if post is not None:
            if check_fake_potential(post):
                potentialFakePostsNum += 1

    # calculate rate
    potentialFakeRate = potentialFakePostsNum / postsNum

    #convert to analysis result
    percent = int((potentialFakeRate*100) // 1)
    percentResult = str(percent) + "%"
    textResult = convert_potential_fake_rate_to_text(potentialFakeRate)

    return AnalysisResult(percentResult, textResult, potentialFakeRate)

# check if a post might be fake by analyzing it's polarity
# idea:
# auto check >= high threshold --- return true
# auto check >= mid threshold && manual check >= super high threshold -- return true
# algo: 
# get auto calculated sentiments
# if sentiments pass high treshold - return true
# if sentiments pass mid threshold - check also manually
# if manual chack pass the super high threshold - return true
def check_fake_potential(post):  
    fake_threshold_super_high = 0.8
    fake_threshold_high = 0.7
    fake_threshold_mid = 0.5
    try:
        englishText = translator.translate(post).text   # translate text

        # auto analysis by nltk
        sentimentDict = sid.polarity_scores(englishText)    # get sentiments of text
        print(sentimentDict)
        # check if sentiments indicates high fake potential
        if sentimentDict['neg'] >= fake_threshold_high or sentimentDict['pos'] >= fake_threshold_high:
            return True

        # check if sentiments indicates mid fake potential
        elif sentimentDict['neg'] >= fake_threshold_mid or sentimentDict['pos'] >= fake_threshold_mid or abs(sentimentDict['compound']) >= fake_threshold_super_high:
            # manual analysis
            manualSentimentCalc = analyze_manualy_sentiments_in_post(englishText) # get sentiments balance by counting words
            print(manualSentimentCalc)
            if abs(manualSentimentCalc) >= fake_threshold_super_high:
                return True
    except Exception:
        return False
    return False

# analyze sentiments manually - by counting words
def analyze_manualy_sentiments_in_post(englishText):
    pos_word_list = []
    neg_word_list = []
    neu_word_list = []
    wordList = re.sub("[^\w]", " ", englishText).split()
    
    for word in wordList:
        if (sid.polarity_scores(word)['compound']) >= 0.1:
            pos_word_list.append(word)
        elif (sid.polarity_scores(word)['compound']) <= -0.1:
            neg_word_list.append(word)
        else:
            neu_word_list.append(word)

    countPos = len(pos_word_list)
    countNeg = len(neg_word_list)
    countNeu = len(neu_word_list)
    countTotal = countNeg + countPos + countNeu
    sentimentCalc = 0

    if(countPos == countNeg):
        sentimentCalc = 0
    elif(countPos > countNeg):
        sentimentCalc = countPos / (countPos + countNeg)
    else:
        sentimentCalc = countNeg / (countPos + countNeg) * (-1)
    return sentimentCalc


def convert_potential_fake_rate_to_text(potentialFakeRate):
    for rate in potentialFakeNewsAnalysisTextResult.keys():
        if potentialFakeRate <= rate:
            return potentialFakeNewsAnalysisTextResult[rate]
    return ""

# dictinary of <offensive_rate, text_result>.
# used to convert offensive rate to text result.
# important! keep the rates going up from 0 to 1.
potentialFakeNewsAnalysisTextResult = {
    0.0 : "User is clean of potential fake news!",
    0.1 : "User is ok.",
    0.2 : "User rarely post potential fake news.",
    0.4 : "User often post potential fake news, pay attention!",
    0.6 : "User is problematic, most posts are potential fake news.",
    0.8 : "User is problematic, the vast majority of posts are potential fake news!",
    1 : "USER IS DANGEROUS! All posts are potential fake news!"
}