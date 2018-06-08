from flask import Flask, render_template, request, redirect, jsonify, json, session, url_for
from flask_pymongo import PyMongo
from functools import wraps
from bson import json_util
from bson.json_util import dumps
import json
from bson import ObjectId
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash
from credentials import MONGODB_URI

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'unyx-ecosystem'
app.config['MONGO_URI'] = 'MONGODB_URI'

# INSTANTIATE DATABASE CONNECTION
mongo = PyMongo(app)


# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# user model
class User(UserMixin):

    def __init__(self, username):
        self.username = username

    @staticmethod
    def is_authenticated(self):
        self.authenticated

    def get_id(self):
        return self.username

    @staticmethod
    def validate_login(password_hash, password):
        return check_password_hash(password_hash, password)

# VIEWS
##########


# home
@app.route('/')
def home():
	print("Initiating check for an authenticated user...")
	if current_user.is_authenticated:
		print("One authenticated user found: ", current_user)
		return render_template('home.html')
	else:
		print("No authenticated users found.")
		return render_template('home.html')

# check authentication
@app.route('/checklogin', methods=['GET'])
def checklogin():
	print("Initiating check for an authenticated user...")
	if current_user.is_authenticated:
		print("One authenticated user found: ", current_user)
		return jsonify({'success' : "Successful authentication."})
	else:
		print("No authenticated users found.")
		return jsonify({'error' : "No authenticated users."})

# somewhere to register
@app.route('/register', methods=['POST', 'GET'])
def register():
	print("Initiating registration process...")
	if request.method == 'POST':
		print("Checking for users with matching usernames...")
		users = mongo.db.users
		existing_user = users.find_one({'name' : request.form['r_username']})
		if existing_user is not None:
			print("This is the existing user: ", existing_user['name'])
			return jsonify({'error' : 'That username already exists!'})

		if existing_user is None:
			password = request.form['r_password']
			username = request.form['r_username']
			first_name = request.form['first_name']
			last_name = request.form['last_name']
			print("New user's password: ", password)
			print("New user's username: ", username)
			users.insert({'name' : username, 'password' : password, 'first_name' : first_name, 'last_name' : last_name, 'authenticated' : False})
			user = users.find_one({'name' : username})
			print("The inserted user: ", user)
			user_obj = User(username)
			print("This is the user_obj: ", user_obj)
			print("Beginning to login after registration...")
			login_user(user_obj)
			print("Post registration login successful!")
			return redirect(url_for('home'))

	return jsonify({'error' : 'Unknown error occurred while attempting to register!'})

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
	print("Login process initiated...")
	print("Beginning to query database for matching username...")
	username = request.form['username']
	password = request.form['password']
	users = mongo.db.users
	user = users.find_one({'name' : username})

	if user:
		print("Matching username found! ", user)
		print("Provided password: ", password)
		print("User's original pass: ", user['password'])
		print("Beginning to compare passwords...")
		if password == user['password']:
			print("Passwords match.")
			user_obj = User(username)
			print("About to log in...")
			login_user(user_obj)
			print("Login successful!")
			return redirect(url_for('home'))
		return jsonify({'error' : 'Invalid username/password combination!'})
	return jsonify({'error' : 'Unknown error occurred while attempting to login!'})

# somewhere to logout
@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
	print("Initiating logout process...")
	user = current_user
	print("Attempting logout...")
	logout_user()
	print("Initiating check if user is logged out...")
	if current_user.is_authenticated:
		print("Authenticated user found: ", current_user)
		return jsonify({'error' : "User not logged out."})
	else:
		print("No authenticated users found.")
		return jsonify({'success' : "User successfully logged out!"})
	print("Logged out successfully!")
# instead of rendering a template, simply send message so JS can switch elements

'''
# some protected url
@app.route('/protected')
@login_required
def protected():
	return Response("Hello. You're home.")
'''

# callback to reload the user object
@login_manager.user_loader
def load_user(username):
	print("User loader username: ", username)
	users = mongo.db.users
	user = users.find_one({'name' : username})
	print("User loader user: ", user)
	if not user:
		return None
	return User(user['name'])


if __name__ == '__main__':
	app.secret_key = 'mysecret'
	app.run()