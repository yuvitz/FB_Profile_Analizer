import fb_user
# UTV = user trust level
# aua = age of user account, fd = friendship duration, tf = total friends, mf = mutual friends
# all computations are according to Nadav's article
def analyze_UTV(aua, fd, tf, mf):
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
    return UTV
