import manager
from data_contracts.scan_result import ScanResult
from data_contracts.analysis_result import AnalysisResult
from scraper import modes
# from modes import Mode
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


@app.route('/about')
def about():
   return render_template('About.html')


@app.route('/contact')
def contact():
   return render_template('Contact.html')


@app.route("/scan_result_specific_user", methods=['POST'])
def get_scan_result_specific_user():
	email = request.json['email']
	password = request.json['password']
	user_url = request.json['user_url']
	mod = modes.Mode.Release							# release mode
	scrape_mod = modes.Scrape_mode.Scrape_specific  	# scrape specific profile
	scan_type = modes.Scan_type.full_scan
	scan_result = manager.scrape_and_analyze(email, password, user_url, mod, scrape_mod, scan_type)[0]

	return create_specific_user_result_template(scan_result)

@app.route("/scan_result_all_friends", methods=['POST'])
def scan_result_all_friends():
	email = request.json['email']
	password = request.json['password']
	user_url = ""
	mod = modes.Mode.Release							# release mode
	scrape_mod = modes.Scrape_mode.Scrape_all  			# scrape all friends
	scan_type = get_scan_type_from_request(request)

	scan_results = manager.scrape_and_analyze(email, password, user_url, mod, scrape_mod, scan_type)

	return render_template('ScanAllFriendsResult.html',
							scan_results = scan_results)

def get_scan_type_from_request(request):
	should_run_full_scan = request.json['fullScan'] # if true - run full scan
	print(should_run_full_scan)
	if should_run_full_scan:
		return modes.Scan_type.full_scan
	else:
		return modes.Scan_type.quick_scan

# create html template according to scan result
def create_specific_user_result_template(scan_result):
	return render_template('ScanSpecificUserResult.html',
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