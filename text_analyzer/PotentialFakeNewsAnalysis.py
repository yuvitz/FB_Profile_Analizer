import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from googletrans import Translator
translator = Translator()
sid = SentimentIntensityAnalyzer()

def analyze_profile_potential_fake_news(posts):
    # get total posts num
    postsNum = len(posts)
    if postsNum==0:
        return "User doesn't have any posts."

    potentialFakePostsNum = 0

    for post in posts:
        if is_post_might_be_fake(post):
            potentialFakePostsNum+=1

    # calculate rate
    potentialFakeRate = potentialFakePostsNum / postsNum

    #convert rate to text result
    fakeResultText = convert_potential_fake_rate_to_text(potentialFakeRate)
    return fakeResultText

# check if post might be fake by analyzeing its polarity
def is_post_might_be_fake(post):  
    fake_threshold = 0.7
    englishText = translator.translate(post).text   # translate text
    print(englishText)

    # auto analysis
    sentimentDict = sid.polarity_scores(englishText)    # get sentiments of text
    print(sentimentDict)
    if sentimentDict['neg'] >= fake_threshold or sentimentDict['pos'] >= fake_threshold:
        return True
    
    #manual analysis
    manualSentimentCalc = analyze_manualy_sentiments_in_post(englishText) # get sentiments balance by counting words
    print(manualSentimentCalc)
    if manualSentimentCalc <= (-1)*fake_threshold or manualSentimentCalc >= fake_threshold:
        return True

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

    countPos=len(pos_word_list)
    countNeg=len(neg_word_list)
    countNeu=len(neu_word_list)
    countTotal=countNeg+countPos+countNeu
    sentimentCalc=0
    if(countPos==countNeg):
        sentimentCalc=0
    elif(countPos>countNeg):
        sentimentCalc=countPos/(countPos+countNeg)
    else:
        sentimentCalc=countNeg/(countPos+countNeg) * (-1)
    return sentimentCalc


def convert_potential_fake_rate_to_text(potentialFakeRate):
    for rate in potentialFakeNewsAnalsisTextResult.keys():
        if potentialFakeRate <= rate:
            return potentialFakeNewsAnalsisTextResult[rate]
    return ""

# dictinary of <offensive_rate, text_result>.
# used to convert offensive rate to text result.
# important! keep the rates going up from 0 to 1.
potentialFakeNewsAnalsisTextResult = {
    0.0 : "User is clean of potential fake news!",
    0.1 : "User is ok.",
    0.2 : "User rarely post potential fake news.",
    0.4 : "User often post potential fake news, pay attention!",
    0.6 : "User is problematic, most posts are potential fake news.",
    0.8 : "User is problematic, the vast majority of posts are potential fake news!",
    1 : "USER IS DANGEROUS! All posts are potential fake news!"
}

test_posts = [
    "משבר הקורונה הקפיץ את כלכלת המדינה ב200%. המשבר זה הדבר הכי טוב שקרה למדינה. כולנו צריכות להודות לקורונה.", 
    "מגדל האייפל הוא הכי גדול ומרשים, המגדל הכי גבוה בעולם.",
    "בשני שעבר אני ואישי היקר  נסענו לחוות החופש בכפר נחלולים ולא תאמינו מה בעלי המקום סיפרו לנו. מסתבר שכ-6 מיליון כבשים נרצחים בכל שנה (!) במדינת ישראל וכל זאת בידי היהודים הצוררים, לזכר אבותיהם שנספו במלחמת העולם השנייה. אני אומרת קאט דה בולשיט חבר'ס. בסך הכל רצינו לבלות סוף שבוע נעים עם הכבשים של @Atalia בעלת המקום ובמקום זה שמענו סיפורי זוועה. לנו נמאס לשמוע בכל פעם על עוד כבש שנרצחת בגלל דת ומנהגים, ועוד לגלות שהמדינה שלהם מגנה על המנהג הבזוי הזה??? אנחנו מאמינות שלכל אחת יש את החופש לבחור בדרכה שלה, אבל מכאן ועד לקרוא לרצח עם מנהג ואפילו מצווה??? שמישהו ייתן על זה את הדעת בבקשה.",
    "נכון לספט' 2020 הוקם בישראל מפעל לייצור רקטות באזור השפלה. אני מזועזעת מכך. מי שחושב כמוני שצריך להעמיד לדין את מקימי המפעל שילחץ לייק.",
    "בשעה טובה נברך את המלך שלנו, ביבי, על הוכחת חפותו בתיקים השונים וכן בתרומתו המדהימה על סך 7,000 שקלים לאזרחים נזקקים במדינה. תודה ביבי, אין עליך!",
    "אחוזי התחלואה בכלמידיה קבעו שיאים חדשים במדינת ישראל כאשר הכפילו את עצמם בין השנים 2000-2010 ואף הספיקו לשלש את עצמם עד לשנת 2020. ",
    "סירופ שוקולד זה המוצר הכי טוב שתוכלו לנסות, סוף סוף הצלחנו להיפטר מהנמלים במרפסת. מריחה קלילה על הפינות והנמלים בורחות",
    "כולם כבר יודעים שאי אפשר לסמוך על דוגלי. אחרי שעברתי בין החברות הטובות ביותר בשוק, גיליתי שהמוצרים של חברת דוגלי מזיקים לבעלי חיים ואף עלולים להרוג אותם. תיזהרו",
    "Obamacare will be replaced with a MUCH better, and FAR cheaper, alternative if it is terminated in the Supreme Court. Would be a big WIN for the USA!",
    "Wow, nobody realized how far Mini Mike Bloomberg went in bribing ex-prisoners to go out and vote for Sleepy Joe. He is desperate to get back into the good graces of the people who not only badly beat him, but made him look like a total fool. Now he’s committed a serious crime",
    "אנחנו בשעת חירום לאומי. כולנו צריכים להתגייס יחד כדי לנצח את הקורונה. עדכון חשוב ממני אליכם:",
    "לפי מצב התחלואה בישראל, סגר היה רק עניין של זמן. לכן עדיף סגר מלא עכשיו בחגים במחיר כלכלי נמוך יותר מאשר סגר אחרי החגים במחיר כלכלי גבוה יותר. הכלכלה שלנו חזקה והיא תתחזק עוד יותר בזכות רווחי הגז שהוצאנו מהאדמה ובזכות ההשקעות הענק שנביא בהסכם השלום עם איחוד האימרויות. הם יעזרו לנו לייצב את הכלכלה ולדאוג לרווחת אזרחי ישראל ולכל מי שיפגע כלכלית בזמן הסגר."
]

# result = analyze_profile_potential_fake_news(test_posts)
# print (result)