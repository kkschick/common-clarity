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
	teacher_id = class_info.get("id")
	api.add_new_cohort(name, teacher_id)
	return None

# @app.route("/login", methods=["POST"])
# def process_login():
#     email = request.form.get("email")
#     password = request.form.get("password")

#     if user == None:
#         flash ("This user is not registered yet")
#         return redirect('signup')
#     else:
#         session['user'] = user.id
#         return redirect('/')

# @app.route("/signup", methods=["POST"])
# def make_new_account():
#     email = request.form.get("email")
#     password = request.form.get("password")
#     age = request.form.get("age")
#     gender = request.form.get("gender")
#     zipcode = request.form.get("zipcode")
#     model.create_user(email, password, gender, zipcode, age)
#     flash ("You're registered! Now please log in.")
#     return redirect('/login')

# @app.route("/logout")
# def process_logout():
#     session.clear()
#     return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)