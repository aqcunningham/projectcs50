# Some portions of this code were developed with the help of AI tools (e.g., ChatGPT)
# for debugging and brainstorming. All logic was reviewed, modified, and understood by me.
import os

from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

app.config["SESSION_PERMANENT"]= False
app.config["SESSION_TYPE"]= "filesystem"

Session(app)

db = SQL("sqlite:///resume.db")

def login_req(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if session.get("user_id") is None:
			return redirect("/login")
		return f(*args, **kwargs)
	return decorated_function


@app.route("/")
def index():
	return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		return render_template("register.html")

	username= request.form.get("username")
	password= request.form.get("password")
	confirmation= request.form.get("confirmation")

	if not username:
		return "Please provide username", 400

	if not password:
		return "Please provide password", 400

	if password != confirmation:
		return "Passwords don't match", 400

	existing = db.execute("select * from users where username = ?", username)

	if  existing:
		return "username already exists", 400

	hash_pass=generate_password_hash(password)
	db.execute("insert into users (username, hash) values (?,?)", username, hash_pass)

	return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
	# Forget any user_id
	session.clear()

	if request.method == "GET":
		 return render_template("login.html")
	username= request.form.get("username")
	password= request.form.get("password")

	if not username or not password:
		 return "missing username or password", 400

	rows = db.execute("select * from users where username = ?", username)
	if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
		return "invalid username or password", 403

	session["user_id"] = rows[0]["id"]
	return redirect("/")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")




# creating a resume form, similar to finance problem:
@app.route("/resume/new", methods=["GET", "POST"])
@login_req
def resume_new():
	if request.method == "GET":
		return render_template("resume_form.html")

	full_name = request.form.get("full_name")
	headline = request.form.get("headline")
	email = request.form.get("email")
	phone = request.form.get("phone")
	summary = request.form.get("summary")
	education = request.form.get("education")
	experience = request.form.get("experience")
	skills = request.form.get("skills")

	# basic validation
	if not full_name:
		return "Missing name", 400

	resume_id = db.execute(
		"""INSERT INTO resumes
		   (user_id, full_name, headline, email, phone, summary, education, experience, skills)
		   VALUES (:user_id, :full_name, :headline, :email, :phone, :summary, :education, :experience, :skills)""",
		user_id=session["user_id"],
		full_name=full_name,
		headline=headline,
		email=email,
		phone=phone,
		summary=summary,
		education=education,
		experience=experience,
		skills=skills,
	)

	return redirect(f"/resume/{resume_id}")

# rendering resume webpage
@app.route("/resume/<int:resume_id>")
def resume_view(resume_id):
	rows = db.execute("SELECT * FROM resumes WHERE id = :id", id=resume_id)
	if not rows:
		return "Not found", 404
	resume = rows[0]
	return render_template("resume_view.html", resume=resume)

@app.route("/resumes")
@login_req
def resume_list():
    # Get all resumes that belong to the logged-in user
    rows = db.execute(
        "SELECT id, full_name, headline FROM resumes WHERE user_id = :u ORDER BY id DESC",
        u=session["user_id"],
    )
    return render_template("resume_list.html", resumes=rows)
@app.route("/p/<int:resume_id>")
def resume_public(resume_id):
    rows = db.execute("SELECT * FROM resumes WHERE id = :id", id=resume_id)

    if not rows:
        return "Not found", 404

    resume = rows[0]
    return render_template("resume_public.html", resume=resume)


if __name__ == "__main__":
    app.run(debug=True)



