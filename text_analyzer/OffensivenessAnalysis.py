from . import OffensiveWords

# main func - determines the offensiveness level of user.
# gets all posts of profile, calculates offensiveness rate of profile, and returns result as text.
def analyze_profile_offensiveness(posts):
    # get total posts num
    postsNum = len(posts)
    if postsNum==0:
        return "User doesn't have any posts."
    
    offensivePostsNum = 0

    for post in posts:
        if is_post_offensive(post):
            offensivePostsNum+=1

    # calculate rate
    offensiveRate = offensivePostsNum / postsNum

    #convert rates to text result
    offensiveResultText = convert_offensive_rate_to_text(offensiveRate)
    return offensiveResultText

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