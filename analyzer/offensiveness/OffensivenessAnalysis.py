from analyzer.offensiveness import OffensiveWords
from data_contracts.analysis_result import AnalysisResult

# main func - determines the offensiveness level of user.
# gets all posts of profile, calculates offensiveness rate of profile, and returns result as text.
def analyze_user(fb_user):
    posts = fb_user.posts
    offensivePostsNum = 0  
    postsNum = len(posts) # get total posts num

    for post in posts:
        if is_post_offensive_V2(post):
            offensivePostsNum+=1

    # calculate rate
    offensiveRate = offensivePostsNum / postsNum

    #convert rates to text result
    percent = int((offensiveRate*100) // 1)
    offensiveResultPercent = str(percent) + "%"
    offensiveResultText = convert_offensive_rate_to_text(offensiveRate)

    return AnalysisResult(offensiveResultPercent, offensiveResultText, offensiveRate)

# check if post is offenive by 
# idea: counting offensive words in it, and compare offensive words rate to threshold
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

# check if post is offensive
# idea: check if one of the offensive words or phrases appears in the post
# we claim that only one word or ohrase is enough.
def is_post_offensive_V2(post):
    offensiveWords = OffensiveWords.offensiveWords 

    # if one of the offensive words or phrases appears in post - return true
    for word in offensiveWords:
        if word in post:
            return True

    return False

# converts offensivenes rate to text result.
def convert_offensive_rate_to_text(offensiveRate):
    for rate in offensiveAnalysisTextResult.keys():
        if offensiveRate <= rate:
            return offensiveAnalysisTextResult[rate]
    return ""

# dictinary of <offensive_rate, text_result>.
# used to convert offensive rate to text result.
# important! keep the rates going up from 0 to 1.
offensiveAnalysisTextResult = {
    0.0 : "User is clean of offensiveness!",
    0.1 : "User is ok.",
    0.2 : "User rarely post offensive posts.",
    0.4 : "User often post offensive posts, pay attention!",
    0.6 : "User is problematic, most posts are offensive.",
    0.8 : "User is problematic, the vast majority of posts are offensive!",
    1 : "USER IS DANGEROUS! ALL POSTS ARE OFFENSIVE!"
}