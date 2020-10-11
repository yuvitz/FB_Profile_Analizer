class ScanResult:
    def __init__(self, user_name, offensiveness_result, potentialFakeNews_result, subjects_result, utv_result):
        self.user_name = user_name
        self.offensiveness_result = offensiveness_result
        self.potentialFakeNews_result = potentialFakeNews_result
        self.subjects_result = subjects_result
        self.utv_result = utv_result
