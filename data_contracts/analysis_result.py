# The output of each analysis
class AnalysisResult:
    percent: str
    text: str
    numeric: float

    def __init__(self, percetResult, textResult, numericResult):
        self.percent = percetResult
        self.text = textResult
        self.numeric = numericResult
