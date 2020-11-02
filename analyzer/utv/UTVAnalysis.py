from data_contracts.analysis_result import AnalysisResult

# UTV = user trust level
# aua = age of user account, fd = friendship duration, tf = total friends, mf = mutual friends
# all computations are according to Nadav's article
def analyze_user(fb_user):
    aua = fb_user.age
    fd = fb_user.friendship_duration
    tf = fb_user.total_friends
    mf = fb_user.mutual_friends
    # if isinstance(aua, str):
    #     aua = int(aua)
    if aua == 0 or fd == 0 or tf ==0 or mf == 0:
        return AnalysisResult("N\A", "Can't calculate user's trust level", 0)
        
    # Thresholds
    T_aua = 2
    T_fd = 1.5
    T_tf = 245
    T_mf = 37

    # User credibility attributes
    U_aua = 1 if aua >= T_aua else aua/T_aua
    U_tf = 1 if tf >= T_tf else tf/T_tf
    userCredibility = (U_aua + U_tf)/2

    # Connection strength attributes
    C_fd = 1 if fd >= T_fd else fd/T_fd
    C_mf = 1 if mf >= T_mf else mf/T_mf
    connectionStrength = (C_fd + C_mf)/2

    # UTV = (U*|U| + C*|C|) / |U + C|
    UTV = (userCredibility*2 + connectionStrength*2)/4
    
    # Convert to analysis result
    UTVPercent = str(UTV*100) + "%"
    # UTVText = utvAnalysisTextResult[UTV]
    UTVText = convert_utv_rate_to_text(UTV)

    return AnalysisResult(UTVPercent, UTVText, UTV)

def convert_utv_rate_to_text(utvRate):
    for rate in utvAnalysisTextResult.keys():
        if utvRate <= rate:
            return utvAnalysisTextResult[rate]
    return ""

utvAnalysisTextResult = {
    0.0: "USER IS DANGEROUS! DO NOT TRUST THEM!",
    0.4: "User is problematic! very low reliability rank",
    0.6: "User is not very reliable, you should pay attention",
    0.8: "User is ok.",
    0.9: "User is reliable.",
    1: "User is 100% reliable!"
}