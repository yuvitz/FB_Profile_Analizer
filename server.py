import managerV2
from scan_result import ScanResult
from analysis_result import AnalysisResult
from modes import Scrape_mode, Mode, Scan_type
from flask import Flask, request, render_template, jsonify, make_response 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
   return render_template('Homepage.html')

@app.route('/scan_specific_user', methods=['GET'])
def scan_specific_user():
   return render_template('ScanSpecificUser.html')

@app.route('/scan_all_friends')
def scan_all_friends():
   return render_template('ScanAllFriends.html')

@app.route("/scan_result_specific_user", methods=['POST'])
def get_scan_result_specific_user():
	email = request.json['email']
	password = request.json['password']
	user_url = request.json['user_url']
	mod = Mode.Release							# release mode
	scrape_mod = Scrape_mode.Scrape_specific  	# scrape specific profile
	scan_type = Scan_type.full_scan
	scan_result = managerV2.scrape_and_analyze(email, password, user_url, mod, scrape_mod, scan_type)[0]

	return create_specific_user_result_template(scan_result)

@app.route("/scan_result_all_friends", methods=['POST'])
def scan_result_all_friends():
	email = request.json['email']
	password = request.json['password']
	user_url = ""
	mod = Mode.Release						# release mode
	scrape_mod = Scrape_mode.Scrape_all  	# scrape all friends
	scan_type = Scan_type.quick_scan			# run quick scan
	scan_results = managerV2.scrape_and_analyze(email, password, user_url, mod, scrape_mod, scan_type)
	# scan_results = [ ScanResult("Yuvi", "https://www.facebook.com", AnalysisResult(70, "A"), AnalysisResult(70, "A"), AnalysisResult(70, "A"), AnalysisResult(70, "A")) ]

	return render_template('ScanAllFriendsResultV2.html',
							scan_results = scan_results)

# create html template according to scan result
def create_specific_user_result_template(scan_result):
	return render_template('ScanSpecificUserResultV2.html',
							user_name = scan_result.user_name,
							offensiveness_result_percent = scan_result.offensiveness_result.percent,
							offensiveness_result_text = scan_result.offensiveness_result.text,
							potentialFakeNews_result_percent = scan_result.potentialFakeNews_result.percent,
							potentialFakeNews_result_text = scan_result.potentialFakeNews_result.text,
							trigers_result_percent = scan_result.trigers_result.percent,
							trigers_result_text = scan_result.trigers_result.text,
							utv_result_percent = scan_result.utv_result.percent,
							utv_result_text = scan_result.utv_result.text)

if __name__ == "__main__":
	app.run()