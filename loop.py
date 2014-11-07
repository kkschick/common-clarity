from flask import Flask, make_response, send_file, session, jsonify, request
import model
import api
import json

app = Flask(__name__)
app.secret_key = '24KJSF98325KJLSDF972saf29832LFjasf87FZKFJL78f7ds98FSDKLF'

@app.route("/")
def index():
	return send_file("templates/index.html")

def _convert_to_JSON(result):
	"""Convert result object to a JSON web request."""

	response = make_response(json.dumps(result))
	response.headers['Access-Control-Allow-Origin'] = "*"
	response.mimetype = "application/json"
	return response

@app.route("/api/addclass/", methods=['POST'])
def addclass():
	class_info = json.loads(request.data)
	name = class_info.get("name")
	teacher_id = session['user']
	cohort = api.add_new_cohort(name, teacher_id)
	return "Success"

@app.route("/api/getclasses/")
def get_cohorts():
	teacher_id = session['user']
	cohorts = api.get_teacher_cohorts(teacher_id)
	cohort_names = []
	for cohort in cohorts:
		cohort_names.append(cohort.name)
	return _convert_to_JSON(cohort_names)

@app.route("/api/signup/", methods=['POST'])
def adduser():
	new_user = json.loads(request.data)
	user_type = "teacher"
	first_name = new_user.get("first_name")
	last_name = new_user.get("last_name")
	email = new_user.get("email")
	username = new_user.get("username")
	password = new_user.get("password")
	api.create_teacher_user(user_type, first_name, last_name, email, username, password)
	return "Success"

@app.route("/api/login/", methods=['POST'])
def loginuser():
	user_to_login = json.loads(request.data)
	username = user_to_login.get("username")
	password = user_to_login.get("password")
	user = api.get_user(username, password)
	session['user'] = user.id
	return "Success"


@app.route("/api/logout/", methods=['POST'])
def process_logout():
	api.logout()


if __name__ == "__main__":
	app.run(debug = True)