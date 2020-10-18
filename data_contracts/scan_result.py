from data_contracts.analysis_result import AnalysisResult

# the output of the analyzer - manager of all the analysis
# gathers all outputs of all aalysis
class ScanResult:
    def __init__(self, user_name, offensiveness_result: AnalysisResult, potentialFakeNews_result: AnalysisResult, subjects_result: AnalysisResult, utv_result: AnalysisResult):
        self.user_name = user_name
        self.offensiveness_result = offensiveness_result
        self.potentialFakeNews_result = potentialFakeNews_result
        self.subjects_result = subjects_result
        self.utv_result = utv_result
