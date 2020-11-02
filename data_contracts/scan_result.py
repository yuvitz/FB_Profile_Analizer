from data_contracts.analysis_result import AnalysisResult

# the output of the analyzer - manager of all the analysis
# gathers all outputs of all aalysis
class ScanResult:
    user_name: str
    url: str
    offensiveness_result: AnalysisResult
    potentialFakeNews_result: AnalysisResult
    trigers_result: AnalysisResult
    utv_result: AnalysisResult

    def __init__(self, user_name, url, offensiveness_result: AnalysisResult, potentialFakeNews_result: AnalysisResult, trigers_result: AnalysisResult, utv_result: AnalysisResult):
        self.user_name = user_name
        self.url = url
        self.offensiveness_result = offensiveness_result
        self.potentialFakeNews_result = potentialFakeNews_result
        self.trigers_result = trigers_result
        self.utv_result = utv_result
