from flask import Flask, render_template, redirect, request, flash, send_file, session, url_for, jsonify
import model
import api

app = Flask(__name__)
app.secret_key = '24KJSF98325KJLSDF972saf29832LFjasf87FZKFJL78f7ds98FSDKLF'

@app.route("/")
def index():
    return send_file("templates/index.html")

# @app.route("/about")
# def about():
#     return render_template("about.html")

# @app.route("/login")
# def show_login():
#     return render_template("login.html")

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

# @app.route("/signup")
# def show_signup():
#     return render_template("signup.html")

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