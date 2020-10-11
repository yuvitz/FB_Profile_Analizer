import managerV2
from scan_result import ScanResult
from modes import Scrape_mode, Mode
from flask import Flask, request, render_template, jsonify, make_response 
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# @app.route("/output")
# def output():
#	return render_template('scan_result.html', scan_result="Hello World!")

@app.route('/')
def home():
   return render_template('Homepage.html')

@app.route('/example', methods=['POST'])
def example():
	data = request.json
	print(data)
	print(request.json)
	# print(jsonify(data))
	print(request.json['email'])
	headers = {'Content-Type': 'text/html'}
	response = make_response(render_template('SpecificUserResult.html'), 200 ,headers)
	print (response)
	return response
	return render_template('SpecificUserResult.html',
							user_name = "A",
							offensiveness_result = "A",
							potentialFakeNews_result = "A",
							subjects_result = "A",
							utv_result = "A")

@app.route('/scan_specific_user', methods=['GET'])
def scan_specific_user():
   return render_template('ScanSpecificUser.html')

@app.route('/scan_all_friends')
def scan_all_friends():
   return render_template('ScanAllFriends.html')

@app.route("/get_scan_result_specific_user/<email>/<password>")
def get_scan_result_specific_user(email, password):
	print("aaaa")
	#email = request.json['email']
	#password = request.json['password']
	#user_url = request.json['user_url']
	print(email)
	mod = Mode.Release							# release mode
	scrape_mod = Scrape_mode.Scrape_specific  	# scrape specific profile
	# scan_result = managerV2.scrape_and_analyze(email, password, user_url, mod, scrape_mod)[0]
	scan_result = ScanResult("yuvi", "a", "b", "c", 1.0)

	return render_template('SpecificUserResult.html',
							user_name = scan_result.user_name,
							offensiveness_result = scan_result.offensiveness_result,
							potentialFakeNews_result = scan_result.potentialFakeNews_result,
							subjects_result = scan_result.subjects_result,
							utv_result = scan_result.utv_result)

@app.route("/scan_all_friends/scan", methods=['POST'])
def scan_all_friends_scan():
	print("aaaa")
	email = request.json['email']
	password = request.json['password']
	user_url = ""
	mod = Mode.Release						# release mode
	scrape_mod = Scrape_mode.Scrape_all  	# scrape all friends
	scan_result = managerV2.scrape_and_analyze(email, password, user_url, mod, scrape_mod)

	return render_template('scan_result.html',
							offensiveness_result=scan_result.offensiveness_result,
							potentialFakeNews_result=scan_result.potentialFakeNews_result,
							subjects_result=scan_result.subjects_result)

if __name__ == "__main__":
	app.run()