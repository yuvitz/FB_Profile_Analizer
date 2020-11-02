from analyzer.offensiveness import OffensivenessAnalysis
from analyzer.fake_news import PotentialFakeNewsAnalysis
from analyzer.trigers import TrigersAnalysis
from analyzer.utv import UTVAnalysis
from data_contracts.scan_result import ScanResult
from data_contracts.analysis_result import AnalysisResult

############ analysis manager ############

# gets facebook user object, performs all analysis, and returns results as ScanResult object
def analyze_user(fb_user):
    posts = fb_user.posts

    if len(posts)==0:
        # result for none posts profile
        return create_not_enough_posts_result(fb_user, "This user doesn't have any posts, hence does not have result.")

    elif len(posts)<=5:
        # result for not enough posts profile
        return create_not_enough_posts_result(fb_user, "This user doesn't have enough posts to derive conclusions from.")

    else:
        # perform all analyses
        offensiveness_result = OffensivenessAnalysis.analyze_user(fb_user)
        potentialFakeNews_result = PotentialFakeNewsAnalysis.analyze_user(fb_user)
        trigers_result = TrigersAnalysis.analyze_user(fb_user)
        utv_result = UTVAnalysis.analyze_user(fb_user)

    return ScanResult(fb_user.name, fb_user.url, offensiveness_result, potentialFakeNews_result, trigers_result, utv_result)

# create result for profile with not enough posts (0 posts or not enough)
def create_not_enough_posts_result(fb_user, text_result):
        text_analyzers_result = AnalysisResult("N\A", text_result, 0)
        utv_result = UTVAnalysis.analyze_user(fb_user)
        result = ScanResult(fb_user.name, fb_user.url, text_analyzers_result, text_analyzers_result, text_analyzers_result, utv_result)
        return result