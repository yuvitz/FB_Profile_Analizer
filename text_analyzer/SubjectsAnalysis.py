from . import Subjects
from googletrans import Translator

def analyze_profile_subjects(posts):
    # get total posts num
    postsNum = len(posts)
    if postsNum==0:
        return "User doesn't have any posts."
    
    # check what is the rate of posts of each subject
    # create dict of results: <subject, subjectPostsRate>
    subjects = Subjects.subjects
    subjectsPostsCount = dict()
    
    # count how may posts are there for each subject
    for post in posts:
        postSubjects = detect_post_subjects_V2(post, subjectsPostsCount)
        increase_count(subjectsPostsCount, postSubjects)

    # calculate subjects rates
    subjectsPostsRates = dict()
    for subject in subjectsPostsCount:
        subjectsPostsRates[subject] = subjectsPostsCount[subject] / postsNum  # calculate rate of posts in this subject
    
    #convert to text result
    subjectsResultText = convert_subjects_rates_to_text(subjectsPostsRates)
    return subjectsResultText

# calculate post's subject and add to counter dictionary
# improve - currently returns only one subject per post
def detect_post_subjects(post, counterDictionary):
    subjects_word_count = {}    # holds word count per subject
    postWords = post.split()
    postWordsNum = len(postWords)

    threshold = 0.05*postWordsNum   # threshold!

    for word in postWords:
        wordSubjcets = find_word_in_subjects(word)
        increase_count(subjects_word_count, wordSubjcets)
    
    # increase post subject in counter dict
    for subject in subjects_word_count:
        if subjects_word_count[subject] >= threshold:
            increase_count(counterDictionary, subject)
            
    return counterDictionary

def detect_post_subjects_V2(post, counterDictionary):
    post_subjects = set()
    postSentences = post.split(".")
    
    for sentence in postSentences:
        sentenceWords = post.split()
        for word in sentenceWords:
            wordSubjcets = detect_word_subjects(word)
            if wordSubjcets!=None:
                for wordSubject in wordSubjcets:    
                    post_subjects.add(wordSubject)
            
    return post_subjects

def increase_count(dictionary, subjects):
    for subject in subjects:
        if subject in dictionary.keys():
            dictionary[subject] += 1
        else:
            dictionary.update({subject : 1})
    return

# check if word exist in each subject
# improve - currently returns only one subject per word
def detect_word_subjects(word):
    subjects = Subjects.subjects
    wordSubjects = set()
    for subject in subjects:
        for subject_word in subjects[subject]:
            if word==subject_word or word=="ה"+subject_word:       # check if current word is substring of the subject word 
                wordSubjects.add(subject)
    return wordSubjects

def convert_subjects_rates_to_text(subjectsPostsRates):
    textResult = "Posts of user according to subjects: "

    for subject in subjectsPostsRates.keys():
        if subject != None:
            textResult += subject + ": " + str(subjectsPostsRates[subject]) + ","
    
    return textResult[:-1]  # trim the last ","